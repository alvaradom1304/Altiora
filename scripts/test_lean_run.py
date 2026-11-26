"""Pruebas de lean_run.py sin ejecutar claude ni consumir cuota."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lean_run", ROOT / "scripts" / "lean_run.py")
lean = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lean)

STREAM = [
    json.dumps({"type": "system", "subtype": "init", "tools": ["a"] * 28, "mcp_servers": [], "skills": []}),
    "no es json",
    json.dumps({"type": "result", "num_turns": 6, "duration_ms": 21000, "total_cost_usd": 0.0623, "result": "ok",
                "usage": {"input_tokens": 8, "cache_creation_input_tokens": 7381, "cache_read_input_tokens": 141601, "output_tokens": 1843}}),
]


class LeanRunTest(unittest.TestCase):
    def test_lean_isolates_everything(self):
        cmd = lean.build_command("lean", "m", "medium", lean.DEFAULT_TOOLS, ["x"], [])
        for flag in ("--safe-mode", "--strict-mcp-config", "--disable-slash-commands", "--append-system-prompt-file"):
            self.assertIn(flag, cmd)
        self.assertTrue(lean.LEAN_PROMPT.exists())

    def test_standard_only_requested_mcp(self):
        cmd = lean.build_command("standard", "m", "medium", "Read", [], ["a.json"])
        self.assertIn("--strict-mcp-config", cmd)
        self.assertEqual(cmd[cmd.index("--mcp-config") + 1], "a.json")
        self.assertNotIn("--safe-mode", cmd)

    def test_advanced_adds_no_isolation_flags(self):
        cmd = lean.build_command("advanced", "m", "high", "Read", [], [])
        self.assertFalse({"--safe-mode", "--strict-mcp-config"} & set(cmd))

    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValueError):
            lean.build_command("x", "m", "low", "Read", [], [])

    def test_parse_and_log(self):
        s = lean.parse_stream(STREAM)
        self.assertEqual((s["turnos"], s["total"], s["herramientas"], s["mcp"]), (6, 150833, 28, 0))
        self.assertEqual(s["ponderado"], round(8 + 7381 * 1.25 + 141601 * 0.1 + 1843 * 5))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.csv"
            lean.append_log(p, {"etiqueta": "T", **s})
            lean.append_log(p, {"etiqueta": "U", **s})
            self.assertEqual(len(p.read_text(encoding="utf-8").splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
