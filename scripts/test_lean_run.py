"""Pruebas de aceptacion deterministas de lean_run.py (V3). No ejecutan ninguna IA ni consumen cuota."""
import argparse
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lean_run", ROOT / "scripts" / "lean_run.py")
lean = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lean)
CFG = lean.load_config()
REPO = Path(tempfile.gettempdir()).resolve()

STREAM = [
    json.dumps({"type": "system", "subtype": "init", "model": "claude-sonnet-5-5", "apiKeySource": "none",
                "tools": ["a"] * 28, "mcp_servers": [], "skills": []}),
    "no es json",
    json.dumps({"type": "result", "num_turns": 6, "duration_ms": 21000, "total_cost_usd": 0.0623, "result": "ok",
                "usage": {"input_tokens": 8, "cache_creation_input_tokens": 7381, "cache_read_input_tokens": 141601,
                          "output_tokens": 1843}}),
]
CODEX = [json.dumps({"type": "thread.started"}),
         json.dumps({"type": "item.completed", "item": {"id": "i1", "type": "agent_message", "text": "18"}}),
         json.dumps({"type": "turn.completed", "usage": {"input_tokens": 900, "cached_input_tokens": 300, "output_tokens": 40}})]


def git_altiora(_cwd):
    return REPO, "https://github.com/alvaradom1304/Altiora.git"


def git_none(_cwd):
    return None, None


def args(task: str = "Redacta el caption del carrusel", **kw) -> argparse.Namespace:
    tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.write(task)
    tmp.close()
    base = dict(profile="lean", project="altiora", task_file=tmp.name, cwd=str(REPO), add_dir=[],
                allow_external_dir=False, mcp_config=[], provider=None, effort=None, reason=None,
                approved_risk=False, allow_write=False, task_id=None, role="worker", log=None)
    base.update(kw)
    return argparse.Namespace(**base)


def pf(a, which=lambda p: f"/bin/{p}", git=git_altiora, env=None, cfg=CFG):
    return lean.preflight(a, cfg, which=which, git=git, env=env or {})


class ArranqueLeanTest(unittest.TestCase):
    def test_lean_is_default_and_isolated(self):
        self.assertEqual(CFG["default_profile"], "lean")
        r = pf(args())
        self.assertEqual(r["status"], "READY", r["blocks"])
        for flag in ("--safe-mode", "--strict-mcp-config", "--disable-slash-commands", "--append-system-prompt-file",
                     "--disallowedTools", "--max-turns", "--max-budget-usd"):
            self.assertIn(flag, r["command"])
        self.assertTrue(lean.LEAN_PROMPT.exists())

    def test_persistence_is_file_based(self):
        # Un proceso nuevo relee profiles.json: el predeterminado sobrevive a reinicios sin flags.
        a = lean.parser(lean.load_config()).parse_args(["--project", "altiora", "--check"])
        self.assertEqual(a.profile, "lean")


class ProyectoTest(unittest.TestCase):
    def test_wrong_repo_blocked(self):
        r = pf(args(project="la-central-del-queso"))
        self.assertEqual(r["status"], "BLOCKED")
        self.assertTrue(any("no pertenece" in b for b in r["blocks"]))

    def test_folder_project_inside_registered_repo_blocked(self):
        r = pf(args(project="currenda"))
        self.assertTrue(any("contexto ajeno" in b for b in r["blocks"]))
        self.assertEqual(pf(args(project="currenda"), git=git_none)["status"], "READY")

    def test_external_add_dir_blocked_unless_explicit(self):
        outside = str(Path(REPO.anchor) / "otro-proyecto")
        self.assertEqual(pf(args(add_dir=[outside]))["status"], "BLOCKED")
        self.assertEqual(pf(args(add_dir=[outside], allow_external_dir=True))["status"], "READY")

    def test_unknown_project_blocked(self):
        self.assertEqual(pf(args(project="x"))["status"], "BLOCKED")


class ModeloYEscalamientoTest(unittest.TestCase):
    def test_model_is_proportional(self):
        self.assertEqual(pf(args(effort="low"))["model_planned"], "claude-haiku-5-5")
        self.assertEqual(pf(args())["model_planned"], "claude-sonnet-5-5")

    def test_high_effort_needs_escalation(self):
        r = pf(args(effort="high"))
        self.assertTrue(any("escalar" in b for b in r["blocks"]))

    def test_advanced_requires_reason(self):
        self.assertEqual(pf(args(profile="advanced"))["status"], "BLOCKED")
        r = pf(args(profile="advanced", reason="decision de arquitectura multi-repo"))
        self.assertEqual((r["status"], r["model_planned"]), ("READY", "claude-opus-5-5"))
        self.assertNotIn("--safe-mode", r["command"])


class DelegacionTest(unittest.TestCase):
    def test_simple_task_no_delegation(self):
        r = pf(args())
        self.assertEqual((r["provider"], r["delegation_chain"], r["fallback_used"]), ("claude", [], False))

    def test_provider_unavailable_falls_back(self):
        r = pf(args(provider="claude"), which=lambda p: None if p == "claude" else f"/bin/{p}")
        self.assertEqual((r["provider"], r["fallback_used"], r["status"]), ("codex", True, "READY"))
        self.assertIn("read-only", r["command"])

    def test_no_provider_blocks(self):
        self.assertEqual(pf(args(), which=lambda p: None)["status"], "BLOCKED")

    def test_cycle_and_depth_prevented(self):
        r = pf(args(provider="claude"), env={lean.CHAIN_ENV: "claude"})
        self.assertTrue(any("ciclo" in b for b in r["blocks"]))
        r = pf(args(provider="codex"), env={lean.CHAIN_ENV: "claude"})
        self.assertTrue(any("profundidad" in b for b in r["blocks"]))

    def test_review_cycles_capped(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "log.csv"
            for _ in range(2):
                lean.append_log(log, {"task_id": "T1", "rol": "reviewer"})
            r = pf(args(provider="codex", task_id="T1", role="reviewer", log=str(log)))
            self.assertTrue(any("revision agotados" in b for b in r["blocks"]))
            self.assertEqual(pf(args(task_id="T2", role="reviewer", log=str(log)))["status"], "READY")


class SeguridadTest(unittest.TestCase):
    def test_mixed_negation_blocks_risky_task(self):
        self.assertEqual(pf(args("no publicar el borrador"))["status"], "READY")
        r = pf(args("no publiques nada pero borra la rama vieja"))
        self.assertEqual(r["risk_signals"], ["borra"])
        self.assertEqual(r["status"], "BLOCKED")
        self.assertEqual(pf(args("no publiques nada pero borra la rama vieja", approved_risk=True))["status"], "READY")

    def test_safe_mode_without_substitute_denies_blocks(self):
        cfg = copy.deepcopy(CFG)
        cfg["security"]["deny_tools"] = [d for d in cfg["security"]["deny_tools"] if ".env" not in d]
        self.assertTrue(any("safe-mode" in b for b in pf(args(), cfg=cfg)["blocks"]))

    def test_forbidden_flag_blocks(self):
        cfg = copy.deepcopy(CFG)
        cfg["profiles"]["lean"]["claude_flags"].append("--dangerously-skip-permissions")
        self.assertTrue(any("prohibida" in b for b in pf(args(), cfg=cfg)["blocks"]))

    def test_codex_write_only_when_explicit(self):
        self.assertIn("read-only", pf(args(provider="codex"))["command"])
        self.assertIn("workspace-write", pf(args(provider="codex", allow_write=True))["command"])


class EconomiaTest(unittest.TestCase):
    def test_parse_claude_and_log(self):
        s = lean.parse_stream(STREAM)
        self.assertEqual((s["turnos"], s["total"], s["herramientas"], s["mcp"]), (6, 150833, 28, 0))
        self.assertEqual(s["ponderado"], round(8 + 7381 * 1.25 + 141601 * 0.1 + 1843 * 5))
        self.assertEqual((s["costo_real"], s["cuota"], s["modelo_efectivo"]),
                         ("SUSCRIPCION_SIN_CARGO_API", "NO_OBSERVADA", "claude-sonnet-5-5"))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.csv"
            lean.append_log(p, {"etiqueta": "T", **s})
            lean.append_log(p, {"etiqueta": "U", **s})
            self.assertEqual(len(p.read_text(encoding="utf-8").splitlines()), 3)

    def test_parse_codex_usage(self):
        s = lean.parse_stream(CODEX)
        self.assertEqual((s["entrada"], s["cache_leida"], s["salida"], s["ok"], s["resultado"]), (600, 300, 40, True, "18"))

    def test_old_log_header_respected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "old.csv"
            p.write_text("fecha,etiqueta,total\n", encoding="utf-8")
            lean.append_log(p, {"fecha": "x", "etiqueta": "y", "total": 1, "proveedor": "z"})
            self.assertEqual(p.read_text(encoding="utf-8").splitlines()[1], "x,y,1")


if __name__ == "__main__":
    unittest.main()
