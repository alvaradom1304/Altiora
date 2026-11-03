#!/usr/bin/env python3
"""Altiora isolated graph plan compiler. No network calls, installs or external execution."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "modular-graph-adapters.json"

def probe_omniroute(endpoint: str) -> bool:
    """A limited, no-auth health check on loopback. Never send user prompts or keys."""
    if endpoint != "http://127.0.0.1:20128/v1/models":
        return False
    try:
        with urlopen(Request(endpoint, headers={"Accept": "application/json"}), timeout=2) as response:
            if response.status != 200:
                return False
            body = response.read(65536)
            models = json.loads(body)
            return isinstance(models, dict) and isinstance(models.get("data"), list)
    except (URLError, HTTPError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        return False


def plan(job: dict, manifest: dict, *, gateway_healthy: bool = False) -> dict:
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
    omni = manifest["nodes"]["omniroute"]
    gateway = "omniroute" if "models:route" in allowed and omni["enabled"] and gateway_healthy else "existing"
    if "models:route" in allowed and omni["enabled"] and not gateway_healthy:
        reasons.append("omniroute: no verified local gateway; using existing model routing")
    compressor = "headroom" if "compress:context" in allowed and manifest["nodes"]["headroom"]["enabled"] and gateway != "omniroute" and job.get("large_payload") is True else "existing"
    return {
        "job_id": job["job_id"], "client_id": job["client_id"], "entrypoint": manifest["entrypoint"],
        "nodes": nodes, "model_gateway": gateway, "compressor": compressor,
        "status": "PLAN_ONLY", "not_executed": reasons
    }

def main():
    parser = argparse.ArgumentParser(description="Print a permission-gated graph plan; never run plugins")
    parser.add_argument("--job", required=True, help="Path to a local JSON job. Do not pass secrets")
    parser.add_argument("--probe", action="store_true", help="Probe only fixed local OmniRoute /v1/models endpoint")
    args = parser.parse_args()
    job = json.loads(Path(args.job).read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    healthy = probe_omniroute(manifest["nodes"]["omniroute"]["endpoint"]) if args.probe else False
    print(json.dumps(plan(job, manifest, gateway_healthy=healthy), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
