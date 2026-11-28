"""Mide una sesion interactiva de Claude Code a partir de su transcript JSONL y la anota en el CSV del lanzador.

Las sesiones interactivas (unico modo en que existe Code Mode) no emiten stream-json; el transcript que Claude Code
guarda en ~/.claude/projects/<proyecto>/<sesion>.jsonl si trae usage por mensaje, modelo efectivo y marcas de tiempo.
Solo lee: no ejecuta nada, no usa red y escribe una fila con lean_run.append_log (mismas columnas que la delegacion).

Uso: python scripts/transcript_usage.py --transcript <ruta.jsonl> --log consumo.csv --task-id CM-A --label sin-code-mode
     [--calidad PASS|FAIL] [--json]
"""
import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location("lean_run", Path(__file__).resolve().parent / "lean_run.py")
lean = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(lean)


def _ts(value: str | None) -> datetime | None:
    try:
        t = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)  # mezclar con/sin zona daba TypeError (REV-CM-01)


def measure(lines) -> dict:
    """Suma usage una vez por mensaje (los bloques de un mismo mensaje repiten id), cuenta herramientas y errores."""
    seen, usage, tools, models, stamps = set(), dict.fromkeys(("entrada", "cache_creada", "cache_leida", "salida"), 0), {}, set(), []
    errores, turnos = 0, 0
    for line in lines:
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if not isinstance(obj, dict) or obj.get("isSidechain"):
            continue  # los subagentes se miden aparte
        msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
        if obj.get("type") in ("user", "assistant") and (t := _ts(obj.get("timestamp"))):
            stamps.append(t)
        content = msg.get("content") if isinstance(msg.get("content"), list) else []
        if obj.get("type") == "user":
            errores += sum(1 for b in content if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"))
            continue
        if obj.get("type") != "assistant":
            continue
        for b in content:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                tools[b.get("name", "?")] = tools.get(b.get("name", "?"), 0) + 1
        key = msg.get("id") or obj.get("requestId") or obj.get("uuid")
        u = msg.get("usage")
        if key in seen or not isinstance(u, dict) or msg.get("model") == "<synthetic>":  # mensajes locales, sin API
            continue
        seen.add(key)
        turnos += 1
        if msg.get("model"):
            models.add(msg["model"])
        usage["entrada"] += u.get("input_tokens", 0)
        usage["cache_creada"] += u.get("cache_creation_input_tokens", 0)
        usage["cache_leida"] += u.get("cache_read_input_tokens", 0)
        usage["salida"] += u.get("output_tokens", 0)  # incluye razonamiento (output_tokens_details es desglose)
    total = sum(usage.values())
    return {**usage, "total": total, "turnos": turnos,
            "ponderado": round(usage["entrada"] + usage["cache_creada"] * 1.25 + usage["cache_leida"] * 0.1 + usage["salida"] * 5),
            "segundos": round((max(stamps) - min(stamps)).total_seconds()) if len(stamps) > 1 else 0,
            "modelo_efectivo": ",".join(sorted(models)) or "NO_OBSERVADO", "herramientas_usadas": tools,
            "llamadas_repl": tools.get("REPL", 0), "llamadas_mcp": sum(v for k, v in tools.items() if k.startswith("mcp__")),
            "errores_herramienta": errores}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--log")
    ap.add_argument("--task-id", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--calidad", choices=["PASS", "FAIL", ""], default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not lean.valid_task_id(a.task_id):
        print(json.dumps({"status": "BLOCKED", "blocks": [f"--task-id invalido: {a.task_id!r}"]}))
        return 2
    path = Path(a.transcript)
    if not path.is_file() or path.suffix != ".jsonl":
        print(json.dumps({"status": "BLOCKED", "blocks": [f"transcript inexistente o no .jsonl: {path}"]}))
        return 2
    with path.open(encoding="utf-8") as fh:
        m = measure(fh)
    if a.log:
        lean.append_log(Path(a.log), {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "task_id": a.task_id, "etiqueta": a.label,
            "rol": "worker", "intento": 1, "perfil": "interactivo", "proveedor": "claude", "modelo": m["modelo_efectivo"],
            "esfuerzo": "", "estado": "MEDIDO", "coordinacion": 1, "calidad": a.calidad, "costo_nocional_usd": 0,
            "costo_real": "NO_OBSERVADO", "cuota": "NO_OBSERVADA",
            "motivo": f"repl={m['llamadas_repl']} mcp={m['llamadas_mcp']} errores={m['errores_herramienta']}",
            **{k: m[k] for k in ("turnos", "segundos", "entrada", "cache_creada", "cache_leida", "salida", "total", "ponderado")}})
    print(json.dumps(m, ensure_ascii=False, indent=2 if a.json else None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
