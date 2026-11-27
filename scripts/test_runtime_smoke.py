import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).with_name('runtime-smoke.py')
spec = importlib.util.spec_from_file_location('runtime_smoke', MODULE)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)

FIXTURE_GUARD = '''import argparse,json,sys
p=argparse.ArgumentParser()
p.add_argument('--runtime'); p.add_argument('--project'); p.add_argument('--event')
a=p.parse_args()
try:
 v=json.load(sys.stdin)
 if not isinstance(v,dict): raise ValueError()
 invalid=False
except (ValueError,TypeError): v={}; invalid=True
if a.event=='SessionStart':
 r={'injectSteps':[{'systemMessage':{'systemMessage':'fixture context'}}]} if a.runtime=='antigravity' else {'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':'fixture context'}}
else:
 call=v.get('toolCall',{}) if a.runtime=='antigravity' else v
 args=call.get('args',{}) if a.runtime=='antigravity' else call.get('tool_input',{})
 filename=args.get('file_path',args.get('TargetFile',''))
 deny=invalid or filename=='.env' or 'Add File: .env\\n' in args.get('command','')
 r=({'decision':'deny','reason':'fixture denial'} if deny else {'decision':'allow'}) if a.runtime=='antigravity' else ({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':'fixture denial'}} if deny else {})
print(json.dumps(r))
'''


class RuntimeSmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.scratch = self.root / 'scratch'
        self.scratch.mkdir()

    def tearDown(self):
        self.assertTrue(self.root.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.temp.cleanup()

    def kit(self, source=FIXTURE_GUARD):
        guard = self.project / '.altiora/system/scripts/guard.py'
        guard.parent.mkdir(parents=True, exist_ok=True)
        guard.write_text(source, encoding='utf-8')
        key = '.altiora/system/scripts/guard.py'
        receipt = {'version': 'fixture', 'managed': {key: hashlib.sha256(guard.read_bytes()).hexdigest()}}
        (self.project / '.altiora/installation.json').write_text(json.dumps(receipt), encoding='utf-8')
        policy = {'protected_names': ['.env', '*.env'], 'allowed_names': ['.env.example']}
        (self.project / '.altiora/policy.json').write_text(json.dumps(policy), encoding='utf-8')
        return guard

    def test_missing_kit_is_structured_and_launches_nothing(self):
        report = smoke.run_smoke(self.project, self.scratch)
        self.assertEqual(report['status'], 'KIT_NOT_PRESENT')
        self.assertEqual(report['executed_cases'], 0)

    def test_hash_drift_never_launches_changed_guard(self):
        guard = self.kit()
        guard.write_text('raise RuntimeError("PRIVATE_PAYLOAD")', encoding='utf-8')
        report = smoke.run_smoke(self.project, self.scratch)
        self.assertEqual(report['status'], 'SOURCE_NOT_VERIFIED')
        self.assertEqual(report['executed_cases'], 0)
        self.assertNotIn('PRIVATE_PAYLOAD', json.dumps(report))

    def test_complete_adapter_smoke_is_separate_from_native_activation(self):
        self.kit()
        report = smoke.run_smoke(self.project, self.scratch)
        self.assertEqual(report['status'], 'PASS', json.dumps(report))
        self.assertEqual(report['executed_cases'], 18)
        self.assertTrue(all(row['native_session'] == 'NOT_VERIFIED' for row in report['runtimes']))
        self.assertTrue(all(row['state'] == 'NOT_COVERED' for row in report['unsupported_coverage']))
        self.assertEqual(list(self.scratch.iterdir()), [])
        self.assertFalse((self.project / '.env').exists())

    def test_malformed_stdout_is_redacted_and_stops_repetition(self):
        self.kit('print("private-token /private/customer.env")')
        report = smoke.run_smoke(self.project, self.scratch)
        self.assertEqual(report['status'], 'FAIL')
        self.assertEqual(report['executed_cases'], 1)
        self.assertNotIn('private-token', json.dumps(report))
        self.assertNotIn('customer.env', json.dumps(report))

    def test_codex_pretool_unsupported_controls_cannot_fake_a_denial(self):
        denial = {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                  'permissionDecision': 'deny', 'permissionDecisionReason': 'fixture denial'}}
        for key in ['continue', 'stopReason', 'suppressOutput']:
            for value in [False, True, None, 'ignored']:
                with self.subTest(key=key, value=value):
                    self.assertFalse(smoke.passed_case('codex', 'protected_edit', {**denial, key: value}))

    def test_startup_context_cannot_pass_with_conflicting_stop_controls(self):
        startup = {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': 'fixture context'}}
        for runtime in ['codex', 'claude']:
            for value in [False, None, 0, 1, 'true', 'false']:
                with self.subTest(runtime=runtime, value=value):
                    self.assertFalse(smoke.passed_case(runtime, 'session_start', {**startup, 'continue': value}))
            self.assertFalse(smoke.passed_case(runtime, 'session_start', {**startup, 'stopReason': 'Stop initialization'}))

    def test_valid_context_and_denial_outputs_keep_passing(self):
        startup = {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': 'fixture context'}}
        denial = {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                  'permissionDecision': 'deny', 'permissionDecisionReason': 'fixture denial'}}
        for runtime in ['codex', 'claude']:
            self.assertTrue(smoke.passed_case(runtime, 'session_start', startup))
            self.assertTrue(smoke.passed_case(runtime, 'session_start', {**startup, 'continue': True}))
            self.assertTrue(smoke.passed_case(runtime, 'protected_edit', denial))

    def test_exact_verified_copy_executes_even_if_source_changes_after_check(self):
        guard = self.kit()
        original = guard.read_bytes()
        real_runner = smoke.limited_process

        def inspect_launch(command, payload, cwd, timeout):
            self.assertNotEqual(Path(command[3]), guard)
            self.assertTrue(Path(command[3]).resolve().is_relative_to(self.scratch.resolve()))
            self.assertEqual(Path(command[3]).read_bytes(), original)
            guard.write_text('raise RuntimeError("changed_source_must_not_run")', encoding='utf-8')
            return real_runner(command, payload, cwd, timeout)

        with patch.object(smoke, 'limited_process', side_effect=inspect_launch):
            self.assertEqual(smoke.run_smoke(self.project, self.scratch)['status'], 'PASS')

    def test_configured_commands_and_unrelated_credentials_are_not_used(self):
        self.kit('import os\nassert "FAKE_RUNTIME_SECRET" not in os.environ\n' + FIXTURE_GUARD)
        settings = self.project / '.claude/settings.json'
        settings.parent.mkdir()
        settings.write_text('{"hooks":{"command":"DO_NOT_EXECUTE private-config-command"}}', encoding='utf-8')
        with patch.dict(os.environ, {'FAKE_RUNTIME_SECRET': 'private-environment-value'}):
            report = smoke.run_smoke(self.project, self.scratch)
        self.assertEqual(report['status'], 'PASS')
        self.assertNotIn('private-environment-value', json.dumps(report))
        self.assertNotIn('private-config-command', json.dumps(report))

    def test_timeout_and_output_limit_are_bounded_failures(self):
        for source, expected, timeout in [('import time; time.sleep(20)', 'TIMEOUT', 0.2), ('print("x"*50000)', 'OUTPUT_LIMIT', 5.0)]:
            self.kit(source)
            report = smoke.run_smoke(self.project, self.scratch, timeout=timeout)
            self.assertEqual(report['status'], 'FAIL')
            self.assertEqual(report['runtimes'][0]['cases'][0]['reason'], expected)
            self.assertEqual(list(self.scratch.iterdir()), [])

    def test_linked_or_hardlinked_guard_is_not_executed(self):
        guard = self.kit()
        linked = guard.with_name('alias.py')
        linked.hardlink_to(guard)
        self.assertEqual(smoke.run_smoke(self.project, self.scratch)['status'], 'SOURCE_NOT_VERIFIED')

    def test_invalid_policy_or_missing_receipt_never_launch(self):
        self.kit()
        (self.project / '.altiora/policy.json').write_text('{"protected_names":42}', encoding='utf-8')
        self.assertEqual(smoke.run_smoke(self.project, self.scratch)['executed_cases'], 0)
        (self.project / '.altiora/installation.json').unlink()
        self.assertEqual(smoke.run_smoke(self.project, self.scratch)['executed_cases'], 0)

    def test_relative_or_linked_scratch_is_rejected(self):
        self.kit()
        self.assertEqual(smoke.run_smoke(self.project, Path('relative'))['status'], 'UNSAFE_LOCATION')
        alias = self.root / 'scratch-link'
        try:
            alias.symlink_to(self.scratch, target_is_directory=True)
        except OSError:
            if os.name != 'nt' or subprocess.run(['cmd', '/c', 'mklink', '/J', str(alias), str(self.scratch)], capture_output=True).returncode:
                self.skipTest('Directory links not available')
        self.assertEqual(smoke.run_smoke(self.project, alias)['status'], 'UNSAFE_LOCATION')


class ClaudeHookConfigTest(unittest.TestCase):
    def test_config_and_guard(self):
        import sys
        from pathlib import PureWindowsPath

        repo = Path(__file__).resolve().parents[1]
        config = json.loads(
            (repo / ".claude/settings.json").read_text(encoding="utf-8-sig")
        )["hooks"]
        marker = "${CLAUDE_PROJECT_DIR}"
        handlers = {}
        for event in ("SessionStart", "PreToolUse"):
            with self.subTest(event=event):
                self.assertEqual(len(config[event]), 1)
                group = config[event][0]
                self.assertEqual(group["matcher"], "*")
                self.assertEqual(len(group["hooks"]), 1)
                handler = group["hooks"][0]
                self.assertEqual(handler["type"], "command")
                self.assertIsInstance(handler["command"], str)
                self.assertTrue(handler["command"])
                self.assertEqual(handler["timeout"], 10)
                expected = [
                    marker + "/.altiora/system/scripts/guard.py",
                    "--runtime", "claude", "--project", marker, "--event", event,
                ]
                self.assertEqual(handler["args"], expected)
                for arg in handler["args"]:
                    self.assertNotIn("altiora-unificado", arg)
                    self.assertFalse(Path(arg).is_absolute())
                    self.assertFalse(PureWindowsPath(arg).is_absolute())
                handlers[event] = handler
        self.assertEqual(handlers["PreToolUse"]["onFailure"], "block")

        with tempfile.TemporaryDirectory(prefix="claude hook spaces ") as tmp:
            project = Path(tmp)
            script = project / ".altiora/system/scripts/guard.py"
            policy = project / ".altiora/policy.json"
            script.parent.mkdir(parents=True)
            script.write_bytes(
                (repo / ".altiora/system/scripts/guard.py").read_bytes()
            )
            policy.write_bytes((repo / ".altiora/policy.json").read_bytes())

            def run(event, name=None, substitute=True):
                args = handlers[event]["args"]
                if substitute:
                    args = [a.replace(marker, str(project)) for a in args]
                payload = {} if name is None else {
                    "tool_name": "Write",
                    "tool_input": {"file_path": str(project / name)},
                }
                return subprocess.run(
                    [sys.executable, *args], input=json.dumps(payload),
                    text=True, capture_output=True, timeout=10,
                    shell=False, cwd=project,
                )

            def output(event, name=None):
                result = run(event, name)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout)

            denied = output("PreToolUse", ".env")
            self.assertEqual(
                denied["hookSpecificOutput"]["permissionDecision"], "deny"
            )
            for name in (".env.example", "README.md"):
                self.assertEqual(output("PreToolUse", name), {})
            self.assertTrue(output("SessionStart")["hookSpecificOutput"]["additionalContext"])
            def assert_unopenable(result, fragment):
                # Python exit 2 because the script path cannot be opened, not another error.
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("can't open file", result.stderr)
                self.assertIn(fragment, result.stderr)

            assert_unopenable(run("PreToolUse", ".env", False), marker)
            saved = script.read_bytes()
            script.unlink()
            assert_unopenable(run("PreToolUse", ".env"), "guard.py")
            script.write_bytes(saved)
            self.assertEqual(output("PreToolUse", "README.md"), {})  # control: restored guard runs
            policy.unlink()
            denied = output("PreToolUse", "README.md")
            self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")


if __name__ == '__main__':
    unittest.main()
