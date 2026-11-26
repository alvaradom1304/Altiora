"""PREAMBRA OS V3.1 - lanzador por perfil (LEAN / STANDARD / ADVANCED) multi-IA con controles de arranque.

Fuente de perfiles, limites y reglas de seguridad: team/profiles/profiles.json (no duplicar aqui).
No instala nada, no toca configuracion global y no usa red propia. Cada ejecucion pasa un preflight
obligatorio; si un control falla, la accion se bloquea (exit 2) y no se lanza ningun proveedor.
Los controles obligatorios son reglas nativas del cliente (--disallowedTools, sandbox de Codex) y una
verificacion de integridad posterior; no dependen de hooks, que fallan abiertos al agotar su tiempo.

  --check        Proyecto, perfil efectivo, modelo/esfuerzo, herramientas, seguridad y presupuesto (sin consumo).
  --dry-run      Preflight + comando que se ejecutaria (sin consumo).
  --interactive  Abre una sesion interactiva de Claude CLI con el perfil (lanzador para Desktop/terminal).
  (normal)       Preflight -> proveedor con reintentos -> respaldo -> integridad -> registro CSV.
Codigos de salida: 0 ok, 2 bloqueado, 3 violacion de integridad, 4 calidad FAIL, otro = fallo del proveedor.

Uso: python scripts/lean_run.py --project auto --task-file t.txt --log consumo.csv \
        [--profile lean|standard|advanced] [--provider claude|codex|agy|det] [--effort low|medium|high] \
        [--task-id T1 --role worker|reviewer --depends-on T0] [--reason "..."] [--approved-risk] \
        [--allow-exec] [--det-cmd "python render.py"] [--verify-cmd "python validate.py"]
"""
from __future__ import annotations

import argparse
import re
import tempfile
import csv
import fnmatch
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES_FILE = ROOT / "team" / "profiles" / "profiles.json"
LEAN_PROMPT = ROOT / "team" / "profiles" / "lean.md"
CHAIN_ENV = "PREAMBRA_DELEGATION_CHAIN"
SKIP_DIRS = {".git", "node_modules", "graphify-out", ".next", "dist", "build", "__pycache__", ".venv", "venv"}
FIELDS = ["fecha", "task_id", "etiqueta", "rol", "intento", "perfil", "proveedor", "modelo", "esfuerzo", "estado",
          "turnos", "segundos", "entrada", "cache_creada", "cache_leida", "salida", "total", "ponderado",
          "costo_nocional_usd", "costo_real", "cuota", "herramientas", "mcp", "skills", "coordinacion", "calidad"]

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preambra_v2_routing import risk_signals  # noqa: E402


def load_config(path: Path = PROFILES_FILE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def chain_from_env(env: dict | None = None) -> list[str]:
    raw = (env if env is not None else os.environ).get(CHAIN_ENV, "")
    return [p for p in raw.split(",") if p]


def git_info(cwd: Path) -> tuple[Path | None, str | None]:
    def run(*args: str) -> str | None:
        try:
            out = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return out.stdout.strip() if out.returncode == 0 else None
    top = run("rev-parse", "--show-toplevel")
    return (Path(top).resolve() if top else None), run("remote", "get-url", "origin")


def remote_slug(url: str | None) -> str | None:
    if not url:
        return None
    parts = url.rstrip("/").removesuffix(".git").replace(":", "/").split("/")
    return "/".join(parts[-2:]).lower() if len(parts) >= 2 else None


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def detect_project(cwd: Path, cfg: dict, git=git_info) -> str | None:
    """Seleccion automatica por el remote del repo; las carpetas sin git no se adivinan."""
    slug = remote_slug(git(cwd)[1])
    return next((pid for pid, p in cfg["projects"].items() if p.get("kind") == "git" and p["remote"].lower() == slug), None)


def check_project(project: str, cwd: Path, add_dirs: list[str], allow_external: bool, cfg: dict,
                  git=git_info) -> tuple[dict, list[str], Path | None]:
    """Aislamiento: el cwd pertenece al proyecto declarado y no se anaden carpetas de otro proyecto."""
    spec = cfg["projects"].get(project)
    if not spec:
        return {"project": project}, [f"proyecto desconocido o no detectable: {project} (registrar en profiles.json)"], None
    blocks: list[str] = []
    top, url = git(cwd)
    slug = remote_slug(url)
    info = {"project": project, "cwd": str(cwd), "git_root": str(top) if top else None, "remote": slug}
    if spec["kind"] == "git":
        if slug != spec["remote"].lower():
            blocks.append(f"cwd no pertenece a {spec['remote']} (remote observado: {slug})")
        root = top
    else:
        registered = {p["remote"].lower() for p in cfg["projects"].values() if p.get("kind") == "git"}
        if slug in registered:
            blocks.append(f"proyecto carpeta '{project}' dentro del repo registrado {slug}: contexto ajeno")
        root = cwd
    for d in add_dirs:
        if root is not None and not is_within(Path(d), root):
            if allow_external:
                info.setdefault("external_dirs", []).append(d)
            else:
                blocks.append(f"--add-dir fuera del proyecto: {d} (usar --allow-external-dir si es intencional)")
    return info, blocks, root


def resolve_profile(profile: str, effort: str | None, reason: str | None, cfg: dict) -> tuple[dict, list[str]]:
    prof = cfg["profiles"].get(profile)
    if prof is None:
        raise ValueError(f"perfil desconocido: {profile}")
    blocks: list[str] = []
    eff = effort or prof["default_effort"]
    if eff not in prof["efforts"]:
        blocks.append(f"esfuerzo {eff} no permitido en {profile} {prof['efforts']}: escalar con --profile advanced --reason")
    if prof.get("requires_reason") and not (reason or "").strip():
        blocks.append(f"el perfil {profile} exige --reason (escalamiento justificado)")
    return {**prof, "name": profile, "effort": eff}, blocks


def deny_list(prof: dict, cfg: dict, allow_exec: bool = False) -> list[str]:
    extra = list(prof.get("extra_deny", []))
    if not allow_exec:
        extra.append("Bash")  # sin --allow-exec, ningun comando: acceptEdits aprobaba 'echo > x' aun sin Bash permitido
    return list(cfg["security"]["deny_tools"]) + extra


def scoped_tools(tools: str) -> str:
    """Edit/Write sin ruta autorizan cualquier carpeta: se limitan al directorio de trabajo."""
    return ",".join(f"{t}(./**)" if t in ("Edit", "Write") else t for t in tools.split(","))


def model_for(provider: str, effort: str, cfg: dict) -> str:
    if provider == "det":
        return "determinista"
    table = cfg["models"][provider]
    return table.get(effort) or table["medium"]


def build_command(provider: str, prof: dict, cfg: dict, cwd: str, add_dirs: list[str], mcp_configs: list[str],
                  allow_write: bool = False, allow_exec: bool = False, interactive: bool = False,
                  det_cmd: str | None = None) -> list[str]:
    eff, sec = prof["effort"], cfg["security"]
    if provider == "det":
        return shlex.split(det_cmd or "", posix=sys.platform != "win32")
    model = model_for(provider, eff, cfg)
    if provider == "claude":
        tools = scoped_tools(prof["tools"]) + ("," + prof["exec_tools"] if allow_exec and prof.get("exec_tools") else "")
        # Modo default: lo no autorizado pide permiso y en -p se deniega (acceptEdits auto-aprobaba comandos de archivos).
        cmd = ["claude"] + ([] if interactive else ["-p"]) + ["--model", model, "--effort", eff,
               "--permission-mode", "default", "--allowedTools", tools,
               "--disallowedTools", ",".join(deny_list(prof, cfg, allow_exec)), *prof["claude_flags"]]
        if not interactive:  # --max-turns y --max-budget-usd solo existen en modo -p
            cmd += ["--no-session-persistence", "--max-turns", str(prof["max_turns"]),
                    "--max-budget-usd", str(prof["max_budget_usd"]), "--output-format", "stream-json", "--verbose"]
        if prof.get("append_prompt"):
            cmd += ["--append-system-prompt-file", str(ROOT / prof["append_prompt"])]
        if "--strict-mcp-config" in prof["claude_flags"] and "--safe-mode" not in prof["claude_flags"]:
            for c in mcp_configs:
                cmd += ["--mcp-config", c]
        for d in add_dirs:
            cmd += ["--add-dir", d]
        return cmd
    if provider == "codex":
        sandbox = sec["codex_sandbox_write"] if allow_write else sec["codex_sandbox"]
        flags = list(prof.get("codex_flags", []))
        if "--ignore-user-config" in flags and sys.platform == "win32" and sec.get("codex_windows_sandbox"):
            flags += ["-c", f"windows.sandbox={sec['codex_windows_sandbox']}"]
        return ["codex", "exec", "-s", sandbox, "--skip-git-repo-check", "--ephemeral", "--json",
                *flags, "-m", model, "-c", f"model_reasoning_effort={eff}", "-C", cwd, "-"]
    if provider == "agy":
        mode = sec["agy_mode_write"] if allow_write else sec["agy_mode"]
        cmd = ["agy", "--model", model, "--effort", eff, "--mode", mode, "--disable-slash-commands",
               "--output-format", "json"]
        for d in add_dirs:
            cmd += ["--add-dir", d]
        return cmd + ["-p"]  # el prompt se anade al final
    raise ValueError(f"proveedor desconocido: {provider}")


def security_check(cmd: list[str], provider: str, cfg: dict, interactive: bool = False) -> list[str]:
    """Controles obligatorios sobre el comando final: si alguno falla, se bloquea."""
    blocks = []
    joined = " ".join(cmd)
    for flag in cfg["security"]["forbidden_flags"]:
        if flag in joined:
            blocks.append(f"bandera prohibida: {flag}")
    if provider == "claude":
        if "--disallowedTools" not in cmd or not cmd[cmd.index("--disallowedTools") + 1]:
            blocks.append("faltan reglas de denegacion (--disallowedTools)")
        if "--safe-mode" in cmd and "Write(**/.env*)" not in joined:
            blocks.append("safe-mode apaga los hooks y no hay denegacion sustituta para secretos")
        if not interactive and ("--max-turns" not in cmd or "--max-budget-usd" not in cmd):
            blocks.append("falta presupuesto (--max-turns / --max-budget-usd)")
    if provider == "codex" and "-s" not in cmd:
        blocks.append("codex sin sandbox explicito")
    if provider == "det" and not cmd:
        blocks.append("proveedor determinista sin --det-cmd")
    return blocks


def read_log(log: Path | None) -> list[dict]:
    if not log or not log.is_file():
        return []
    with log.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_limits(a, prof: dict, cfg: dict, chain: list[str], provider: str, rows: list[dict]) -> list[str]:
    lim, blocks = cfg["limits"], []
    if provider in chain:
        blocks.append(f"ciclo de delegacion: {provider} ya esta en la cadena {chain}")
    if len(chain) >= lim["max_delegation_depth"]:
        blocks.append(f"profundidad de delegacion {len(chain)} >= {lim['max_delegation_depth']}: un trabajador delegado no re-delega")
    mine = [r for r in rows if r.get("task_id") == a.task_id] if a.task_id else []
    if a.role == "reviewer" and sum(r.get("rol") == "reviewer" for r in mine) >= lim["max_review_cycles"]:
        blocks.append(f"ciclos de revision agotados para {a.task_id}: max {lim['max_review_cycles']}")
    if a.role == "worker" and any(r.get("rol") == "worker" and r.get("estado") == "OK" for r in mine):
        blocks.append(f"tarea duplicada: {a.task_id} ya se completo (usar otro --task-id o --role reviewer)")
    used = sum(int(r.get("total") or 0) for r in mine)
    if used >= prof.get("max_task_tokens", float("inf")):
        blocks.append(f"presupuesto de tokens agotado para {a.task_id}: {used} >= {prof['max_task_tokens']}")
    if len(mine) >= lim.get("max_delegations_per_task", float("inf")):
        blocks.append(f"presupuesto de coordinacion agotado para {a.task_id}: {len(mine)} intentos/delegaciones")
    for dep in a.depends_on:
        ok = [r for r in rows if r.get("task_id") == dep and r.get("estado") == "OK" and r.get("calidad") != "FAIL"]
        if not ok:
            blocks.append(f"dependencia no satisfecha: {dep} no tiene resultado OK validado")
    return blocks


def integrity_snapshot(root: Path | None, cfg: dict) -> dict[str, str]:
    """Huella sha256 de archivos protegidos del proyecto: secretos y configuracion."""
    if root is None or not root.is_dir():
        return {}
    sec = cfg["security"]
    names = [n.lower() for n in sec["protected_names"]]
    paths = [p.replace("\\", "/") for p in sec["protected_paths"]]
    snap = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            full = Path(dirpath) / fn
            rel = full.relative_to(root).as_posix()
            low = fn.lower()
            if low in (".env.example", ".env.sample", ".env.template"):
                continue
            if any(fnmatch.fnmatchcase(low, n) for n in names) or any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in paths):
                try:
                    snap[rel] = hashlib.sha256(full.read_bytes()).hexdigest()  # contenido, no mtime/tamano
                except OSError as exc:  # ilegible: se registra igual y cualquier cambio de estado cuenta
                    snap[rel] = f"ILEGIBLE:{type(exc).__name__}"
    return snap


def integrity_diff(before: dict, after: dict) -> list[str]:
    changed = [k for k in after if k not in before or before[k] != after[k]]
    removed = [k for k in before if k not in after]
    return sorted(changed + removed)


def parse_stream(lines) -> dict:
    """Claude stream-json, Codex --json o Agy json: toma init, result y el ultimo bloque con usage."""
    init, result, usage, last_msg, model_seen = {}, {}, {}, "", None
    for line in lines:
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            init = obj
        if obj.get("type") == "result":
            result = obj
        if isinstance(obj.get("usage"), dict):
            usage = obj["usage"]
        item = obj.get("item") if isinstance(obj.get("item"), dict) else {}
        if item.get("type") == "agent_message" and item.get("text"):  # Codex --json
            last_msg = item["text"]
        model_seen = obj.get("model") if isinstance(obj.get("model"), str) else model_seen
    u = result.get("usage", usage)
    creada = u.get("cache_creation_input_tokens", 0)
    if "cached_input_tokens" in u:  # Codex/OpenAI: input_tokens ya incluye los cacheados
        leida = u["cached_input_tokens"]
        entrada = max(u.get("input_tokens", 0) - leida, 0)
    else:
        leida = u.get("cache_read_input_tokens", 0)
        entrada = u.get("input_tokens", 0)
    salida = u.get("output_tokens", 0)
    resultado = str(result.get("result", "") or last_msg)
    ok = ((bool(result) and not result.get("is_error", False)) or (not result and bool(usage))) and bool(resultado.strip())
    return {
        "turnos": result.get("num_turns", 0), "segundos": round(result.get("duration_ms", 0) / 1000),
        "entrada": entrada, "cache_creada": creada, "cache_leida": leida, "salida": salida,
        "total": entrada + creada + leida + salida,
        "ponderado": round(entrada + creada * 1.25 + leida * 0.1 + salida * 5),
        "costo_nocional_usd": round(result.get("total_cost_usd", 0), 3),
        "costo_real": "SUSCRIPCION_SIN_CARGO_API" if init.get("apiKeySource", "none") == "none" else "API_VER_FACTURA",
        "cuota": "NO_OBSERVADA",
        "herramientas": len(init.get("tools", [])), "mcp": len(init.get("mcp_servers", [])),
        "skills": len(init.get("skills", [])), "modelo_efectivo": init.get("model") or model_seen or "NO_OBSERVADO",
        "resultado": resultado[:200], "ok": ok,
    }


def append_log(path: Path, row: dict) -> None:
    fields = FIELDS
    new = not path.exists() or not path.stat().st_size
    if not new:
        with path.open(encoding="utf-8") as fh:
            fields = next(csv.reader(fh), FIELDS)  # respeta registros previos con otra cabecera
    with path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerow(row)


TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def valid_task_id(task_id: str | None) -> bool:
    return bool(TASK_ID_RE.match(task_id or "")) and ".." not in (task_id or "")


def new_task_id(task: str) -> str:
    return "T-" + time.strftime("%Y%m%d%H%M%S") + "-" + hashlib.sha256(task.encode("utf-8")).hexdigest()[:6]


def preflight(a, cfg: dict, which=None, git=None, env: dict | None = None) -> dict:
    which, git = which or shutil.which, git or git_info
    chain = chain_from_env(env)
    prof, blocks = resolve_profile(a.profile, a.effort, a.reason, cfg)
    if a.project == "auto":
        a.project = detect_project(Path(a.cwd), cfg, git=git) or "auto"
    proj, pblocks, root = check_project(a.project, Path(a.cwd), a.add_dir, a.allow_external_dir, cfg, git=git)
    blocks += pblocks
    task = Path(a.task_file).read_text(encoding="utf-8") if a.task_file and Path(a.task_file).is_file() else ""
    if not a.task_id and task:
        a.task_id = new_task_id(task)
    if a.task_id and not valid_task_id(a.task_id):
        blocks.append(f"--task-id invalido (solo letras, numeros, . _ -; sin rutas): {a.task_id!r}")
        a.task_id = None
    signals = risk_signals(task) if task else []
    if signals and not a.approved_risk:
        blocks.append(f"riesgo critical en la tarea {signals}: requiere aprobacion humana (--approved-risk)")
    if a.allow_write and a.provider in ("codex", "agy"):
        blocks.append("--allow-write bloqueado para codex/agy: su sandbox no puede denegar rutas protegidas (decision del fundador)")
    if a.allow_exec and signals:
        blocks.append("--allow-exec no se combina con tareas de riesgo critical: los scripts escapan a las reglas por herramienta")
    known = cfg.get("known_providers", ["claude", "codex", "agy"])
    available = {p: bool(which(p)) for p in known}
    if a.det_cmd:
        order = ["det"]
        available["det"] = True
    else:
        order = ([a.provider] if a.provider else []) + [p for p in prof["providers"] if p != a.provider]
    chosen = next((p for p in order if available.get(p)), None)
    cmd: list[str] = []
    if chosen is None:
        blocks.append(f"ningun proveedor disponible en {order}")
    else:
        cmd = build_command(chosen, prof, cfg, a.cwd, a.add_dir, a.mcp_config, a.allow_write, a.allow_exec,
                            getattr(a, "interactive", False), a.det_cmd)
        blocks += security_check(cmd, chosen, cfg, getattr(a, "interactive", False))
        if a.context_file:
            blocks += check_context_files(a.context_file, root, cfg)
        blocks += check_script_cmd(a.det_cmd, root, cfg, "--det-cmd")
        blocks += check_script_cmd(a.verify_cmd, root, cfg, "--verify-cmd")
        if chosen != "det" and not resolve_exe(cmd[0], which):
            blocks.append(f"ejecutable de {chosen} no es un binario nativo resoluble: se rechaza shell para evitar inyeccion")
        if getattr(a, "interactive", False) and chain:
            blocks.append(f"sesion interactiva pedida desde una delegacion {chain}: un trabajador no abre sesiones")
        blocks += check_limits(a, prof, cfg, chain, chosen, read_log(Path(a.log) if a.log else None))
    return {
        "status": "BLOCKED" if blocks else "READY", "blocks": blocks, **proj, "task_id": a.task_id,
        "profile": prof["name"], "provider_order": order, "providers_available": available,
        "provider": chosen, "fallback_used": bool(a.provider and chosen and chosen != a.provider),
        "model_planned": model_for(chosen, prof["effort"], cfg) if chosen else None,
        "model_effective": "NO_OBSERVADO (se lee del evento init al ejecutar)",
        "effort": prof["effort"], "tools_allowed": cmd[cmd.index("--allowedTools") + 1] if "--allowedTools" in cmd else None,
        "deny_rules": len(deny_list(prof, cfg, a.allow_exec)), "hooks": prof.get("hooks"),
        "exec": "PERMITIDO (limitacion: scripts no pasan por reglas por herramienta; integridad posterior)" if a.allow_exec else "NO",
        "interactive_limits": ("sin presupuesto ni integridad automaticos (limitacion de la plataforma)"
                               if getattr(a, "interactive", False) else None),
        "budget": {"max_turns": prof["max_turns"], "max_budget_usd_nocional": prof["max_budget_usd"],
                   "max_task_tokens": prof.get("max_task_tokens"), **cfg["limits"]},
        "risk_signals": signals, "delegation_chain": chain, "project_root": str(root) if root else None, "command": cmd,
    }


def neutral_workspace(task_id: str, files: list[str], root: Path) -> Path:
    """Carpeta neutra: solo los archivos autorizados (rutas relativas al proyecto) y las reglas LEAN como AGENTS.md.
    Evita que Codex cargue AGENTS.md completo y las skills del repo (.agents/skills)."""
    if not valid_task_id(task_id):
        raise ValueError(f"task_id invalido: {task_id!r}")
    base = Path(tempfile.gettempdir()) / "preambra-neutral"
    base.mkdir(exist_ok=True)
    dest = Path(tempfile.mkdtemp(prefix=f"{task_id}-", dir=base))  # carpeta nueva y exclusiva; nunca se borra nada
    for rel in files:
        src = (root / rel).resolve()
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    (dest / "AGENTS.md").write_text(LEAN_PROMPT.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def check_script_cmd(cmd_text: str | None, root: Path | None, cfg: dict, label: str) -> list[str]:
    """--det-cmd / --verify-cmd: solo 'python|node <script versionado del proyecto> [args]', sin codigo en linea."""
    if not cmd_text:
        return []
    parts = shlex.split(cmd_text, posix=sys.platform != "win32")
    runner = Path(parts[0]).stem.lower() if parts else ""
    if runner not in cfg["security"]["script_runners"] or len(parts) < 2 or parts[1].startswith("-"):
        return [f"{label} debe ser 'python|node <script del proyecto>' sin -c/-e: {cmd_text!r}"]
    script = (root / parts[1]) if root else Path(parts[1])
    if root is None or not script.is_file() or not is_within(script, root):
        return [f"{label}: script fuera del proyecto o inexistente: {parts[1]}"]
    if (root / ".git").exists():
        tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", str(script.resolve())],
                                 capture_output=True, text=True)
        if tracked.returncode != 0:
            return [f"{label}: el script no esta versionado en git (solo se ejecuta codigo revisado): {parts[1]}"]
    return []


def check_context_files(files: list[str], root: Path | None, cfg: dict) -> list[str]:
    blocks = []
    names = [n.lower() for n in cfg["security"]["protected_names"]]
    for rel in files:
        src = (root / rel) if root else Path(rel)
        if root is None or not src.is_file() or not is_within(src, root):
            blocks.append(f"--context-file invalido o fuera del proyecto: {rel}")
        elif any(fnmatch.fnmatchcase(src.name.lower(), n) for n in names):
            blocks.append(f"--context-file protegido (secreto): {rel}")
    return blocks


def resolve_exe(name: str, which=None) -> str | None:
    """Ruta absoluta del binario; en Windows solo .exe (un .cmd/.bat obligaria a pasar por cmd.exe)."""
    path = (which or shutil.which)(name)
    if not path:
        return None
    if sys.platform == "win32" and str(path).lower().endswith((".cmd", ".bat")):
        return None
    return str(path)


def run_provider(cmd: list[str], provider: str, task: str, cwd: str, env: dict) -> subprocess.CompletedProcess:
    """Nunca shell=True: la tarea no puede inyectar comandos (hallazgo critico de la revision V31-REV)."""
    exe = resolve_exe(cmd[0])
    if exe is None:
        raise RuntimeError(f"binario no resoluble sin shell: {cmd[0]}")
    cmd = [exe, *cmd[1:]]
    if provider == "agy":
        cmd, task = cmd + [task], ""  # argumento de proceso, sin interprete de shell
    return subprocess.run(cmd, input=task if provider != "det" else None, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=cwd, env=env)


def parser(cfg: dict) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", choices=sorted(cfg["profiles"]), default=cfg["default_profile"])
    ap.add_argument("--project", default="auto", help="Id de profiles.json o 'auto' (por el remote del cwd).")
    ap.add_argument("--task-file")
    ap.add_argument("--cwd", default=".")
    ap.add_argument("--add-dir", action="append", default=[])
    ap.add_argument("--allow-external-dir", action="store_true")
    ap.add_argument("--mcp-config", action="append", default=[])
    ap.add_argument("--provider", choices=["claude", "codex", "agy", "det"])
    ap.add_argument("--det-cmd", help="Ejecucion determinista sin IA (se prefiere cuando basta).")
    ap.add_argument("--effort")
    ap.add_argument("--reason")
    ap.add_argument("--approved-risk", action="store_true", help="El fundador aprobo el riesgo detectado.")
    ap.add_argument("--allow-write", action="store_true", help="Codex workspace-write / Agy accept-edits.")
    ap.add_argument("--allow-exec", action="store_true", help="Claude: anade exec_tools del perfil (Bash(python *)).")
    ap.add_argument("--context-file", action="append", default=[],
                    help="Codex/Agy: copia solo estos archivos (relativos al proyecto) a una carpeta neutra y trabaja alli.")
    ap.add_argument("--task-id")
    ap.add_argument("--depends-on", action="append", default=[])
    ap.add_argument("--role", choices=["worker", "reviewer"], default="worker")
    ap.add_argument("--label", default="")
    ap.add_argument("--log")
    ap.add_argument("--raw-dir", help="Carpeta donde guardar la salida bruta de cada intento (evidencia).")
    ap.add_argument("--verify-cmd", help="Comprobacion determinista posterior; su exit code fija 'calidad'.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--interactive", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    cfg = load_config()
    a = parser(cfg).parse_args(argv)
    a.cwd = str(Path(a.cwd).resolve())
    if a.interactive and a.provider not in (None, "claude"):
        print(json.dumps({"status": "BLOCKED", "blocks": ["--interactive solo esta implementado para Claude CLI"]}))
        return 2
    report = preflight(a, cfg)
    if a.check or a.dry_run or report["status"] == "BLOCKED":
        if a.check:
            report.pop("command")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if report["status"] == "BLOCKED" else 0
    if a.interactive:
        print(json.dumps({k: report[k] for k in ("project", "profile", "model_planned", "effort", "deny_rules", "hooks")},
                         ensure_ascii=False))
        return subprocess.call([resolve_exe("claude"), *report["command"][1:]], cwd=a.cwd,
                               env={**os.environ, CHAIN_ENV: ",".join(chain_from_env() + ["claude"])})
    if not (a.task_file and a.log):
        print(json.dumps({"status": "BLOCKED", "blocks": ["ejecucion real exige --task-file y --log"]}))
        return 2
    task = Path(a.task_file).read_text(encoding="utf-8")
    chain = chain_from_env()
    prof, _ = resolve_profile(a.profile, a.effort, a.reason, cfg)
    root = Path(report["project_root"]) if report["project_root"] else None
    rc, attempt = 1, 0
    for provider in [p for p in report["provider_order"] if report["providers_available"].get(p)]:
        run_cwd = a.cwd
        if a.context_file and provider in ("codex", "agy") and root:
            run_cwd = str(neutral_workspace(a.task_id, a.context_file, root))
        cmd = build_command(provider, prof, cfg, run_cwd, a.add_dir, a.mcp_config, a.allow_write, a.allow_exec,
                            False, a.det_cmd)
        if security_check(cmd, provider, cfg):  # el respaldo pasa los mismos controles
            continue
        env = {**os.environ, CHAIN_ENV: ",".join(chain + [provider])}
        for _ in range(cfg["limits"]["max_retries"] + 1):
            again = check_limits(a, prof, cfg, chain, provider, read_log(Path(a.log)))
            if again:  # presupuesto, coordinacion y duplicados se revalidan antes de cada intento y respaldo
                print(json.dumps({"status": "BLOCKED", "task_id": a.task_id, "blocks": again}, ensure_ascii=False))
                return 2
            attempt += 1
            t0 = time.time()
            before = integrity_snapshot(root, cfg)
            proc = run_provider(cmd, provider, task, run_cwd, env)
            violations = integrity_diff(before, integrity_snapshot(root, cfg))
            stats = parse_stream(proc.stdout.splitlines()) if provider != "det" else {
                **parse_stream([]), "resultado": proc.stdout.strip()[:200], "ok": True}
            if a.raw_dir:
                Path(a.raw_dir).mkdir(parents=True, exist_ok=True)
                (Path(a.raw_dir) / f"{a.task_id}-{attempt}-{provider}.jsonl").write_text(proc.stdout, encoding="utf-8")
            stats["segundos"] = stats["segundos"] or round(time.time() - t0)
            ok = proc.returncode == 0 and stats["ok"]
            calidad = ""
            if ok and not violations and a.verify_cmd:
                vparts = shlex.split(a.verify_cmd, posix=sys.platform != "win32")
                v = subprocess.run([resolve_exe(vparts[0]) or vparts[0], *vparts[1:]], cwd=a.cwd)
                calidad = "PASS" if v.returncode == 0 else "FAIL"
                violations = integrity_diff(before, integrity_snapshot(root, cfg))  # el verificador tambien se audita
            estado = ("VIOLACION_INTEGRIDAD" if violations else "FALLO_CALIDAD" if calidad == "FAIL"
                      else "OK" if ok else f"FALLO_rc{proc.returncode}")
            row = {"fecha": time.strftime("%Y-%m-%d %H:%M"), "task_id": a.task_id, "etiqueta": a.label,
                   "rol": a.role, "intento": attempt, "perfil": a.profile, "proveedor": provider,
                   "modelo": stats["modelo_efectivo"] if stats["modelo_efectivo"] != "NO_OBSERVADO" else model_for(provider, prof["effort"], cfg) + " (planeado)",
                   "esfuerzo": prof["effort"], "estado": estado, "coordinacion": len(chain) + 1, "calidad": calidad, **stats}
            append_log(Path(a.log), row)
            print(json.dumps({**{k: row[k] for k in ("task_id", "proveedor", "modelo", "intento", "estado", "turnos", "total",
                                                    "calidad", "resultado")}, "violaciones": violations}, ensure_ascii=False))
            if violations:
                return 3  # nunca se reintenta ni se pasa a otro proveedor tras una violacion
            if calidad == "FAIL":
                return 4
            if ok:
                return 0
            rc = proc.returncode or 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
