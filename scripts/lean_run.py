"""PREAMBRA OS V3 - lanzador por perfil (LEAN / STANDARD / ADVANCED) multi-IA con controles de arranque.

Fuente de perfiles, limites y reglas de seguridad: team/profiles/profiles.json (no duplicar aqui).
No instala nada, no toca configuracion global y no usa red propia. Cada ejecucion pasa un preflight
obligatorio; si un control falla, la accion se bloquea (exit 2) y no se lanza ningun proveedor.

  --check    Verifica proyecto, perfil efectivo, modelo/esfuerzo, herramientas, seguridad y presupuesto (sin consumo).
  --dry-run  Preflight + comando que se ejecutaria (sin consumo).
  (normal)   Preflight -> proveedor con hasta N reintentos -> respaldo si no esta disponible -> registro CSV.

Uso: python scripts/lean_run.py --project altiora --task-file t.txt --cwd . --log consumo.csv \
        [--profile lean|standard|advanced] [--provider claude|codex|agy] [--effort low|medium|high] \
        [--task-id T1 --role worker|reviewer] [--reason "..."] [--approved-risk] [--verify-cmd "python v.py"]
"""
from __future__ import annotations

import argparse
import csv
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


def check_project(project: str, cwd: Path, add_dirs: list[str], allow_external: bool, cfg: dict,
                  git=git_info) -> tuple[dict, list[str]]:
    """Aislamiento: el cwd pertenece al proyecto declarado y no se anaden carpetas de otro proyecto."""
    spec = cfg["projects"].get(project)
    if not spec:
        return {"project": project}, [f"proyecto desconocido: {project} (registrar en profiles.json)"]
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
    return info, blocks


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


def deny_list(prof: dict, cfg: dict) -> list[str]:
    return list(cfg["security"]["deny_tools"]) + list(prof.get("extra_deny", []))


def model_for(provider: str, effort: str, cfg: dict) -> str:
    table = cfg["models"][provider]
    return table.get(effort) or table["medium"]


def build_command(provider: str, prof: dict, cfg: dict, cwd: str, add_dirs: list[str], mcp_configs: list[str],
                  allow_write: bool = False) -> list[str]:
    eff, sec = prof["effort"], cfg["security"]
    model = model_for(provider, eff, cfg)
    if provider == "claude":
        cmd = ["claude", "-p", "--model", model, "--effort", eff, "--no-session-persistence",
               "--max-turns", str(prof["max_turns"]), "--max-budget-usd", str(prof["max_budget_usd"]),
               "--permission-mode", "acceptEdits", "--allowedTools", prof["tools"],
               "--disallowedTools", ",".join(deny_list(prof, cfg)),
               "--output-format", "stream-json", "--verbose", *prof["claude_flags"]]
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
        return ["codex", "exec", "-s", sandbox, "--skip-git-repo-check", "--ephemeral", "--json",
                "-m", model, "-c", f"model_reasoning_effort={eff}", "-C", cwd, "-"]
    if provider == "agy":
        mode = sec["agy_mode_write"] if allow_write else sec["agy_mode"]
        cmd = ["agy", "--model", model, "--effort", eff, "--mode", mode, "--disable-slash-commands",
               "--output-format", "json"]
        for d in add_dirs:
            cmd += ["--add-dir", d]
        return cmd + ["-p"]  # el prompt se anade al final
    raise ValueError(f"proveedor desconocido: {provider}")


def security_check(cmd: list[str], provider: str, cfg: dict) -> list[str]:
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
        if "--max-turns" not in cmd or "--max-budget-usd" not in cmd:
            blocks.append("falta presupuesto (--max-turns / --max-budget-usd)")
    if provider == "codex" and "-s" not in cmd:
        blocks.append("codex sin sandbox explicito")
    return blocks


def check_limits(task_id: str | None, role: str, log: Path, cfg: dict, chain: list[str], provider: str) -> list[str]:
    lim, blocks = cfg["limits"], []
    if provider in chain:
        blocks.append(f"ciclo de delegacion: {provider} ya esta en la cadena {chain}")
    if len(chain) >= lim["max_delegation_depth"]:
        blocks.append(f"profundidad de delegacion {len(chain)} >= {lim['max_delegation_depth']}: un trabajador delegado no re-delega")
    if task_id and role == "reviewer" and log.is_file():
        with log.open(encoding="utf-8") as fh:
            done = sum(1 for r in csv.DictReader(fh) if r.get("task_id") == task_id and r.get("rol") == "reviewer")
        if done >= lim["max_review_cycles"]:
            blocks.append(f"ciclos de revision agotados para {task_id}: {done}/{lim['max_review_cycles']}")
    return blocks


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
    ok = (bool(result) and not result.get("is_error", False)) or (not result and bool(usage))
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
        "resultado": str(result.get("result", "") or last_msg)[:200], "ok": ok,
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


def preflight(a, cfg: dict, which=shutil.which, git=git_info, env: dict | None = None) -> dict:
    chain = chain_from_env(env)
    prof, blocks = resolve_profile(a.profile, a.effort, a.reason, cfg)
    proj, pblocks = check_project(a.project, Path(a.cwd), a.add_dir, a.allow_external_dir, cfg, git=git)
    blocks += pblocks
    task = Path(a.task_file).read_text(encoding="utf-8") if a.task_file and Path(a.task_file).is_file() else ""
    signals = risk_signals(task) if task else []
    if signals and not a.approved_risk:
        blocks.append(f"riesgo critical en la tarea {signals}: requiere aprobacion humana (--approved-risk)")
    order = ([a.provider] if a.provider else []) + [p for p in prof["providers"] if p != a.provider]
    available = {p: bool(which(p)) for p in order}
    chosen = next((p for p in order if available[p]), None)
    cmd: list[str] = []
    if chosen is None:
        blocks.append(f"ningun proveedor disponible en {order}")
    else:
        cmd = build_command(chosen, prof, cfg, a.cwd, a.add_dir, a.mcp_config, a.allow_write)
        blocks += security_check(cmd, chosen, cfg)
        blocks += check_limits(a.task_id, a.role, Path(a.log) if a.log else Path(os.devnull), cfg, chain, chosen)
    return {
        "status": "BLOCKED" if blocks else "READY", "blocks": blocks, **proj,
        "profile": prof["name"], "provider_order": order, "providers_available": available,
        "provider": chosen, "fallback_used": bool(a.provider and chosen and chosen != a.provider),
        "model_planned": model_for(chosen, prof["effort"], cfg) if chosen else None,
        "model_effective": "NO_OBSERVADO (se lee del evento init al ejecutar)",
        "effort": prof["effort"], "tools_allowed": prof["tools"], "deny_rules": len(deny_list(prof, cfg)),
        "hooks": prof.get("hooks"),
        "budget": {"max_turns": prof["max_turns"], "max_budget_usd_nocional": prof["max_budget_usd"], **cfg["limits"]},
        "risk_signals": signals, "delegation_chain": chain, "command": cmd,
    }


def run_provider(cmd: list[str], provider: str, task: str, cwd: str, env: dict) -> subprocess.CompletedProcess:
    if provider == "agy":
        cmd, task = cmd + [task], ""
    return subprocess.run(cmd, input=task, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=cwd, env=env, shell=sys.platform == "win32")


def parser(cfg: dict) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", choices=sorted(cfg["profiles"]), default=cfg["default_profile"])
    ap.add_argument("--project", required=True)
    ap.add_argument("--task-file")
    ap.add_argument("--cwd", default=".")
    ap.add_argument("--add-dir", action="append", default=[])
    ap.add_argument("--allow-external-dir", action="store_true")
    ap.add_argument("--mcp-config", action="append", default=[])
    ap.add_argument("--provider", choices=["claude", "codex", "agy"])
    ap.add_argument("--effort")
    ap.add_argument("--reason")
    ap.add_argument("--approved-risk", action="store_true", help="El fundador aprobo el riesgo detectado.")
    ap.add_argument("--allow-write", action="store_true", help="Codex workspace-write / Agy accept-edits.")
    ap.add_argument("--task-id")
    ap.add_argument("--role", choices=["worker", "reviewer"], default="worker")
    ap.add_argument("--label", default="")
    ap.add_argument("--log")
    ap.add_argument("--raw-dir", help="Carpeta donde guardar la salida bruta de cada intento (evidencia).")
    ap.add_argument("--verify-cmd", help="Comprobacion determinista posterior; su exit code fija 'calidad'.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    cfg = load_config()
    a = parser(cfg).parse_args(argv)
    a.cwd = str(Path(a.cwd).resolve())
    report = preflight(a, cfg)
    if a.check or a.dry_run or report["status"] == "BLOCKED":
        if a.check:
            report.pop("command")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if report["status"] == "BLOCKED" else 0
    if not (a.task_file and a.log):
        print(json.dumps({"status": "BLOCKED", "blocks": ["ejecucion real exige --task-file y --log"]}))
        return 2
    task = Path(a.task_file).read_text(encoding="utf-8")
    chain = chain_from_env()
    prof, _ = resolve_profile(a.profile, a.effort, a.reason, cfg)
    rc, attempt = 1, 0
    for provider in [p for p in report["provider_order"] if report["providers_available"][p]]:
        cmd = build_command(provider, prof, cfg, a.cwd, a.add_dir, a.mcp_config, a.allow_write)
        if security_check(cmd, provider, cfg):  # el respaldo pasa los mismos controles
            continue
        env = {**os.environ, CHAIN_ENV: ",".join(chain + [provider])}
        for _ in range(cfg["limits"]["max_retries"] + 1):
            attempt += 1
            t0 = time.time()
            proc = run_provider(cmd, provider, task, a.cwd, env)
            stats = parse_stream(proc.stdout.splitlines())
            if a.raw_dir:
                Path(a.raw_dir).mkdir(parents=True, exist_ok=True)
                (Path(a.raw_dir) / f"{a.task_id or a.label or 'run'}-{attempt}-{provider}.jsonl").write_text(
                    proc.stdout, encoding="utf-8")
            stats["segundos"] = stats["segundos"] or round(time.time() - t0)
            ok = proc.returncode == 0 and stats["ok"]
            calidad = ""
            if ok and a.verify_cmd:
                v = subprocess.run(shlex.split(a.verify_cmd, posix=sys.platform != "win32"), cwd=a.cwd)
                calidad = "PASS" if v.returncode == 0 else "FAIL"
            row = {"fecha": time.strftime("%Y-%m-%d %H:%M"), "task_id": a.task_id or "", "etiqueta": a.label,
                   "rol": a.role, "intento": attempt, "perfil": a.profile, "proveedor": provider,
                   "modelo": stats["modelo_efectivo"] if stats["modelo_efectivo"] != "NO_OBSERVADO" else model_for(provider, prof["effort"], cfg) + " (planeado)",
                   "esfuerzo": prof["effort"], "estado": "OK" if ok else f"FALLO_rc{proc.returncode}",
                   "coordinacion": len(chain) + 1, "calidad": calidad, **stats}
            append_log(Path(a.log), row)
            print(json.dumps({k: row[k] for k in ("proveedor", "modelo", "intento", "estado", "turnos", "total", "calidad", "resultado")},
                             ensure_ascii=False))
            if ok:
                return 0
            rc = proc.returncode or 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
