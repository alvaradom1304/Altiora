import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("graph_plan", ROOT / "scripts" / "modular_graph_plan.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
MANIFEST = json.loads((ROOT / "config" / "modular-graph-adapters.json").read_text(encoding="utf-8"))
BASE = {"job_id": "T-001", "client_id": "client-a", "intent": "landing", "authorized_tools": ["frontend:design"]}

class ModularGraphTests(unittest.TestCase):
    def test_frontend_reuses_local_skill(self):
        result = module.plan(BASE, MANIFEST)
        self.assertEqual(result["nodes"], ["frontend_design"])
        self.assertEqual(result["model_gateway"], "existing")
    def test_memory_not_requested_by_default(self):
        self.assertNotIn("palacio_mental", module.plan(BASE, MANIFEST)["nodes"])
    def test_history_requires_consent_and_enabled_runtime(self):
        a = dict(BASE, context_missing=True, authorized_tools=["memory:read"])
        result = module.plan(a, MANIFEST)
        self.assertNotIn("palacio_mental", result["nodes"])
        self.assertTrue(any("NOT_CONNECTED" in x for x in result["not_executed"]))
    def test_browser_disabled_even_when_authorized(self):
        a = dict(BASE, intent="prueba web", authorized_tools=["browser:execute"])
        self.assertEqual(module.plan(a, MANIFEST)["nodes"], [])
    def test_no_double_compression(self):
        m = json.loads(json.dumps(MANIFEST))
        m["nodes"]["headroom"]["enabled"] = True
        m["nodes"]["omniroute"]["enabled"] = True
        a = dict(BASE, authorized_tools=["models:route", "compress:context"], large_payload=True)
        result = module.plan(a, m, gateway_healthy=True)
        self.assertEqual(result["model_gateway"], "omniroute")
        self.assertEqual(result["compressor"], "existing")
    def test_omniroute_armed_but_fails_closed(self):
        a = dict(BASE, authorized_tools=["models:route"])
        result = module.plan(a, MANIFEST)
        self.assertEqual(result["model_gateway"], "existing")
        self.assertTrue(any("no verified local gateway" in x for x in result["not_executed"]))

    def test_omniroute_routes_when_healthy_and_authorized(self):
        a = dict(BASE, authorized_tools=["models:route"])
        self.assertEqual(module.plan(a, MANIFEST, gateway_healthy=True)["model_gateway"], "omniroute")

    def test_gateway_requires_permission(self):
        self.assertEqual(module.plan(BASE, MANIFEST, gateway_healthy=True)["model_gateway"], "existing")

    def test_probe_blocks_non_loopback(self):
        self.assertFalse(module.probe_omniroute("https://example.org/v1/models"))

    def test_missing_scope_rejected(self):
        with self.assertRaises(ValueError):
            module.plan({"job_id": "X", "intent": "UI"}, MANIFEST)

if __name__ == "__main__":
    unittest.main()
