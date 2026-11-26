"""Lanzador de sesiones por perfil (LEAN / STANDARD / ADVANCED) con registro de consumo.

Solo construye y ejecuta `claude -p`; no instala nada ni toca la configuracion global.
  LEAN      --safe-mode (sin MCP, skills, plugins, hooks, CLAUDE.md ni memoria) + reglas esenciales de team/profiles/lean.md.
  STANDARD  sesion normal con --strict-mcp-config: solo los MCP que se pasen con --mcp-config.
  ADVANCED  configuracion completa del usuario (Graphify, Council, Codex, Antigravity bajo demanda).

Uso: python scripts/lean_run.py --profile lean --label C2 --task-file tarea.txt --cwd carpeta \
        --add-dir entradas --log consumo.csv [--model claude-sonnet-5-5] [--effort medium] [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_PROMPT = ROOT / "team" / "profiles" / "lean.md"
DEFAULT_TOOLS = "Read,Write,Edit,Glob,Grep,Bash(python *)"
FIELDS = ["fecha", "etiqueta", "perfil", "modelo", "esfuerzo", "turnos", "segundos", "entrada", "cache_creada",
          "cache_leida", "salida", "total", "ponderado", "costo_nocional_usd", "herramientas", "mcp", "skills"]


def build_command(profile: str, model: str, effort: str, tools: str, add_dirs: list[str],
                  mcp_configs: list[str], max_turns: int = 12) -> list[str]:
    cmd = ["claude", "-p", "--model", model, "--effort", effort, "--no-session-persistence",
           "--max-turns", str(max_turns), "--permission-mode", "acceptEdits", "--allowedTools", tools,
           "--output-format", "stream-json", "--verbose"]
    if profile == "lean":
        cmd += ["--safe-mode", "--strict-mcp-config", "--disable-slash-commands",
                "--append-system-prompt-file", str(LEAN_PROMPT)]
    elif profile == "standard":
        cmd += ["--strict-mcp-config"]
        for cfg in mcp_configs:
            cmd += ["--mcp-config", cfg]
    elif profile != "advanced":
        raise ValueError(f"perfil desconocido: {profile}")
    for d in add_dirs:
        cmd += ["--add-dir", d]
    return cmd


def parse_stream(lines) -> dict:
    init, result = {}, {}
    for line in lines:
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            init = obj
        elif obj.get("type") == "result":
            result = obj
    u = result.get("usage", {})
    entrada, creada = u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0)
    leida, salida = u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0)
    return {
        "turnos": result.get("num_turns", 0), "segundos": round(result.get("duration_ms", 0) / 1000),
        "entrada": entrada, "cache_creada": creada, "cache_leida": leida, "salida": salida,
        "total": entrada + creada + leida + salida,
        "ponderado": round(entrada + creada * 1.25 + leida * 0.1 + salida * 5),
        "costo_nocional_usd": round(result.get("total_cost_usd", 0), 3),
        "herramientas": len(init.get("tools", [])), "mcp": len(init.get("mcp_servers", [])),
        "skills": len(init.get("skills", [])), "resultado": str(result.get("result", ""))[:200],
    }


def append_log(path: Path, row: dict) -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerow(row)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", choices=["lean", "standard", "advanced"], default="lean")
    ap.add_argument("--label", required=True)
    ap.add_argument("--task-file", required=True)
    ap.add_argument("--cwd", required=True)
    ap.add_argument("--add-dir", action="append", default=[])
    ap.add_argument("--mcp-config", action="append", default=[])
    ap.add_argument("--tools", default=DEFAULT_TOOLS)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--log", required=True)
    ap.add_argument("--dry-run", action="store_true", help="Imprime el comando sin ejecutarlo (no consume nada).")
    a = ap.parse_args()
    cmd = build_command(a.profile, a.model, a.effort, a.tools, a.add_dir, a.mcp_config, a.max_turns)
    if a.dry_run:
        print(" ".join(cmd))
        return 0
    task = Path(a.task_file).read_text(encoding="utf-8")
    t0 = time.time()
    proc = subprocess.run(cmd, input=task, capture_output=True, text=True, encoding="utf-8", cwd=a.cwd, shell=sys.platform == "win32")
    stats = parse_stream(proc.stdout.splitlines())
    stats["segundos"] = stats["segundos"] or round(time.time() - t0)
    row = {"fecha": time.strftime("%Y-%m-%d %H:%M"), "etiqueta": a.label, "perfil": a.profile,
           "modelo": a.model, "esfuerzo": a.effort, **stats}
    append_log(Path(a.log), row)
    print(json.dumps({k: row[k] for k in ("etiqueta", "perfil", "turnos", "segundos", "total", "ponderado", "resultado")}, ensure_ascii=False))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
