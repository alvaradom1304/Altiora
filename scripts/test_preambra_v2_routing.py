"""Tests for PREAMBRA V2 decision policy. Does not invoke AI or Orca."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from preambra_v2_routing import decide_mode, make_handoffs, overlapping_paths, validate_contract

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "orca-dispatch.py"


def task(owner: str, *paths: str, **extra: object) -> dict:
    return {"preferred_ai": owner, "title": "Tarea verificable", "effort": "medium",
            "owned_paths": list(paths), **extra}


class AdaptiveRoutingV2Test(unittest.TestCase):
    def test_direct_mode_keeps_current_entrypoint(self):
        d = decide_mode("Formatear este texto", [task("claude", "docs/")])
        self.assertEqual(d["mode"], "A")
        self.assertEqual(d["lead_candidate"], "current")
        self.assertEqual(d["orca_policy"], "NOT_REQUIRED")
        handoff = make_handoffs("Formatear este texto", [task("claude", "docs/")], d)[0]
        self.assertEqual(handoff["owner"], "current")
        self.assertEqual(handoff["status"], "PLANNED")
        self.assertEqual(validate_contract(handoff), [])

    def test_builder_reviewer_for_substantial_task(self):
        d = decide_mode("Implementar una API para clientes", [task("codex", "src/api/")])
        self.assertEqual(d["mode"], "B")
        self.assertEqual(d["reviewer_candidate"], "claude")
        self.assertFalse(d["requires_human_approval"])

    def test_critical_requires_human_review(self):
        d = decide_mode("Auditar seguridad de pagos", [task("codex", "src/payments/")])
        self.assertEqual(d["mode"], "B")
        self.assertEqual(d["risk"], "critical")
        self.assertTrue(d["requires_human_approval"])

    def test_parallel_only_for_independent_non_overlapping(self):
        streams = [task("codex", "services/catalog/"), task("antigravity", "components/visual/")]
        d = decide_mode("Crear en paralelo módulos independientes de catálogo y 3D", streams)
        self.assertEqual(d["mode"], "C")
        self.assertTrue(d["parallel_safe"])
        self.assertEqual(d["path_collisions"], [])
        self.assertEqual(d["orca_policy"], "OPTIONAL_AFTER_RUNTIME_VERIFICATION")

    def test_parent_child_path_collision_prevents_parallel(self):
        streams = [task("claude", "components/"), task("antigravity", "components/3d/")]
        d = decide_mode("Diseñar componentes y 3D en paralelo", streams)
        self.assertEqual(d["mode"], "B")
        self.assertFalse(d["parallel_safe"])
        self.assertTrue(d["path_collisions"])

    def test_dependencies_prevent_parallel(self):
        streams = [task("codex", "src/api/"), task("claude", "src/ui/", depends_on=[1])]
        d = decide_mode("Crear API e interfaz en paralelo", streams)
        self.assertEqual(d["mode"], "B")
        self.assertTrue(d["has_dependencies"])

    def test_integral_mode_has_business_gate(self):
        d = decide_mode("Proyecto integral de cliente desde diagnóstico hasta lanzamiento",
                        [task("claude", "project/")])
        self.assertEqual(d["mode"], "D")
        self.assertTrue(d["requires_human_approval"])

    def test_contract_rejects_fake_done(self):
        s = [task("codex", "src/api/")]
        d = decide_mode("Implementar API", s)
        c = make_handoffs("Implementar API", s, d)[0]
        c["status"] = "DONE"
        self.assertTrue(any("evidence" in error for error in validate_contract(c)))
        self.assertTrue(any("checks" in error for error in validate_contract(c)))

    def test_unsafe_owned_path_rejected(self):
        with self.assertRaises(ValueError):
            overlapping_paths([task("codex", "../credentials")])

    def test_default_cli_is_cost_free_and_has_v2_metadata(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "--json", "Formatear texto"],
            cwd=ROOT, capture_output=True, text=True, timeout=20, check=False,
            encoding="utf-8", errors="replace",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["router"]["router"], "heuristic")
        self.assertEqual(data["policy_v2"]["mode"], "A")
        self.assertEqual(data["handoffs"][0]["model_observed"], "UNKNOWN")
        self.assertNotIn("orca_dispatch", data)

    def test_worker_launch_cannot_assume_worktrees_exist(self):
        env = dict(os.environ)
        env["ALTIORA_DISPATCH_EXECUTE"] = "1"
        result = subprocess.run(
            [sys.executable, str(CLI), "--router", "heuristic", "--launch-workers",
             "Crear estrategia backend y escena 3D WebGL en paralelo"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=20,
            check=False, encoding="utf-8", errors="replace",
        )
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("lanzamiento bloqueado", result.stderr)


if __name__ == "__main__":
    unittest.main()
