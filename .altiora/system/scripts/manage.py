"""Install, diagnose, validate handoffs and roll back Altiora Agent System. Python 3.11+."""
import argparse
import copy
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.3.0"
ROOT = Path(__file__).resolve().parents[1]
START = "<!-- ALTIORA_AGENT_SYSTEM_START -->"
END = "<!-- ALTIORA_AGENT_SYSTEM_END -->"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def load(path, default=None):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else copy.deepcopy(default)


def safe(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"Ruta fuera del proyecto: {relative}")
    path = root / rel
    current = path
    while current != root:
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError(f"No se escriben enlaces o junctions: {relative}")
        current = current.parent
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Ruta resuelta fuera del proyecto: {relative}")
    return path


def wrapper(existing):
    block = (f"{START}\n## Altiora Agent System {VERSION}\n"
             "Leer `.altiora/system/core/constitution.md` al empezar trabajo en este proyecto. "
             "Usar `.altiora/project.json` como contexto y `.altiora/handoff.json` si existe, "
             "contrastando siempre con el encargo vigente. Seleccionar skills por descripcion. "
             "Las instrucciones propias del proyecto y las del usuario siguen aplicando.\n"
             f"{END}")
    text = existing.decode("utf-8-sig") if existing else ""
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError("Bloque Altiora ambiguo o incompleto; conservar y revisar antes de instalar")
    if START in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip() + ("\n\n" if text.strip() else "") + block + "\n"
    return text.encode("utf-8")


def command(target, runtime, event):
    if runtime == "antigravity":
        # Portable: agy ejecuta el hook con cwd = carpeta de .agents/hooks.json (sonda agy 1.4.12, 2026-11-28),
        # asi que el proyecto es '..' y el comando no depende del checkout ni del interprete de esta maquina.
        return f"python ../.altiora/system/scripts/guard.py --runtime antigravity --project .. --event {event}"
    parts = [str(Path(sys.executable).resolve()), str(target / ".altiora/system/scripts/guard.py"),
             "--runtime", runtime, "--project", str(target), "--event", event]
    # Hook command is executed by the client's shell. Use forward slashes on Windows
    # so double-quoted paths also work in Git Bash. Reject expansion metacharacters.
    if any(any(c in x for c in '\n\r`$%"!') for x in parts):
        raise ValueError("Ruta de hook contiene caracteres de expansion shell no admitidos")
    if os.name == "nt":
        def _win_quote(arg: str) -> str:
            s = arg.replace("\\", "/")
            return f'"{s}"' if (" " in s or "\t" in s) else s
        return " ".join(_win_quote(x) for x in parts)
    return shlex.join(parts)


def hook_config(target, runtime, existing):
    cfg = copy.deepcopy(existing or {})
    if not isinstance(cfg, dict):
        raise ValueError("Configuracion de hooks debe ser un objeto")
    events = {}
    for event in ["SessionStart", "PreToolUse"]:
        handler = {"type": "command", "command": command(target, runtime, event), "timeout": 10}
        if runtime == "antigravity" and event == "SessionStart":
            events[event] = [handler]
        else:
            events[event] = [{"matcher": "*", "hooks": [handler]}]
    if runtime == "antigravity":
        if "altiora-agent-system" in cfg and cfg["altiora-agent-system"] != events:
            raise ValueError("Hook Antigravity homonimo diferente; no se sustituye")
        cfg["altiora-agent-system"] = events
    else:
        hooks = cfg.setdefault("hooks", {})
        if not isinstance(hooks, dict):
            raise ValueError("hooks debe ser objeto")
        for event, groups in events.items():
            prior = hooks.setdefault(event, [])
            if not isinstance(prior, list):
                raise ValueError("Evento de hook debe ser lista")
            # Preserve existing handlers and avoid adding a duplicate on reinstall.
            for group in groups:
                if group not in prior:
                    if any(".altiora/system/scripts/guard.py" in str(x).replace("\\", "/") for x in prior):
                        raise ValueError("Hook Altiora existente con ruta distinta; revisar antes de actualizar")
                    prior.append(group)
    return cfg


LEGACY_ROLE_TOOLS = {"research": "Read, Glob, Grep", "review": "Read, Glob, Grep", "experience": "Read, Glob, Grep"}


def role_metadata(role):
    """Return (description, tools, text) from a role file.

    Optional front matter declares `description` and `tools` (`inherit` omits the
    Claude tools line). Without it, keep the legacy defaults and use the first
    paragraph, shortened at a word boundary instead of mid-word.
    """
    text = role.read_text(encoding="utf-8")
    fields = {}
    match = re.match(r"---\r?\n(.*?)\r?\n---\r?\n+", text, re.S)
    if match:
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep and key.strip() in ("description", "tools"):
                fields[key.strip()] = value.strip().strip('"')
        text = text[match.end():]
    desc = fields.get("description")
    if not desc:
        prose = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
        paragraph = next((p.strip() for p in prose.split("\n\n") if p.strip()), "")
        desc = " ".join(paragraph.split())
        if len(desc) > 1024:
            desc = desc[:1024].rsplit(" ", 1)[0]
    suffix = role.stem.rsplit("-", 1)[-1]
    tools = fields.get("tools") or LEGACY_ROLE_TOOLS.get(suffix, "Read, Glob, Grep, Write, Edit, Bash")
    return desc, tools, text


def plan_install(target, library=None, names=()):
    changes, reused, current = {}, [], {}
    receipt = load(safe(target, ".altiora/installation.json"), {"managed": {}})
    def put(rel, data, preserve=False):
        path = safe(target, rel)
        old = path.read_bytes() if path.exists() else None
        if old == data:
            # Already matches the kit payload: record it so doctor can verify it.
            current[rel] = digest(data)
            return
        if preserve and old is not None:
            reused.append(rel)
            return
        previous = receipt["managed"].get(rel)
        if old is not None and previous != digest(old):
            raise ValueError(f"Archivo local diferente no se sobrescribe: {rel}")
        changes[rel] = data

    # Copy only operational payload, not tests or local audit reports.
    for folder in ["core", "contracts", "docs", "roles", "scripts", "skills"]:
        for source in sorted((ROOT / folder).rglob("*")):
            if source.is_symlink():
                raise ValueError(f"Fuente enlazada no admitida: {source}")
            if source.is_file() and "__pycache__" not in source.parts:
                put(".altiora/system/" + source.relative_to(ROOT).as_posix(), source.read_bytes())
    for filename, source in [("project.json", "project.json"), ("policy.json", "policy.json")]:
        put(".altiora/" + filename, (ROOT / "core" / source).read_bytes(), preserve=True)
    for name in ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]:
        path = safe(target, name)
        old = path.read_bytes() if path.exists() else None
        new = wrapper(old)
        if old != new:
            changes[name] = new
    sources = list((ROOT / "skills").iterdir())
    if names and library is None:
        raise ValueError("--skill requiere --library")
    for name in names:
        if not re.fullmatch(r"[a-z0-9-]+", name):
            raise ValueError(f"Nombre de skill invalido: {name}")
        source = library / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Skill no encontrada: {source}")
        sources.append(source)
    for source in sources:
        for destination in [".agents/skills", ".claude/skills"]:
            # Preserve entire existing skill if any file differs and is not managed.
            relative_base = f"{destination}/{source.name}"
            files = [p for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
            if any(p.is_symlink() for p in source.rglob("*")):
                raise ValueError(f"Skill con enlaces; revisar antes de importar: {source.name}")
            conflict = False
            for p in files:
                rel = relative_base + "/" + p.relative_to(source).as_posix()
                dest = safe(target, rel)
                if dest.exists() and dest.read_bytes() != p.read_bytes() and receipt["managed"].get(rel) != digest(dest.read_bytes()):
                    conflict = True
            if conflict:
                reused.append(relative_base)
                continue
            for p in files:
                put(relative_base + "/" + p.relative_to(source).as_posix(), p.read_bytes())
    for role in sorted((ROOT / "roles").glob("*.md")):
        desc, tools, text = role_metadata(role)
        body = text + ("\nRecibir objetivo, archivos propios, herramientas y criterio de aceptacion. "
                "Respetar instrucciones aplicables del proyecto. No iniciar otros agentes por defecto. "
                "Devolver resultado, evidencia y limites segun .altiora/system/contracts/result.schema.json.\n")
        # TOML strings use JSON-compatible escapes; no fixed model or permissions.
        toml = f"name = {json.dumps(role.stem)}\ndescription = {json.dumps(desc)}\ndeveloper_instructions = {json.dumps(body, ensure_ascii=True)}\n"
        put(f".codex/agents/{role.stem}.toml", toml.encode(), preserve=True)
        tools_line = "" if tools == "inherit" else f"tools: {tools}\n"
        md = f"---\nname: {role.stem}\ndescription: {json.dumps(desc, ensure_ascii=False)}\n{tools_line}---\n\n{body}"
        put(f".claude/agents/{role.stem}.md", md.encode("utf-8"), preserve=True)
    for runtime, rel in [("codex", ".codex/hooks.json"), ("claude", ".claude/settings.json"), ("antigravity", ".agents/hooks.json")]:
        path = safe(target, rel)
        old = path.read_bytes() if path.exists() else None
        new = encoded(hook_config(target, runtime, load(path, {})))
        if old != new:
            changes[rel] = new
    managed = receipt["managed"].copy()
    managed.update(current)
    managed.update({rel: digest(data) for rel, data in changes.items()})
    # User-editable context and settings are not treated as immutable payload.
    for rel in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".altiora/project.json", ".altiora/policy.json",
                ".codex/hooks.json", ".claude/settings.json", ".agents/hooks.json"]:
        managed.pop(rel, None)
    data = encoded({"version": VERSION, "managed": managed})
    if not safe(target, ".altiora/installation.json").exists() or safe(target, ".altiora/installation.json").read_bytes() != data:
        changes[".altiora/installation.json"] = data
    return changes, reused


def apply(target, changes):
    if not changes:
        return None
    tx = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    backup = safe(target, ".altiora/backups/" + tx)
    originals = {rel: safe(target, rel).read_bytes() if safe(target, rel).exists() else None for rel in changes}
    backup.mkdir(parents=True)
    record = {"id": tx, "files": {}}
    for index, (rel, data) in enumerate(changes.items()):
        old = originals[rel]
        key = str(index) + ".bak" if old is not None else None
        if key:
            (backup / key).write_bytes(old)
        record["files"][rel] = {"backup": key, "installed_hash": digest(data)}
    (backup / "transaction.json").write_bytes(encoded(record))
    written = []
    try:
        for rel, data in changes.items():
            path = safe(target, rel)
            if (path.read_bytes() if path.exists() else None) != originals[rel]:
                raise ValueError(f"Archivo cambio durante instalacion: {rel}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            written.append(rel)
    except Exception:
        for rel in reversed(written):
            path = safe(target, rel)
            if originals[rel] is None:
                path.unlink()
            else:
                path.write_bytes(originals[rel])
        raise
    return tx


def rollback(target, tx, do_apply):
    if not re.fullmatch(r"[0-9TZ-]+[a-f0-9]{8}", tx):
        raise ValueError("Identificador de transaccion invalido")
    folder = safe(target, ".altiora/backups/" + tx)
    record = load(folder / "transaction.json")
    if not isinstance(record, dict):
        raise ValueError("Transaccion no encontrada")
    restores = {}
    for rel, info in record["files"].items():
        path = safe(target, rel)
        if not path.exists() or digest(path.read_bytes()) != info["installed_hash"]:
            raise ValueError(f"Rollback detenido: hubo cambios posteriores en {rel}")
        restores[rel] = safe(folder, info["backup"]).read_bytes() if info["backup"] else None
    if do_apply:
        for rel, data in restores.items():
            path = safe(target, rel)
            if data is None:
                path.unlink()
            else:
                path.write_bytes(data)
    return {"mode": "applied" if do_apply else "preview", "files": len(restores)}


def validate(value, schema, label="$"):
    """Validate the JSON Schema subset used by this kit; not a general schema engine."""
    errors = []
    types = {"object": dict, "array": list, "string": str, "null": type(None)}
    wanted = schema.get("type")
    if wanted:
        choices = wanted if isinstance(wanted, list) else [wanted]
        if not any(isinstance(value, types[t]) for t in choices):
            return [f"{label}: tipo incorrecto"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{label}: valor constante incorrecto")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{label}: valor no permitido")
    if isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0):
            errors.append(f"{label}: texto vacio")
        if schema.get("format") == "date-time":
            try:
                stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    raise ValueError()
            except ValueError:
                errors.append(f"{label}: fecha ISO con zona requerida")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{label}.{key}: requerido")
        props = schema.get("properties", {})
        for key, item in value.items():
            if key in props:
                errors += validate(item, props[key], label + "." + key)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{label}.{key}: campo desconocido")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{label}: faltan elementos")
        for i, item in enumerate(value):
            errors += validate(item, schema.get("items", {}), f"{label}[{i}]")
    return errors


def handoff_check(target):
    path = safe(target, ".altiora/handoff.json")
    if not path.exists():
        return ["No existe .altiora/handoff.json"]
    value = load(path)
    errors = validate(value, load(ROOT / "contracts/handoff.schema.json"))
    if errors:
        return errors
    for test in value["tests"]:
        if test["status"] in ["passed", "failed"] and (not test["evidence"].strip() or test["executed_at"] is None):
            errors.append("Prueba ejecutada requiere evidencia y fecha")
        if test["status"] == "not_run" and test["executed_at"] is not None:
            errors.append("Prueba no ejecutada debe tener executed_at null")
    if value["status"] == "complete" and (value["pending"] or any(t["status"] == "failed" for t in value["tests"])):
        errors.append("Tarea complete contiene pendientes o pruebas fallidas")
    for rel in value["changed_files"]:
        try:
            safe(target, rel)
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def plan_adopt(target, paths):
    """Accept reviewed local edits of managed files by recording their current hash."""
    receipt = load(safe(target, ".altiora/installation.json"))
    if not isinstance(receipt, dict):
        raise ValueError("Sistema no instalado")
    managed, adopted = receipt["managed"].copy(), {}
    for rel in paths:
        rel = Path(rel).as_posix()
        if rel not in managed:
            raise ValueError(f"No es un archivo gestionado: {rel}")
        path = safe(target, rel)
        if not path.is_file():
            raise ValueError(f"Archivo gestionado ausente: {rel}")
        new = digest(path.read_bytes())
        if new != managed[rel]:
            adopted[rel] = {"previous": managed[rel], "current": new}
            managed[rel] = new
    changes = {}
    if adopted:
        changes[".altiora/installation.json"] = encoded({**receipt, "managed": managed})
    return changes, adopted


def doctor(target):
    receipt = load(safe(target, ".altiora/installation.json"))
    errors = []
    if not isinstance(receipt, dict):
        return {"status": "FAILED", "errors": ["Sistema no instalado"], "live_runtime": "NOT_TESTED"}
    for rel, expected in receipt["managed"].items():
        path = safe(target, rel)
        if not path.exists() or digest(path.read_bytes()) != expected:
            errors.append("Falta o cambio: " + rel)
    for name in ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]:
        text = safe(target, name).read_text(encoding="utf-8-sig") if safe(target, name).exists() else ""
        if text.count(START) != 1 or text.count(END) != 1:
            errors.append("Adaptador incompleto: " + name)
    for runtime, rel in [("codex", ".codex/hooks.json"), ("claude", ".claude/settings.json"), ("antigravity", ".agents/hooks.json")]:
        cfg = load(safe(target, rel), {})
        holder = cfg.get("altiora-agent-system", {}) if runtime == "antigravity" else cfg.get("hooks", {})
        for event in ["SessionStart", "PreToolUse"]:
            if command(target, runtime, event) not in json.dumps(holder):
                # json.dumps escapes quotes, so inspect handler values instead.
                groups = holder.get(event, [])
                handlers = groups if runtime == "antigravity" and event == "SessionStart" else [h for g in groups for h in g.get("hooks", [])]
                if not any(h.get("command") == command(target, runtime, event) for h in handlers):
                    errors.append(f"Hook ausente: {runtime}/{event}")
    for name in ["project", "policy"]:
        value = load(safe(target, f".altiora/{name}.json"))
        if not isinstance(value, dict):
            errors.append("Contexto o politica invalida: " + name)
    return {"status": "PASSED" if not errors else "FAILED", "version": receipt["version"],
            "managed_files": len(receipt["managed"]), "errors": errors, "live_runtime": "NOT_TESTED",
            "note": "Diagnostico estructural; revisar descubrimiento y confianza en cada cliente."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    for action in ["install", "doctor", "rollback", "handoff-check", "adopt"]:
        item = sub.add_parser(action)
        item.add_argument("--target", type=Path, required=True)
        if action in ["install", "rollback", "adopt"]:
            item.add_argument("--apply", action="store_true", help="Escribir; sin esta opcion solo muestra el plan")
        if action == "adopt":
            item.add_argument("--path", action="append", required=True,
                              help="Archivo gestionado, relativo al proyecto, cuya edicion local ya se reviso")
        if action == "install":
            item.add_argument("--library", type=Path, help="Biblioteca local opcional; importa solo --skill seleccionadas")
            item.add_argument("--skill", action="append", default=[])
        if action == "rollback":
            item.add_argument("--transaction", required=True)
    a = p.parse_args()
    target = a.target.resolve()
    try:
        if a.action == "install":
            if not target.is_dir():
                raise ValueError("El proyecto destino debe existir")
            changes, reused = plan_install(target, a.library, a.skill)
            tx = apply(target, changes) if a.apply else None
            result = {"mode": "applied" if a.apply else "preview", "target": str(target),
                      "changed_files": list(changes), "preserved_existing": reused, "transaction": tx}
        elif a.action == "adopt":
            changes, adopted = plan_adopt(target, a.path)
            tx = apply(target, changes) if a.apply else None
            result = {"mode": "applied" if a.apply else "preview", "adopted": adopted, "transaction": tx}
        elif a.action == "rollback":
            result = rollback(target, a.transaction, a.apply)
        elif a.action == "doctor":
            result = doctor(target)
        else:
            errors = handoff_check(target)
            result = {"status": "FAILED" if errors else "PASSED", "errors": errors}
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 1 if result.get("status") == "FAILED" else 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
