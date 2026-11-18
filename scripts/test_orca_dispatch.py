"""Pruebas aisladas del dispatcher: no requieren Orca, Claude ni credenciales."""
from __future__ import annotations

import importlib.util
import io
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("altiora_orca_dispatch", ROOT / "scripts" / "orca-dispatch.py")
assert SPEC is not None and SPEC.loader is not None
dispatcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dispatcher)


class OrcaRoutingSmokeTest(unittest.TestCase):
    def test_three_distinct_domains_have_agents_and_contracts(self):
        message = "Auditar estrategia financiera backend y automatización, branding copy landing y experiencia 3D WebGL GSAP"
        streams = dispatcher.classify_message(message)
        self.assertEqual(
            {s["domain"] for s in streams},
            {"strategy-finance-backend", "brand-copy-frontend", "immersive-3d-qa"},
        )
        self.assertEqual(len(streams), 3)
        self.assertEqual({s["preferred_ai"] for s in streams}, {"codex", "claude", "antigravity"})
        for stream in streams:
            self.assertEqual(stream["worktree_strategy"], "new-child")
            self.assertIn(stream["effort"], dispatcher.EFFORT_LEVELS)
            self.assertIn("Verificación requerida", stream["spec"])
            self.assertTrue(stream["skills"])
            self.assertTrue(stream["owned_paths"])

    def test_one_domain_requires_no_parallel_worktrees(self):
        streams = dispatcher.classify_message("Corregir copy de marca y propuesta")
        self.assertEqual(len(streams), 1)
        self.assertEqual(streams[0]["preferred_ai"], "claude")
        self.assertEqual(streams[0]["worktree_strategy"], "current")

    def test_execution_flag_is_blocked_without_explicit_switch(self):
        # Guard occurs BEFORE model invocation, Orca calls, or state writes.
        with patch.dict(os.environ, {"ALTIORA_DISPATCH_EXECUTE": ""}), \
             patch.object(sys, "argv", ["orca-dispatch.py", "--execute", "un cambio pequeño"]), \
             patch("sys.stderr", new_callable=io.StringIO) as stderr, \
             patch.object(dispatcher, "dispatch_to_orca", side_effect=AssertionError("never call")):
            self.assertEqual(dispatcher.main(), 2)
            self.assertIn("Modo solo plan", stderr.getvalue())

    def test_fallback_when_preferred_is_rate_limited(self):
        stream = {"preferred_ai": "codex", "orca_worker_agent": "codex"}
        blocked = {"codex": {"exhausted_until": "2099-01-01T00:00:00Z", "reason": "fixture"}}
        dispatcher.apply_availability(stream, blocked)
        self.assertEqual(stream["preferred_ai"], "claude")
        self.assertEqual(stream["rerouted_from"], "codex")

    def test_effort_risk_and_no_default_max(self):
        self.assertEqual(dispatcher.choose_effort("formatear texto", "brand-copy-frontend"), "low")
        self.assertEqual(dispatcher.choose_effort("implementar UI", "brand-copy-frontend"), "medium")
        self.assertEqual(dispatcher.choose_effort("auditar arquitectura", "brand-copy-frontend"), "high")
        self.assertEqual(dispatcher.choose_effort("seguridad de pagos", "strategy-finance-backend"), "xhigh")


if __name__ == "__main__":
    unittest.main()
