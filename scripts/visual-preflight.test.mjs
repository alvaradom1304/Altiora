import test from "node:test";
import assert from "node:assert/strict";
import {probeExecutable, createReport, formatReport, blenderCandidates, detectBlender, probeNpm, probePython3} from "./visual-preflight.mjs";

test('Windows Blender discovery uses installed versions in numeric order without shell', () => {
  const paths = blenderCandidates({platform: 'win32', env: {ProgramFiles: 'C:\\Program Files'},
    list: () => ['Blender 5.9', 'Blender 5.10', 'Blender 5.2', 'other', 'Blender 5.99 beta']});
  assert.ok(paths[0].includes('Blender 5.10'));
  assert.ok(paths[1].includes('Blender 5.9'));
  assert.equal(paths.at(-1), 'blender');
  assert.ok(paths.every(p => !p.includes('beta') && !p.includes('other')));
});

test('installed Blender is detected after PATH failure; returned path is local evidence only', () => {
  const calls = [];
  const runner = (exe, args, options) => {
    calls.push(exe);
    assert.deepEqual(args, ['--version']);
    assert.equal(options.shell, false);
    return exe === 'blender' ? {error: {code: 'ENOENT'}} : {status: 0, stdout: 'Blender 5.2.2 LTS\n'};
  };
  const report = detectBlender(runner, ['C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe', 'blender']);
  assert.equal(report.status, 'AVAILABLE');
  assert.equal(report.version, 'Blender 5.2.2 LTS');
  assert.ok(report.executable.includes('Blender 5.2'));
  assert.equal(report.discovery, 'INSTALLATION_PATH');
  assert.deepEqual(calls, ['blender', 'C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe']);
});

test('an explicit Blender override never silently falls back to another version', () => {
  for (const value of ['relative/blender.exe', '\\\\server\\share\\blender.exe', 'C:\\path:alias\\blender.exe', 'C:\\tool\\other.exe']) {
    assert.throws(() => blenderCandidates({platform: 'win32', env: {ALTIORA_BLENDER: value}}));
  }
  const candidates = blenderCandidates({platform: 'win32', env: {ALTIORA_BLENDER: 'C:\\missing\\blender.exe'}, list: () => {throw Error('must not scan');}});
  assert.deepEqual(candidates, ['C:\\missing\\blender.exe']);
  const calls = [];
  const report = detectBlender(exe => {calls.push(exe); return {error: {code: 'ENOENT'}};}, candidates);
  assert.equal(report.status, 'NOT_FOUND');
  assert.deepEqual(calls, candidates);
});

test('a working PATH Blender remains authoritative without launching every installed version', () => {
  const calls = [];
  const result = detectBlender(exe => {calls.push(exe); return {status: 0, stdout: 'Blender 5.2\n'};}, ['C:\\other\\blender.exe', 'blender']);
  assert.equal(result.discovery, 'PATH');
  assert.deepEqual(calls, ['blender']);
});

test('failed Blender probes remain errors, discovery does not invoke renders', () => {
  const result = detectBlender(() => ({error: {code: 'ETIMEDOUT'}}), ['blender']);
  assert.equal(result.status, 'ERROR');
  assert.equal(result.executable, null);
  assert.deepEqual(blenderCandidates({platform: 'linux', env: {}, list: () => {throw Error('must not scan');}}), ['blender']);
});

test("executable found is not mistaken for connected plugin", () => {
  const stub = () => ({status: 0, stdout: "Blender 4.3.1\nBuild: ..."});
  const value = probeExecutable("Blender", "blender", ["--version"], stub);
  assert.deepEqual(value, {name:"Blender", status:"AVAILABLE", version:"Blender 4.3.1"});
});

test("ENOENT becomes not found without claiming absence from whole computer", () => {
  const stub = () => ({status: null, error:{code:"ENOENT"}});
  const value = probeExecutable("Blender", "blender", ["--version"], stub);
  assert.equal(value.status, "NOT_FOUND");
});

test("failed or timed-out commands report error, never available", () => {
  const stub = () => ({status: null, error:{code:"ETIMEDOUT"}});
  assert.equal(probeExecutable("FFmpeg", "ffmpeg", ["-version"], stub).status, "ERROR");
  assert.equal(probeExecutable("Git", "git", ["--version"], () => ({status: 1, stderr:"bad"})).status, "ERROR");
});

test("preflight never claims Adobe, Figma or MCP connected", async () => {
  const stub = (cmd, args) => ({status: 0, stdout: "VERSION\n"});
  const report = await createReport(stub);
  assert.equal(report.report_type, "local_visual_preflight");
  assert.equal(report.manual_checks.length, 3);
  assert.ok(report.manual_checks.every(x => x.status === "MANUAL_CHECK_REQUIRED"));
  assert.equal(report.tools.length, 6);
  assert.doesNotMatch(formatReport(report), /AUTOMATICALLY_CONNECTED|LINKED_AND_READY/);
});

test("no arbitrary commands can be passed as preflight probes", () => {
  assert.throws(() => probeExecutable("bad","x","; destructive command"), {name:"AssertionError"});
});

test("Windows: npm se detecta via cmd.exe y python3 cae a python si el atajo de Store falla", () => {
  const calls = [];
  const runner = (exe, args) => {
    calls.push(exe);
    if (exe === "cmd.exe") return {status: 0, stdout: "11.0.0"};
    if (exe === "python3") return {status: 9009, stderr: "Python was not found"};
    if (exe === "python") return {status: 0, stdout: "Python 3.12.10"};
    return {status: null, error: {code: "ENOENT"}};
  };
  assert.equal(probeNpm(runner, "win32").status, "AVAILABLE");
  const py = probePython3(runner, "win32");
  assert.equal(py.status, "AVAILABLE");
  assert.equal(py.command, "python");
  assert.ok(calls.includes("cmd.exe") && calls.includes("python3"));
});

test("Python 3 ausente en todos los alias se reporta sin inventar disponibilidad", () => {
  const none = () => ({status: null, error: {code: "ENOENT"}});
  assert.equal(probePython3(none, "linux").status, "NOT_FOUND");
});
