"""Pruebas de aceptacion deterministas de lean_run.py (V3). No ejecutan ninguna IA ni consumen cuota."""
import argparse
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lean_run", ROOT / "scripts" / "lean_run.py")
lean = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lean)
CFG = lean.load_config()
REPO = Path(tempfile.gettempdir()).resolve()
lean.RETRY_BACKOFF_S = (0, 0)  # las pruebas no esperan entre reintentos

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
                approved_risk=False, allow_write=False, allow_exec=False, task_id=None, role="worker", log=None,
                det_cmd=None, depends_on=[], interactive=False, context_file=[], verify_cmd=None, accept_interactive_limits=False, accept_script_risk=True)
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
        self.assertNotIn("Bash", r["tools_allowed"])  # LEAN sin ejecucion de comandos por defecto
        deny = r["command"][r["command"].index("--disallowedTools") + 1].split(",")
        self.assertIn("Bash", deny)
        self.assertIn("Write(./**)", r["tools_allowed"])
        self.assertEqual(r["command"][r["command"].index("--permission-mode") + 1], "default")

    def test_persistence_is_file_based(self):
        # Un proceso nuevo relee profiles.json: el predeterminado sobrevive a reinicios sin flags.
        a = lean.parser(lean.load_config()).parse_args(["--check"])
        self.assertEqual((a.profile, a.project), ("lean", "auto"))


class ProyectoTest(unittest.TestCase):
    def test_wrong_repo_blocked(self):
        r = pf(args(project="la-central-del-queso"))
        self.assertEqual(r["status"], "BLOCKED")
        self.assertTrue(any("no pertenece" in b for b in r["blocks"]))

    def test_folder_project_inside_registered_repo_blocked(self):
        r = pf(args(project="currenda"))
        self.assertTrue(any("contexto ajeno" in b for b in r["blocks"]))
        with tempfile.TemporaryDirectory() as own:  # %TEMP% puede contener repos ajenos: carpeta propia
            self.assertEqual(pf(args(project="currenda", cwd=own), git=git_none)["status"], "READY")

    def test_folder_project_parent_of_other_repo_blocked(self):
        # Defecto 2026-11-27: --cwd %USERPROFILE% aceptaba 'currenda' con todo el perfil como raiz.
        with tempfile.TemporaryDirectory() as parent:
            (Path(parent) / "otro-cliente" / ".git").mkdir(parents=True)
            r = pf(args(project="currenda", cwd=parent), git=git_none)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertTrue(any("contiene otro repositorio" in b for b in r["blocks"]), r["blocks"])
        with tempfile.TemporaryDirectory() as own:
            (Path(own) / "produccion" / "c1").mkdir(parents=True)
            r = pf(args(project="currenda", cwd=own), git=git_none)
            self.assertEqual(r["status"], "READY", r["blocks"])
            self.assertTrue(r["writable"])

    def test_nested_scan_fails_closed_when_too_wide(self):
        with tempfile.TemporaryDirectory() as wide:
            for i in range(4):
                (Path(wide) / f"d{i}.txt").write_text("x")  # tambien cuentan los archivos, no solo carpetas
            self.assertEqual(lean.nested_repo(Path(wide), max_entries=2), "DEMASIADO_AMPLIA")

    def test_nested_scan_reaches_depth_three_like_profile_onedrive_desktop(self):
        # Revision Codex 52dfc35: %USERPROFILE%\OneDrive\Desktop\<carpeta>\.git quedaba sin examinar (solo 2 niveles).
        with tempfile.TemporaryDirectory() as home:
            (Path(home) / "OneDrive" / "Desktop" / "altiora" / ".git").mkdir(parents=True)
            self.assertTrue(lean.nested_repo(Path(home)).endswith("altiora"))
            self.assertIsNone(lean.nested_repo(Path(home), depth=2))

    def test_nested_scan_marker_case_and_file(self):
        with tempfile.TemporaryDirectory() as home:
            (Path(home) / "a").mkdir()
            (Path(home) / "a" / ".GIT").write_text("gitdir: x")  # worktree: .git es archivo; mayusculas en Windows
            self.assertTrue(lean.nested_repo(Path(home)).endswith("a"))

    def test_nested_scan_unreadable_fails_closed(self):
        with tempfile.TemporaryDirectory() as home:
            real = lean.os.scandir
            def deny(p):
                if str(p) != home:
                    raise PermissionError(p)
                return real(p)
            (Path(home) / "privada").mkdir()
            lean.os.scandir = deny
            try:
                self.assertTrue(lean.nested_repo(Path(home)).startswith("NO_LEGIBLE"))
            finally:
                lean.os.scandir = real

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


class OrquestacionV31Test(unittest.TestCase):
    def log_with(self, d, *rows):
        log = Path(d) / "log.csv"
        for r in rows:
            lean.append_log(log, r)
        return str(log)

    def test_auto_project_and_task_id(self):
        a = args(project="auto")
        r = pf(a)
        self.assertEqual((r["project"], r["status"]), ("altiora", "READY"))
        self.assertTrue(r["task_id"].startswith("T-"))
        self.assertEqual(pf(args(project="auto"), git=git_none)["status"], "BLOCKED")

    def test_duplicate_task_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            log = self.log_with(d, {"task_id": "T1", "rol": "worker", "estado": "OK", "total": 10})
            self.assertTrue(any("duplicada" in b for b in pf(args(task_id="T1", log=log))["blocks"]))

    def test_token_budget_exhausted(self):
        with tempfile.TemporaryDirectory() as d:
            log = self.log_with(d, {"task_id": "T1", "rol": "worker", "estado": "FALLO_rc1", "total": 150000})
            self.assertTrue(any("presupuesto de tokens" in b for b in pf(args(task_id="T1", log=log))["blocks"]))

    def test_coordination_budget(self):
        with tempfile.TemporaryDirectory() as d:
            rows = [{"task_id": "T1", "rol": "worker", "estado": "FALLO_rc1", "total": 1}] * 4
            log = self.log_with(d, *rows)
            self.assertTrue(any("coordinacion" in b for b in pf(args(task_id="T1", log=log))["blocks"]))

    def test_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            log = self.log_with(d, {"task_id": "T0", "rol": "worker", "estado": "OK", "calidad": "FAIL", "total": 1})
            self.assertTrue(any("dependencia" in b for b in pf(args(task_id="T1", depends_on=["T0"], log=log))["blocks"]))
            log2 = self.log_with(d, {"task_id": "T9", "rol": "worker", "estado": "OK", "calidad": "PASS", "total": 1})
            self.assertEqual(pf(args(task_id="T1", depends_on=["T9"], log=log2))["status"], "READY")

    def test_deterministic_preferred_and_validated(self):
        r = pf(args(det_cmd="python -c print(1)"))
        self.assertEqual((r["provider"], r["model_planned"]), ("det", "determinista"))
        self.assertTrue(any("sin -c/-e" in b for b in r["blocks"]))  # codigo en linea rechazado
        self.assertTrue(lean.check_script_cmd("bash x.sh", ROOT, CFG, "v"))
        self.assertEqual(lean.check_script_cmd("python scripts/lean_run.py --help", ROOT, CFG, "v"), [])
        self.assertTrue(lean.check_script_cmd("python ../fuera.py", ROOT, CFG, "v"))

    def test_exec_opt_in_and_not_with_risk(self):
        r = pf(args(allow_exec=True))
        self.assertIn("Bash(python *)", r["tools_allowed"])
        self.assertNotIn("Bash", r["command"][r["command"].index("--disallowedTools") + 1].split(","))
        r = pf(args("borra la carpeta vieja", allow_exec=True, approved_risk=True))
        self.assertTrue(any("allow-exec" in b for b in r["blocks"]))

    def test_interactive_has_no_print_only_flags(self):
        self.assertTrue(any("--accept-interactive-limits" in b for b in pf(args(interactive=True))["blocks"]))
        r = pf(args(interactive=True, accept_interactive_limits=True))
        self.assertEqual(r["status"], "READY", r["blocks"])
        self.assertNotIn("-p", r["command"])
        self.assertIn("--safe-mode", r["command"])
        self.assertIn("--disallowedTools", r["command"])

    def test_empty_result_is_not_ok(self):
        s = lean.parse_stream([json.dumps({"type": "result", "result": "", "usage": {}})])
        self.assertFalse(s["ok"])

    def test_integrity_detects_secret_and_config_writes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / ".claude").mkdir()
            (root / "ok.txt").write_text("x")
            before = lean.integrity_snapshot(root, CFG)
            (root / "nuevo.txt").write_text("legitimo")
            self.assertEqual(lean.integrity_diff(before, lean.integrity_snapshot(root, CFG)), [])
            (root / ".env").write_text("FAKE=1")
            (root / ".claude" / "settings.json").write_text("{}")
            (root / ".env.example").write_text("A=")
            self.assertEqual(lean.integrity_diff(before, lean.integrity_snapshot(root, CFG)),
                             [".claude/settings.json", ".env"])


class RevisionV31Test(unittest.TestCase):
    """Regresiones de los hallazgos de la revision independiente de Codex (V31-REV)."""

    def test_task_id_path_rejected(self):
        for bad in (str(REPO), "../x", "a/b", "..", "C:\\x"):
            r = pf(args(task_id=bad))
            self.assertTrue(any("--task-id invalido" in b for b in r["blocks"]), bad)
        with self.assertRaises(ValueError):
            lean.neutral_workspace(str(REPO), [], REPO)

    def test_neutral_workspace_never_reuses_or_deletes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.py").write_text("x")
            w1 = lean.neutral_workspace("SAME", ["a.py"], root)
            w2 = lean.neutral_workspace("SAME", ["a.py"], root)
            self.assertNotEqual(w1, w2)
            self.assertTrue(w1.exists())
            shutil.rmtree(w1)
            shutil.rmtree(w2)

    def test_bash_denied_without_allow_exec_in_every_profile(self):
        for prof, extra in (("standard", {}), ("advanced", {"reason": "arquitectura"})):
            r = pf(args(profile=prof, **extra))
            deny = r["command"][r["command"].index("--disallowedTools") + 1].split(",")
            self.assertIn("Bash", deny, prof)
            self.assertNotIn("Bash", r["tools_allowed"], prof)

    def test_interactive_from_delegation_blocked(self):
        r = pf(args(interactive=True, provider="claude"), env={lean.CHAIN_ENV: "codex"})
        self.assertTrue(any("interactiva" in b for b in r["blocks"]))

    def test_cmd_shims_rejected_on_windows(self):
        if lean.sys.platform == "win32":
            self.assertIsNone(lean.resolve_exe("x", which=lambda p: "C:/npm/x.CMD"))
        self.assertEqual(lean.resolve_exe("x", which=lambda p: "C:/npm/x.EXE"), "C:/npm/x.EXE")

    def test_context_file_paths_announced_to_neutral_worker(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / ".lean-ctx").mkdir()
            (Path(d) / ".lean-ctx" / "extractos.md").write_text("x", encoding="utf-8")
            task = Path(d) / "t.txt"
            task.write_text("Redacta un caption", encoding="utf-8")
            seen = {}

            def fake_run(cmd, provider, task_text, cwd, env):
                if provider == "codex":  # el respaldo claude trabaja en el cwd del proyecto, sin carpeta neutra
                    seen.setdefault("task", task_text)
                    seen.setdefault("cwd", cwd)
                return lean.subprocess.CompletedProcess(cmd, 1, "", "")

            orig_run, orig_git, orig_which = lean.run_provider, lean.git_info, lean.shutil.which
            lean.run_provider = fake_run
            lean.git_info = lambda _c: (Path(d).resolve(), "https://github.com/alvaradom1304/Altiora.git")
            lean.shutil.which = lambda p: f"/bin/{p}"
            try:
                lean.main(["--project", "altiora", "--cwd", d, "--task-file", str(task), "--log", str(Path(d) / "l.csv"),
                           "--task-id", "TCTX", "--provider", "codex", "--context-file", ".lean-ctx/extractos.md"])
            finally:
                lean.run_provider, lean.git_info, lean.shutil.which = orig_run, orig_git, orig_which
            self.assertIn(".lean-ctx/extractos.md", seen["task"])
            self.assertTrue((Path(seen["cwd"]) / ".lean-ctx" / "extractos.md").is_file())  # la ruta anunciada existe

    def test_limits_rechecked_before_each_attempt(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "log.csv"
            task = Path(d) / "t.txt"
            task.write_text("Redacta un caption", encoding="utf-8")
            calls = []

            def fake_run(cmd, provider, task_text, cwd, env):
                calls.append(provider)
                lean.append_log(log, {"task_id": "TB", "rol": "worker", "estado": "FALLO_rc1", "total": 150000})
                return lean.subprocess.CompletedProcess(cmd, 1, "", "")

            orig_run, orig_git, orig_which = lean.run_provider, lean.git_info, lean.shutil.which
            lean.run_provider = fake_run
            lean.git_info = lambda _c: (Path(d).resolve(), "https://github.com/alvaradom1304/Altiora.git")
            lean.shutil.which = lambda p: f"/bin/{p}"
            try:
                rc = lean.main(["--project", "altiora", "--cwd", d, "--task-file", str(task), "--log", str(log),
                                "--task-id", "TB"])
            finally:
                lean.run_provider, lean.git_info, lean.shutil.which = orig_run, orig_git, orig_which
            self.assertEqual(rc, 2)
            self.assertEqual(len(calls), 1)  # el presupuesto agotado tras el 1.er intento impide el 2.o


class RevisionV32Test(unittest.TestCase):
    """Regresiones de la segunda revision independiente (V32-REV)."""

    def test_allow_write_blocked_for_effective_provider(self):
        only_codex = lambda p: "/bin/codex" if p == "codex" else None
        r = pf(args(allow_write=True), which=only_codex)
        self.assertTrue(any("proveedor efectivo" in b for b in r["blocks"]))

    def test_script_runner_must_be_bare_name_and_relative_script(self):
        for bad in ("C:/attacker/python.exe scripts/lean_run.py", "python /abs/x.py", "python ../x.py", "python -c x"):
            self.assertTrue(lean.check_script_cmd(bad, ROOT, CFG, "v", ROOT), bad)
        self.assertEqual(lean.check_script_cmd('python "scripts/lean_run.py" --help', ROOT, CFG, "v", ROOT), [])

    def test_script_resolved_from_cwd_not_root(self):
        self.assertTrue(lean.check_script_cmd("python lean_run.py", ROOT, CFG, "v", ROOT))  # existe solo en scripts/
        self.assertEqual(lean.check_script_cmd("python lean_run.py", ROOT, CFG, "v", ROOT / "scripts"), [])

    def test_context_file_traversal_absolute_and_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "A"
            root.mkdir()
            (root / "ok.txt").write_text("x")
            (root / ".env").write_text("S=1")
            self.assertTrue(lean.check_context_files(["../A/ok.txt"], root, CFG))
            self.assertTrue(lean.check_context_files([str(root / "ok.txt")], root, CFG))
            try:
                (root / "public.txt").symlink_to(root / ".env")
            except OSError:
                return  # Windows sin privilegio de enlaces: se omite solo esta parte
            self.assertTrue(lean.check_context_files(["public.txt"], root, CFG))

    def test_integrity_inventory_failure_is_blocking(self):
        with tempfile.TemporaryDirectory() as d:
            orig = lean.os.walk

            def bad_walk(root, onerror=None, **kw):
                onerror(PermissionError("denegado"))
                return iter(())
            lean.os.walk = bad_walk
            try:
                with self.assertRaises(RuntimeError):
                    lean.integrity_snapshot(Path(d), CFG)
            finally:
                lean.os.walk = orig

    def test_relative_add_dir_resolved_against_cwd(self):
        a = args(add_dir=[".."])
        r = pf(a)
        self.assertEqual(a.add_dir, [str(REPO.parent.resolve())])
        self.assertTrue(any("fuera del proyecto" in b for b in r["blocks"]))


class RevisionV33Test(unittest.TestCase):
    def test_scripts_need_explicit_risk_acceptance(self):
        r = pf(args(det_cmd="python scripts/lean_run.py --help", accept_script_risk=False, cwd=str(ROOT)), git=lambda _c: (ROOT, "https://github.com/alvaradom1304/Altiora.git"))
        self.assertTrue(any("--accept-script-risk" in b for b in r["blocks"]))

    def test_clean_env_drops_secrets(self):
        os_env = lean.os.environ
        os_env["GH_TOKEN_TEST"], os_env["ANTHROPIC_API_KEY"] = "x", "y"
        try:
            env = lean.clean_env(["claude"])
        finally:
            del os_env["GH_TOKEN_TEST"], os_env["ANTHROPIC_API_KEY"]
        self.assertNotIn("GH_TOKEN_TEST", env)
        self.assertNotIn("ANTHROPIC_API_KEY", env)
        self.assertEqual(env[lean.CHAIN_ENV], "claude")


class CodexNeutralTest(unittest.TestCase):
    def test_codex_lean_ignores_user_config(self):
        self.assertIn("--ignore-user-config", pf(args(provider="codex"))["command"])

    def test_context_files_validated_and_copied(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.py").write_text("x = 1")
            (root / ".env").write_text("S=1")
            self.assertEqual(lean.check_context_files(["a.py"], root, CFG), [])
            self.assertTrue(lean.check_context_files([".env"], root, CFG))
            self.assertTrue(lean.check_context_files(["../fuera.py"], root, CFG))
            ws = lean.neutral_workspace("TEST-NEUTRAL", ["a.py"], root)
            self.assertEqual(sorted(p.name for p in ws.iterdir()), ["AGENTS.md", "a.py"])
            shutil.rmtree(ws)


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

    def test_codex_read_only_and_write_blocked(self):
        self.assertIn("read-only", pf(args(provider="codex"))["command"])
        r = pf(args(provider="codex", allow_write=True))
        self.assertTrue(any("--allow-write bloqueado" in b for b in r["blocks"]))


class EconomiaTest(unittest.TestCase):
    def test_parse_claude_and_log(self):
        s = lean.parse_stream(STREAM)
        self.assertEqual((s["turnos"], s["total"], s["herramientas"], s["mcp"]), (6, 150833, 28, 0))
        self.assertEqual(s["ponderado"], round(8 + 7381 * 1.25 + 141601 * 0.1 + 1843 * 5))
        self.assertEqual((s["costo_real"], s["cuota"], s["modelo_efectivo"]),
                         ("SIN_API_KEY_DECLARADA_FACTURA_NO_VERIFICADA", "NO_OBSERVADA", "claude-sonnet-5-5"))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.csv"
            lean.append_log(p, {"etiqueta": "T", **s})
            lean.append_log(p, {"etiqueta": "U", **s})
            self.assertEqual(len(p.read_text(encoding="utf-8").splitlines()), 3)

    def test_parse_codex_usage(self):
        s = lean.parse_stream(CODEX)
        self.assertEqual((s["entrada"], s["cache_leida"], s["salida"], s["ok"], s["resultado"]), (600, 300, 40, True, "18"))

    def test_parse_agy_json(self):
        s = lean.parse_stream([json.dumps({"conversation_id": "c", "status": "SUCCESS", "response": "listo",
                                           "duration_seconds": 20.2, "num_turns": 1,
                                           "usage": {"input_tokens": 34116, "output_tokens": 2, "cache_read_tokens": 0}})])
        self.assertEqual((s["ok"], s["resultado"].strip(), s["total"], s["turnos"], s["segundos"]), (True, "listo", 34118, 1, 20))

    def test_parse_agy_multiline_json(self):
        raw = json.dumps({"status": "SUCCESS", "response": "ok", "num_turns": 1,
                          "usage": {"input_tokens": 5, "output_tokens": 1}}, indent=2)
        self.assertTrue(lean.parse_stream(raw.splitlines())["ok"])

    def test_old_log_header_respected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "old.csv"
            p.write_text("fecha,etiqueta,total\n", encoding="utf-8")
            lean.append_log(p, {"fecha": "x", "etiqueta": "y", "total": 1, "proveedor": "z"})
            self.assertEqual(p.read_text(encoding="utf-8").splitlines()[1], "x,y,1")


class FinalReadinessTest(unittest.TestCase):
    def test_unknown_auth_does_not_claim_subscription(self):
        for stream in ([], CODEX, [json.dumps({"type": "system", "subtype": "init"})],
                       [json.dumps({"status": "SUCCESS", "response": "ok"})]):
            self.assertEqual(lean.parse_stream(stream)["costo_real"], "NO_OBSERVADO")
        explicit = [{"type": "system", "subtype": "init", "apiKeySource": "none"}]
        self.assertEqual(lean.parse_stream([json.dumps(x) for x in explicit])["costo_real"],
                         "SIN_API_KEY_DECLARADA_FACTURA_NO_VERIFICADA")

    def test_unreadable_protected_file_blocks_inventory(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / ".env").write_text("FIXTURE_ONLY", encoding="utf-8")
            with patch.object(Path, "read_bytes", side_effect=PermissionError("fixture denied")):
                with self.assertRaisesRegex(RuntimeError, "inventario de integridad incompleto"):
                    lean.integrity_snapshot(root, CFG)


AGY_ERROR = json.dumps({"conversation_id": "", "status": "ERROR", "response": "",
                        "error": "failed to start conversation: backend returned an empty conversation id",
                        "usage": {"input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0, "cache_read_tokens": 0}})


class AntigravityTest(unittest.TestCase):
    """Correcciones Antigravity (sondas reales agy 1.4.12, 2026-11-28)."""

    def _main(self, d, fake_run, *extra):
        task = Path(d) / "t.txt"
        task.write_text("Redacta un caption", encoding="utf-8")
        orig_run, orig_git, orig_which = lean.run_provider, lean.git_info, lean.shutil.which
        lean.run_provider = fake_run
        lean.git_info = lambda _c: (Path(d).resolve(), "https://github.com/alvaradom1304/Altiora.git")
        lean.shutil.which = lambda p: f"/bin/{p}"
        try:
            return lean.main(["--project", "altiora", "--cwd", d, "--task-file", str(task), "--log",
                              str(Path(d) / "l.csv"), "--profile", "standard", "--accept-agy-limits", *extra])
        finally:
            lean.run_provider, lean.git_info, lean.shutil.which = orig_run, orig_git, orig_which

    def test_plan_mode_not_cancelled_by_slash_disable(self):
        r = pf(args(profile="standard", provider="agy", accept_agy_limits=True))
        self.assertEqual(r["status"], "READY", r["blocks"])
        self.assertEqual(r["command"][r["command"].index("--mode") + 1], "plan")
        self.assertNotIn("--disable-slash-commands", r["command"])
        bad = ["agy", "--mode", "plan", "--disable-slash-commands", "-p"]
        self.assertTrue(any("anula --mode plan" in b for b in lean.security_check(bad, "agy", CFG)))
        self.assertTrue(any("sin --mode" in b for b in lean.security_check(["agy", "-p"], "agy", CFG)))

    def test_agy_disabled_without_explicit_acceptance(self):
        r = pf(args(profile="standard", provider="agy"))
        self.assertEqual(r["status"], "BLOCKED")
        self.assertTrue(any("agy desactivado" in b for b in r["blocks"]))
        only_agy = lambda p: "/bin/agy" if p == "agy" else None  # ni siquiera como unico respaldo
        r2 = pf(args(profile="standard"), which=only_agy)
        self.assertIsNone(r2["provider"])
        self.assertFalse(r2["providers_available"]["agy"])

    def test_leading_slash_neutralized(self):
        from unittest.mock import patch
        with patch.object(lean, "resolve_exe", return_value="agy.exe"), \
                patch.object(lean.subprocess, "run", return_value=None) as run:
            lean.run_provider(["agy", "--mode", "plan", "-p"], "agy", "  /deploy prod", ".", {})
        self.assertEqual(run.call_args[0][0][-1], "Tarea: /deploy prod")

    def test_agy_error_is_failure_with_reason_and_thinking_counted(self):
        s = lean.parse_stream([AGY_ERROR])
        self.assertFalse(s["ok"])
        self.assertTrue(s["resultado"].startswith("ERROR: failed to start conversation"))
        bare = lean.parse_stream([json.dumps({"status": "ERROR", "error": "cuota"})])  # sin response/conversation_id
        self.assertEqual((bare["ok"], bare["resultado"]), (False, "ERROR: cuota"))
        naked = lean.parse_stream([json.dumps({"status": "ERROR"})])
        self.assertEqual((naked["ok"], naked["resultado"]), (False, "ERROR: ERROR sin detalle"))
        ok = lean.parse_stream([json.dumps({"conversation_id": "c", "status": "SUCCESS", "response": "ok",
                                            "usage": {"input_tokens": 10, "output_tokens": 2, "thinking_tokens": 5}})])
        self.assertEqual((ok["salida"], ok["total"]), (7, 17))

    def test_transient_zero_token_failures_retried_then_fallback(self):
        calls = []

        def fake_run(cmd, provider, task_text, cwd, env):
            calls.append(provider)
            out = AGY_ERROR if provider == "agy" else json.dumps({"type": "result", "result": "ok", "num_turns": 1,
                                                                   "usage": {"input_tokens": 3, "output_tokens": 1}})
            return lean.subprocess.CompletedProcess(cmd, 0, out, "")

        with tempfile.TemporaryDirectory() as d:
            rc = self._main(d, fake_run, "--provider", "agy", "--task-id", "TAGY1")
            rows = lean.read_log(Path(d) / "l.csv")
        self.assertEqual(rc, 0)
        self.assertEqual(calls, ["agy"] * (CFG["limits"]["max_retries"] + 1) + ["claude"])
        self.assertTrue(rows[0]["motivo"].startswith("transitorio_sin_consumo: ERROR: failed to start"))
        self.assertEqual(rows[-1]["motivo"], "")

    def test_failure_with_consumption_not_retried(self):
        calls = []

        def fake_run(cmd, provider, task_text, cwd, env):
            calls.append(provider)
            out = json.dumps({"conversation_id": "c", "status": "SUCCESS", "response": "",
                              "usage": {"input_tokens": 34000, "output_tokens": 1}})
            return lean.subprocess.CompletedProcess(cmd, 0, out, "")

        with tempfile.TemporaryDirectory() as d:
            self._main(d, fake_run, "--provider", "agy", "--task-id", "TAGY2")
            rows = lean.read_log(Path(d) / "l.csv")
        self.assertEqual(calls.count("agy"), 1)  # sin reintento identico tras gastar tokens
        self.assertTrue(rows[0]["motivo"].startswith("fallo_con_consumo"))


GUARD = ROOT / ".altiora" / "system" / "scripts" / "guard.py"


def guard(payload: dict, project: str = "..", cwd: Path = ROOT / ".agents") -> dict:
    import subprocess
    import sys
    p = subprocess.run([sys.executable, str(GUARD), "--runtime", "antigravity", "--project", project,
                        "--event", "PreToolUse"], input=json.dumps(payload), capture_output=True, text=True, cwd=cwd)
    return json.loads(p.stdout)


class AntigravityGuardTest(unittest.TestCase):
    """Formato real de agy 1.4.12 capturado por sonda; el guard antes solo reconocia write_to_file/TargetFile."""

    def test_write_file_to_secret_denied_with_relative_project(self):
        self.assertEqual(guard({"toolCall": {"name": "write_file", "args": {"Path": "C:\\x\\.env", "Content": "a"}}})
                         ["decision"], "deny")
        self.assertEqual(guard({"toolCall": {"name": "write_file", "args": {"Path": "notas.md"}}})["decision"], "allow")
        self.assertEqual(guard({"toolCall": {"name": "write_to_file", "args": {"TargetFile": "a/id_rsa"}}})
                         ["decision"], "deny")

    def test_mcp_write_denied_and_read_allowed(self):
        mcp = {"toolCall": {"name": "call_mcp_tool", "args": {"ServerName": "altiora-shared", "ToolName": "write_file",
                                                               "Arguments": {"path": "C:/p/.env.local"}}}}
        self.assertEqual(guard(mcp)["decision"], "deny")
        self.assertEqual(guard({"toolCall": {"name": "read_file", "args": {"Path": ".env"}}})["decision"], "allow")

    def test_hooks_json_is_portable(self):
        text = (ROOT / ".agents" / "hooks.json").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"[A-Za-z]:[/\\]")  # sin rutas absolutas de una maquina o checkout
        cfg = json.loads(text)["altiora-agent-system"]
        cmd = cfg["PreToolUse"][0]["hooks"][0]["command"]
        self.assertIn("../.altiora/system/scripts/guard.py", cmd)
        self.assertTrue((ROOT / ".agents" / ".." / ".altiora" / "system" / "scripts" / "guard.py").is_file())


if __name__ == "__main__":
    unittest.main()
