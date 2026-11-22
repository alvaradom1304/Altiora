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

    def test_reviewer_skips_unavailable_ai(self):
        d = decide_mode("Implementar una API para clientes", [task("claude", "src/api/")],
                        unavailable=["codex"])
        self.assertEqual(d["mode"], "B")
        self.assertEqual(d["reviewer_candidate"], "antigravity")
        self.assertEqual(d["unavailable_ais"], ["codex"])
        self.assertFalse(d["requires_human_approval"])
        handoff = make_handoffs("Implementar una API para clientes", [task("claude", "src/api/")], d)[0]
        self.assertEqual(handoff["reviewer"], "antigravity")

    def test_default_reviewer_unchanged_without_unavailable_list(self):
        d = decide_mode("Implementar una API para clientes", [task("claude", "src/api/")])
        self.assertEqual(d["reviewer_candidate"], "codex")
        self.assertEqual(d["unavailable_ais"], [])

    def test_no_reviewer_left_requires_human_review(self):
        d = decide_mode("Implementar una API para clientes", [task("claude", "src/api/")],
                        unavailable=["codex", "antigravity"])
        self.assertIsNone(d["reviewer_candidate"])
        self.assertTrue(d["requires_human_approval"])
        self.assertTrue(any("human review" in w for w in d["warnings"]))

    def test_every_reviewed_handoff_gets_an_independent_reviewer(self):
        # Regression: in D, the stream owned by the run-level reviewer got reviewer=None silently.
        streams = [task("claude", "docs/strategy/"), task("codex", "scripts/"),
                   task("antigravity", "experiments/3d/")]
        msg = "Proyecto integral: estrategia, backend y escena 3D"
        d = decide_mode(msg, streams, entrypoint="claude")
        self.assertEqual(d["mode"], "D")
        for handoff in make_handoffs(msg, streams, d):
            self.assertIsNotNone(handoff["reviewer"], handoff["owner"])
            self.assertNotEqual(handoff["reviewer"], handoff["owner"])
            self.assertEqual(validate_contract(handoff), [])

    def test_handoff_without_any_reviewer_flags_human_review(self):
        streams = [task("claude", "docs/"), task("codex", "scripts/")]
        msg = "Implementar API y documentarla"
        d = decide_mode(msg, streams, entrypoint="claude", unavailable=["antigravity"])
        handoffs = make_handoffs(msg, streams, d)
        self.assertEqual([h["reviewer"] for h in handoffs], ["codex", "claude"])
        d = decide_mode(msg, streams, entrypoint="claude", unavailable=["codex", "antigravity"])
        handoffs = make_handoffs(msg, streams, d)
        codex = [h for h in handoffs if h["owner"] == "codex"][0]
        self.assertEqual(codex["reviewer"], "claude")
        claude = [h for h in handoffs if h["owner"] == "claude"][0]
        self.assertIsNone(claude["reviewer"])
        self.assertTrue(any("human review" in r for r in claude["risks"]))
        done = dict(claude, status="DONE", evidence=["log"], checks=["npm run check"])
        self.assertIn("DONE requires an independent reviewer or recorded human_review",
                      validate_contract(done))
        self.assertEqual(validate_contract(dict(done, human_review="humano/qa 2026-11-22")), [])

    def test_unavailable_lead_is_warned(self):
        d = decide_mode("Implementar una API para clientes", [task("codex", "src/api/")],
                        unavailable=["codex"])
        self.assertEqual(d["reviewer_candidate"], "claude")
        self.assertTrue(any("marked unavailable" in w for w in d["warnings"]))

    def test_unknown_unavailable_ai_rejected(self):
        with self.assertRaises(ValueError):
            decide_mode("Implementar API", [task("codex", "src/api/")], unavailable=["gpt-x"])

    def test_cli_unavailable_flag_and_env(self):
        env = dict(os.environ)
        env["PREAMBRA_UNAVAILABLE_AIS"] = "codex"
        result = subprocess.run(
            [sys.executable, str(CLI), "--json", "--entrypoint", "claude", "--unavailable", "antigravity",
             "Implementar una API con pruebas"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=20, check=False,
            encoding="utf-8", errors="replace",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        policy = json.loads(result.stdout)["policy_v2"]
        self.assertEqual(policy["unavailable_ais"], ["antigravity", "codex"])
        self.assertNotIn(policy["reviewer_candidate"], ("codex", "antigravity"))

    def test_cli_rejects_unknown_unavailable_ai(self):
        env = dict(os.environ)
        env.pop("PREAMBRA_UNAVAILABLE_AIS", None)
        result = subprocess.run(
            [sys.executable, str(CLI), "--json", "--unavailable", "gpt-x", "Implementar API"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=20, check=False,
            encoding="utf-8", errors="replace",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown AI", result.stderr)

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
