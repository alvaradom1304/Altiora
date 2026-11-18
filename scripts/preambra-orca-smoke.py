#!/usr/bin/env python3
"""PREAMBRA PMO-ORCA-001: no-cost, read-only routing and safety smoke test.

This program tests the existing dispatcher's heuristic mode; it never starts Orca,
calls Claude/Codex/Antigravity or changes tracked files. No installation required.
A PASS means ONLY that the plan/guard work, not that an external runtime is active.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPATCH = ROOT / "scripts" / "orca-dispatch.py"
TASKS = (
    ("Revisar el branding y copy comercial de PREAMBRA", "claude"),
    ("Auditar scripts Python y seguridad backend", "codex"),
    ("Crear una escena 3D con WebGL y GSAP", "antigravity"),
)


def plan(message: str) -> dict:
    env = dict(os.environ)
    env.pop("ALTIORA_DISPATCH_EXECUTE", None)
    proc = subprocess.run(
        [sys.executable, str(DISPATCH), "--router", "heuristic", "--json", message],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=20,
        check=False, encoding="utf-8", errors="replace",
    )
    if proc.returncode:
        raise AssertionError(f"Router failed (code {proc.returncode}): {proc.stderr[:450]}")
    return json.loads(proc.stdout)


def guard_blocks_execution() -> bool:
    env = dict(os.environ)
    env.pop("ALTIORA_DISPATCH_EXECUTE", None)
    proc = subprocess.run(
        [sys.executable, str(DISPATCH), "--router", "heuristic",
         "--execute", "Revisar branding PREAMBRA"],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=20,
        check=False, encoding="utf-8", errors="replace",
    )
    return proc.returncode == 2 and "Modo solo plan" in proc.stderr


def main() -> int:
    results = []
    failed = False
    for text, expected in TASKS:
        try:
            data = plan(text)
            agents = [s["preferred_ai"] for s in data["streams"]]
            ok = expected in agents and "orca_dispatch" not in data and not data.get("parallel_worktrees")
            results.append({"test": "route", "message": text, "expected": expected,
                            "actual": agents, "pass": ok})
            failed |= not ok
        except (AssertionError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
            results.append({"test": "route", "expected": expected,
                            "pass": False, "error": str(exc)})
            failed = True
    try:
        protected = guard_blocks_execution()
    except (OSError, subprocess.TimeoutExpired) as exc:
        protected = False
        results.append({"test": "execution_guard", "pass": False, "error": str(exc)})
    else:
        results.append({"test": "execution_guard", "pass": protected})
    failed |= not protected

    # This is a real task *plan* and structured handoff, NOT an executed agent task.
    first = {
        "job_id": "PMO-ORCA-001",
        "brand": "PREAMBRA",
        "goal": "Verify multi-AI routing then validate one read-only Orca agent handoff",
        "agent": "claude",
        "model_observed": "UNKNOWN",
        "effort": "medium",
        "inputs": ["AGENTS.md", "brand/preambra/BRAND-PLATFORM.md"],
        "owned_paths": [],
        "dependencies": [],
        "budget_limit": "no external model invocation from this smoke",
        "acceptance": "route tests pass; local Orca execution independently confirmed",
        "artifacts": [],
        "checks": results,
        "status": "ROUTING_TESTED_OR_NOT_RUN" if not failed else "BLOCKED_TEST_FAILURE",
        "evidence": "stdout of this command (local); no live Orca evidence",
        "next_action": "On user's PC run orca status --json, then an authorized read-only worker",
    }
    payload = {"ok": not failed, "kind": "OFFLINE_ROUTING_SMOKE",
               "executed_agents": 0, "orca_runtime_tested": False,
               "results": results, "first_task": first}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
