#!/usr/bin/env python3
"""Altiora isolated graph plan compiler. No network calls, installs or external execution."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "modular-graph-adapters.json"

def plan(job: dict, manifest: dict) -> dict:
    """Produce a minimal, permission-gated dispatch PLAN; never execute tools."""
    required = ("job_id", "intent", "client_id")
    if any(not isinstance(job.get(k), str) or not job[k].strip() for k in required):
        raise ValueError("job_id, intent, client_id are required")
    allowed = set(job.get("authorized_tools", []))
    if not all(isinstance(v, str) for v in allowed):
        raise ValueError("authorized_tools must be string list")
    context_missing = job.get("context_missing") is True
    nodes = []
    reasons = []
    def try_node(name, condition, permission):
        node = manifest["nodes"][name]
        if not condition:
            return
        if permission not in allowed:
            reasons.append(f"{name}: permission missing")
        elif not node.get("enabled", False):
            reasons.append(f"{name}: {node['status']}")
        else:
            nodes.append(name)
    intent = job["intent"].lower()
    try_node("palacio_mental", context_missing, "memory:read")
    try_node("playwright", any(t in intent for t in ("browser", "navegador", "e2e", "playwright", "prueba web")), "browser:execute")
    try_node("frontend_design", any(t in intent for t in ("frontend", "ui", "componente", "landing")), "frontend:design")
    try_node("claudered", any(t in intent for t in ("security review", "auditoría de seguridad", "pentest")), "security:review")
    # OmniRoute and Headroom are middleware; neither is a task node.
    gateway = "omniroute" if "models:route" in allowed and manifest["nodes"]["omniroute"]["enabled"] else "existing"
    compressor = "headroom" if "compress:context" in allowed and manifest["nodes"]["headroom"]["enabled"] and gateway != "omniroute" and job.get("large_payload") is True else "existing"
    return {
        "job_id": job["job_id"], "client_id": job["client_id"], "entrypoint": manifest["entrypoint"],
        "nodes": nodes, "model_gateway": gateway, "compressor": compressor,
        "status": "PLAN_ONLY", "not_executed": reasons
    }

def main():
    parser = argparse.ArgumentParser(description="Print a permission-gated graph plan; never run plugins")
    parser.add_argument("--job", required=True, help="Path to a local JSON job. Do not pass secrets")
    args = parser.parse_args()
    job = json.loads(Path(args.job).read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(json.dumps(plan(job, manifest), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
