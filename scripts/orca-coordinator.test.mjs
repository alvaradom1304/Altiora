import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, mkdirSync, writeFileSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { route, loadConfig, pickReviewer, canAccept, checkOwnershipConflicts, buildWorkerStartArgs, handleLaunchFailure, pickModel, checkFlagsAgainstHelp, preflight, claimOwnership, releaseOwnership, checkLaunchOwnership, loadActive, observeEffective, findDispatchId, validateOwnership, readRegistry, markClaim, dropClaim, classifyLaunch, isTerminalDispatch, planInference, runInference, inferenceArgs, buildSpec } from './orca-coordinator.mjs';

// Las reglas del router usan una fixture explicita; no dependen de proveedores reales.
const cfg = structuredClone(loadConfig());
for (const agent of ['claude', 'codex']) {
  cfg.agents[agent].availability = { transports: {
    'orca-worker': { status: 'verified' },
    'external-review': { status: 'verified' },
  } };
}
cfg.agents.antigravity.model = null;
cfg.agents.antigravity.efforts = [];
delete cfg.agents.antigravity.modelsByEffort;
cfg.agents.antigravity.availability = { transports: { 'orca-worker': { status: 'unverified' } } };
const catalog = [{ slug: 'gpt-6.1-sol', visibility: 'list', supported_reasoning_levels: ['low', 'medium', 'high', 'xhigh', 'max'] }];
const O = { codexCatalog: catalog };
const F = ['docs/operations/x.md'];
const T = (o) => ({ id: 't1', size: 'substantial', files: F, ...o });

test('seleccion por dominio', () => {
  assert.equal(route(T({ text: 'Redacta copy y ajusta el css de la landing' }), cfg, O).agent, 'claude');
  assert.equal(route(T({ text: 'Corrige el bug del endpoint y agrega tests' }), cfg, O).agent, 'codex');
});
test('3D/WebGL: Antigravity sin prueba => respaldo Claude y se explica', () => {
  const r = route(T({ text: 'Crear shader webgl con gsap y scroll' }), cfg, O);
  assert.equal(r.agent, 'claude');
  assert.equal(r.fallbackUsed, true);
  assert.match(r.skipped[0], /antigravity.*unverified/);
});
test('Antigravity "disponible" pero sin modelo validado: no se inventa, respaldo', () => {
  const fixture = structuredClone(cfg);
  fixture.agents.antigravity.efforts = ['low', 'medium', 'high'];
  const r = route(T({ text: 'Crear shader webgl con gsap y scroll' }), fixture, { ...O, availability: { antigravity: { ok: true } } });
  assert.notEqual(r.agent, 'antigravity');
  assert.match(r.skipped.join(' '), /sin modelo configurado/);
});
test('riesgo/esfuerzo: seguridad => high; critical => xhigh; mecanico => low', () => {
  assert.equal(route(T({ text: 'Auditoria de seguridad OWASP del endpoint api' }), cfg, O).effort, 'high');
  assert.equal(route(T({ text: 'Auditoria de seguridad OWASP del endpoint api', risk: 'critical' }), cfg, O).effort, 'xhigh');
  assert.equal(route(T({ text: 'Corrige typo de formato en el script de tests' }), cfg, O).effort, 'low');
});
test('tarea chica => directo, sin delegar', () => {
  assert.equal(route({ id: 'a', size: 'small', text: 'Ajusta css del componente react' }, cfg, O).decision, 'direct');
});
test('abstencion: ambigua, sin senales, sin tamano', () => {
  assert.equal(route(T({ text: 'Mejora la web' }), cfg, O).decision, 'abstain');
  assert.equal(route(T({ text: 'Landing con copy y un bug en el endpoint api' }), cfg, O).decision, 'abstain');
  assert.equal(route({ id: 'a', text: 'copy landing', files: F }, cfg, O).decision, 'abstain');
});
test('rechazo: sin propiedad / ruta protegida / comodin / fuera de raiz', () => {
  const t = 'Redacta copy y ajusta el css de la landing';
  assert.equal(route(T({ text: t, files: [] }), cfg, O).decision, 'reject');
  assert.equal(route(T({ text: t, files: undefined }), cfg, O).decision, 'reject');
  for (const f of ['app/page.tsx', '.env.local', '../x.md', 'docs/*.md', '.claude/settings.json', 'projects/cliente/a.md'])
    assert.equal(route(T({ text: t, files: [f] }), cfg, O).decision, 'reject', f);
});
test('decision comercial/legal => humano, no equipo', () => {
  assert.equal(route(T({ text: 'Define el precio y el contrato del cliente con css' }), cfg, O).decision, 'human-decision');
});
test('accion externa exige aprobacion', () => {
  assert.equal(route(T({ text: 'Ajusta el copy de la landing y publicar en produccion' }), cfg, O).needsUserApproval, true);
});
test('fallo de proveedor: respaldo; todos caidos => rechazo', () => {
  const t = T({ text: 'Corrige el bug del endpoint y agrega tests' });
  const r = route(t, cfg, { ...O, availability: { codex: { ok: false, reason: 'sin cuota' } } });
  assert.equal(r.agent, 'claude');
  assert.match(r.skipped[0], /sin cuota/);
  assert.equal(route(t, cfg, { ...O, availability: { codex: { ok: false }, claude: { ok: false } } }).decision, 'reject');
});
test('catalogo: modelo ausente, ilegible o esfuerzo no soportado => no se usa', () => {
  assert.equal(pickModel('codex', 'medium', cfg, { codexCatalog: [] }).ok, false);
  assert.equal(pickModel('codex', 'medium', cfg, { codexCatalog: null }).ok, false);
  assert.equal(pickModel('codex', 'medium', cfg, { codexCatalog: [{ slug: 'gpt-6.1-sol', visibility: 'list', supported_reasoning_levels: ['low'] }] }).ok, false);
});
test('sin autoaprobacion: revisor distinto del implementador', () => {
  assert.equal(route(T({ text: 'Revisar tests del endpoint api', mode: 'review', implementer: 'codex', files: [] }), cfg, O).agent, 'claude');
  assert.equal(route(T({ text: 'Revisar tests del endpoint api', mode: 'review', files: [] }), cfg, O).decision, 'abstain');
  assert.equal(pickReviewer('claude', 'ux-copy-frontend', cfg, O).agent, 'codex');
  assert.notEqual(pickReviewer('codex', 'engineering-security-qa', cfg, O).agent, 'codex');
  assert.equal(canAccept({ implementer: 'claude', review: { reviewer: 'claude', verdict: 'PASS', evidence: 'x' } }).accepted, false);
  assert.equal(canAccept({ implementer: 'claude' }).accepted, false);
  assert.equal(canAccept({ implementer: 'claude', review: { reviewer: 'codex', verdict: 'PASS', evidence: '' } }).accepted, false);
  assert.equal(canAccept({ implementer: 'claude', review: { reviewer: 'codex', verdict: 'PASS', evidence: 'npm test ok' } }).accepted, true);
});
test('un escritor por archivo', () => {
  assert.equal(checkOwnershipConflicts([{ id: 'a', files: ['docs/a.md'] }, { id: 'b', files: ['docs/A.md'] }]).ok, false);
  assert.equal(checkOwnershipConflicts([{ id: 'a', files: ['docs/a.md'] }, { id: 'b', files: ['docs/b.md'] }]).ok, true);
});
test('worker-start: sin --model salvo que el usuario lo nombre; flags validos', () => {
  const plan = { agent: 'codex', domain: 'd', taskId: 't', model: 'gpt-6.1-sol', effort: 'high' };
  assert.equal(buildWorkerStartArgs(plan).includes('--model'), false);
  assert.equal(buildWorkerStartArgs(plan, { userNamedModel: true }).includes('--model'), true);
  assert.equal(checkFlagsAgainstHelp(['--agent', '--zzz'], '--agent').ok, false);
});
test('fallo de lanzamiento: no reintentar a ciegas', () => {
  const h = handleLaunchFailure({ failedStage: 'setup' });
  assert.equal(h.retry, false);
  assert.match(h.action, /setup/);
});

// ---- Correcciones QA 2026-11-09 -------------------------------------------------
const fakeRun = (handleLive) => (c, a) => {
  const k = `${c} ${a.join(' ')}`;
  if (k.startsWith('git rev-parse')) return { status: 0, stdout: `${cfg.root}\n` };
  if (k.includes('worker-start --help')) return { status: 0, stdout: '--spec-file --worktree --agent --task-title --json --model --effort' };
  if (k.startsWith('orca status')) return { status: 0, stdout: JSON.stringify({ result: { runtime: { reachable: true } } }) };
  if (k.startsWith('orca terminal show')) return { status: handleLive ? 0 : 1, stdout: JSON.stringify({ ok: handleLive, result: { terminal: { handle: a[a.indexOf('--terminal') + 1], connected: handleLive, writable: handleLive, orphaned: !handleLive } } }) };
  return { status: 1, stdout: '' };
};
const HANDLE = 'term_82ec7553-cf65-4e8a-b176-71563eba49eb';

test('QA1: sin ORCA_TERMINAL_HANDLE puede lanzar pero NO esta listo para ejecutar (sin retorno)', () => {
  const r = preflight({ cfg, opts: O, env: {}, run: fakeRun(true) });
  assert.equal(r.launchReady, true);
  assert.equal(r.returnReady, false);
  assert.equal(r.executeReady, false);
  assert.match(JSON.stringify(r.returnChecks), /AUSENTE/);
});
test('QA1: handle presente pero que no es un terminal vivo => no executeReady; handle vivo => executeReady', () => {
  assert.equal(preflight({ cfg, opts: O, env: { ORCA_TERMINAL_HANDLE: HANDLE }, run: fakeRun(false) }).executeReady, false);
  const ok = preflight({ cfg, opts: O, env: { ORCA_TERMINAL_HANDLE: HANDLE }, run: fakeRun(true) });
  assert.equal(ok.executeReady, true);
  assert.equal(JSON.stringify(ok).includes(HANDLE), false, 'el handle no se vuelca a la salida');
});
test('QA1: handle con formato invalido => no executeReady', () => {
  assert.equal(preflight({ cfg, opts: O, env: { ORCA_TERMINAL_HANDLE: 'abc' }, run: fakeRun(true) }).returnReady, false);
});

test('QA2: asignacion activa bloquea a un segundo escritor del mismo archivo (incl. variantes de ruta/mayusculas)', () => {
  const p = path.join(mkdtempSync(path.join(tmpdir(), 'own-')), 'active.json');
  const a = { taskId: 'A', agent: 'codex', ownerFiles: ['docs/a.md'] };
  assert.deepEqual(claimOwnership(a, p), { ok: true, claimed: true });
  for (const f of ['docs/a.md', 'docs/A.md', 'docs//a.md', 'docs/./a.md']) {
    const own = validateOwnership([f], cfg);
    const r = claimOwnership({ taskId: 'B', agent: 'claude', ownerFiles: own.files }, p);
    assert.equal(r.ok, false, f);
    assert.match(r.reason, /asignado a A y B/);
  }
  assert.equal(claimOwnership({ taskId: 'C', agent: 'claude', ownerFiles: ['docs/c.md'] }, p).ok, true);
  assert.deepEqual(Object.keys(loadActive(p)).sort(), ['A', 'C']);
});
test('QA2: liberar (dispatch terminal comprobado) permite a otro escritor', () => {
  const p = path.join(mkdtempSync(path.join(tmpdir(), 'own-')), 'active.json');
  assert.equal(claimOwnership({ taskId: 'A', agent: 'codex', ownerFiles: ['docs/a.md'] }, p).ok, true);
  assert.equal(markClaim('A', { state: 'launched', dispatch: 'disp_A' }, p).ok, true);
  assert.equal(checkLaunchOwnership({ taskId: 'B', ownerFiles: ['docs/a.md'] }, readRegistry(p)).ok, false);
  const running = () => ({ status: 0, stdout: JSON.stringify({ ok: true, result: { dispatchId: 'disp_A', state: 'running', stage: 'working' } }) });
  assert.equal(releaseOwnership('A', p, { run: running }).ok, false, 'dispatch activo: no se libera');
  const done = () => ({ status: 0, stdout: JSON.stringify({ ok: true, result: { dispatchId: 'disp_A', state: 'succeeded', stage: 'settled' } }) });
  assert.deepEqual(releaseOwnership('A', p, { run: done }), { ok: true, released: true });
  assert.equal(claimOwnership({ taskId: 'B', agent: 'claude', ownerFiles: ['docs/a.md'] }, p).ok, true);
});

// ---- Recheck Codex: regresiones aisladas (sin red ni workers) -----------------
function isolated(t, prefix = 'coord-recheck-') {
  const dir = mkdtempSync(path.join(tmpdir(), prefix));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
}
const claim = (taskId = 'a') => ({ taskId, agent: 'claude', ownerFiles: ['docs/a.md'] });
const settledReceipt = (dispatchId = 'ctx_exact') => ({ ok: true, result: {
  dispatchId, taskId: 'task_exact', runId: 'run_exact', state: 'succeeded', stage: 'settled',
  liveness: 'live', activity: 'idle', terminal: 'term_retained', terminalState: 'retained',
  projection: { id: dispatchId, dispatchId, resources: [{ state: 'running' }] },
} });

test('registro ausente es vacio; corrupto, ilegible o esquema invalido bloquea sin reemplazarlo', (t) => {
  const dir = isolated(t);
  const p = path.join(dir, 'active.json');
  assert.deepEqual(readRegistry(p), { ok: true, active: {}, exists: false });
  for (const raw of ['{invalid', '[]', 'null', '{"a":{}}', '{"a":{"files":[7],"state":"claimed","claimedAt":"now"}}', '{"a":{"files":[],"state":"running","claimedAt":"now"}}']) {
    writeFileSync(p, raw);
    assert.equal(readRegistry(p).ok, false, raw);
    assert.throws(() => loadActive(p));
    assert.equal(claimOwnership(claim(), p).ok, false);
    assert.equal(readFileSync(p, 'utf8'), raw, 'no borrar ni reemplazar evidencia corrupta');
  }
  const unreadable = path.join(dir, 'directory.json');
  mkdirSync(unreadable);
  assert.equal(readRegistry(unreadable).ok, false);
  assert.equal(claimOwnership(claim(), unreadable).ok, false);
});

test('IDs reservados no alteran prototipo ni se aceptan desde JSON existente', (t) => {
  const p = path.join(isolated(t), 'active.json');
  for (const id of ['__proto__', 'constructor', 'prototype', 'toString', 'hasOwnProperty', '', ' padded ']) {
    assert.equal(claimOwnership(claim(id), p).ok, false, id);
    assert.equal(claimOwnership(claim(id), p).ok, false, `${id} repetido`);
  }
  assert.deepEqual(readRegistry(p).active, {});
  writeFileSync(p, '{"__proto__":{"files":[],"state":"claimed","claimedAt":"now"}}');
  assert.equal(readRegistry(p).ok, false);
  assert.equal(claimOwnership(claim('normal'), p).ok, false);
});

test('fallos inciertos conservan claim y exigen conciliacion; fallo limpio requiere evidencia explicita', (t) => {
  const p = path.join(isolated(t), 'active.json');
  assert.equal(claimOwnership(claim(), p).ok, true);
  for (const result of [
    { status: 1, stdout: JSON.stringify({ status: 'failed', failedStage: 'launch' }) },
    { status: 1, stdout: '{broken' }, { status: null, stdout: '' },
    { status: 1, error: new Error('spawn failed'), stdout: '' },
    { status: 1, stdout: JSON.stringify({ status: 'failed', failedStage: 'launch', residualResources: ['worker'] }) },
    { status: 1, stdout: JSON.stringify({ status: 'outcome_unknown', failedStage: 'launch', residualResources: [] }) },
  ]) {
    assert.equal(classifyLaunch(result).kind, 'uncertain');
    assert.equal(markClaim('a', { state: 'unknown-launch' }, p).ok, true);
    assert.equal(releaseOwnership('a', p).ok, false);
    assert.equal(claimOwnership(claim(), p).ok, false);
  }
  assert.equal(classifyLaunch({ status: 1, stdout: JSON.stringify({ status: 'failed', failedStage: 'setup', residualResources: [] }) }).kind, 'failed-clean');
  assert.equal(classifyLaunch({ status: 0, stdout: '{}' }).kind, 'launched');
  assert.deepEqual(releaseOwnership('a', p, { reconciled: true }), { ok: true, released: true });
});

test('directorios/protegidos exactos y archivo nuevo bajo junction externa se rechazan', (t) => {
  const base = isolated(t);
  const root = path.join(base, 'root');
  const external = path.join(base, 'external');
  mkdirSync(path.join(root, 'docs'), { recursive: true });
  mkdirSync(external);
  symlinkSync(external, path.join(root, 'linked'), process.platform === 'win32' ? 'junction' : 'dir');
  for (const f of ['app', 'components', 'lib', 'public', 'projects', '.github', 'docs', 'docs/', 'linked/new.md', 'linked/missing/new.md']) {
    assert.equal(validateOwnership([f], cfg, root).ok, false, f);
  }
  assert.deepEqual(validateOwnership(['docs/new.md'], cfg, root), { ok: true, files: ['docs/new.md'] });
});

test('junction interna canonicaliza archivos existentes/nuevos y detecta segundo escritor por alias', (t) => {
  const root = isolated(t);
  mkdirSync(path.join(root, 'docs'));
  mkdirSync(path.join(root, 'app'));
  writeFileSync(path.join(root, 'docs', 'existing.md'), 'test');
  symlinkSync(path.join(root, 'docs'), path.join(root, 'alias'), process.platform === 'win32' ? 'junction' : 'dir');
  symlinkSync(path.join(root, 'app'), path.join(root, 'product-alias'), process.platform === 'win32' ? 'junction' : 'dir');
  for (const file of ['existing.md', 'new.md', 'missing/new.md']) {
    assert.deepEqual(validateOwnership([`alias/${file}`], cfg, root), { ok: true, files: [`docs/${file}`] });
    assert.equal(checkOwnershipConflicts([{ id: 'a', files: [`alias/${file}`] }, { id: 'b', files: [`docs/${file}`] }], root).ok, false);
  }
  assert.equal(validateOwnership(['product-alias/new.md'], cfg, root).ok, false);
});

test('release usa shape real y dispatch exacto; retained/live no bloquean trabajo succeeded/settled', (t) => {
  const p = path.join(isolated(t), 'active.json');
  claimOwnership(claim(), p);
  markClaim('a', { state: 'launched', dispatch: 'ctx_exact' }, p);
  const real = settledReceipt();
  assert.equal(isTerminalDispatch(real, 'ctx_exact'), true);
  const invalid = [
    settledReceipt('ctx_other'), { ...real, ok: false },
    { ok: true, result: { ...real.result, state: 'running' } },
    { ok: true, result: { ...real.result, stage: 'working' } },
    { ok: true, result: { ...real.result, state: 'outcome_unknown' } },
    { ok: true, result: { state: 'succeeded', stage: 'settled' } },
    { ok: true, result: { dispatch: { dispatchId: 'ctx_exact', state: 'succeeded', stage: 'settled' } } },
    { ok: true, result: { dispatchId: 'ctx_exact', state: 'running', stage: 'working', unrelated: { status: 'completed' } } },
  ];
  for (const receipt of invalid) {
    assert.equal(releaseOwnership('a', p, { run: () => ({ status: 0, stdout: JSON.stringify(receipt) }) }).ok, false);
    assert.equal(readRegistry(p).active.a.dispatch, 'ctx_exact');
  }
  assert.equal(releaseOwnership('a', p, { run: () => ({ status: 1, stdout: JSON.stringify(real) }) }).ok, false);
  assert.deepEqual(releaseOwnership('a', p, { run: (command, args) => {
    assert.equal(command, 'orca');
    assert.deepEqual(args, ['orchestration', 'worker-show', '--dispatch', 'ctx_exact', '--json']);
    return { status: 0, stdout: JSON.stringify(real) };
  } }), { ok: true, released: true });
  assert.deepEqual(readRegistry(p).active, {});
});

const inferenceTask = (patch = {}) => ({ id: 'infer-check', text: 'Respond exactly ALTIORA_COORD_OMNI_OK', transport: 'omniroute', mode: 'inference', ...patch });
test('inferencia explicita limita modo, archivos, prompt, modelo, tokens y catalogo', () => {
  const good = planInference(inferenceTask(), cfg);
  assert.deepEqual([good.decision, good.agentic, good.tools, good.executed], ['inference', false, false, false]);
  for (const patch of [
    { mode: 'write' }, { mode: 'review' }, { transport: 'orca' }, { files: ['docs/a.md'] },
    { files: 'docs/a.md' }, { text: '' }, { text: 'x'.repeat(cfg.omniroute.maxPromptChars + 1) },
    { id: '__proto__' }, { model: 'unknown' }, { maxTokens: 0 }, { maxTokens: 1.2 }, { maxTokens: cfg.omniroute.maxTokens + 1 },
  ]) assert.equal(planInference(inferenceTask(patch), cfg).decision, 'reject', JSON.stringify(patch).slice(0, 150));
  assert.equal(planInference(inferenceTask(), cfg, { omnirouteCatalog: [] }).decision, 'reject');
  assert.equal(route(inferenceTask({ transport: undefined }), cfg).decision, 'reject');
});

test('transporte infer pasa prompt solo por stdin y separa modelo pedido/reportado sin herramientas', () => {
  const task = inferenceTask();
  const plan = planInference(task, cfg);
  let calls = 0;
  const result = runInference(plan, task.text, cfg, (command, args, input, timeout) => {
    calls++;
    assert.equal(command, cfg.omniroute.python);
    assert.deepEqual(args, inferenceArgs(plan, cfg));
    assert.equal(args.includes(task.text), false);
    assert.equal(input, task.text);
    assert.equal(timeout, cfg.omniroute.timeoutSec);
    return { status: 0, stdout: JSON.stringify({ status: 'PASS', requested_model: plan.model, reported_model: 'gpt-6-luna-low', http: 200, response: 'ALTIORA_COORD_OMNI_OK' }) };
  });
  assert.equal(calls, 1);
  assert.equal(result.ok, true);
  assert.equal(result.response, 'ALTIORA_COORD_OMNI_OK');
  assert.equal(result.requestedModel, 'cxa/gpt-6-luna-low');
  assert.equal(result.reportedModel, 'gpt-6-luna-low');
  const notObserved = runInference(plan, task.text, cfg, () => ({ status: 0, stdout: JSON.stringify({ status: 'PASS', response: 'ok' }) }));
  assert.equal(notObserved.reportedModel, null);
});

test('inferencia no reintenta y rechaza fallo/catalogo/respuesta invalida', () => {
  const task = inferenceTask();
  const plan = planInference(task, cfg);
  for (const output of [
    { status: 1, stderr: JSON.stringify({ error: 'modelo ausente', error_type: 'catalog' }) },
    { status: null, error: new Error('timeout') }, { status: 0, stdout: '{bad' },
    { status: 0, stdout: '{"status":"FAIL","response":"no"}' },
    { status: 0, stdout: '{"status":"PASS","response":" "}' },
  ]) {
    let calls = 0;
    assert.equal(runInference(plan, task.text, cfg, () => { calls++; return output; }).ok, false);
    assert.equal(calls, 1);
  }
});
test('QA-02: el mismo ID activo NO se reclama dos veces (ni siquiera con otros archivos)', () => {
  const p = path.join(mkdtempSync(path.join(tmpdir(), 'own-')), 'active.json');
  const a = { taskId: 'qa-same', agent: 'claude', ownerFiles: ['docs/operations/a.md'] };
  assert.deepEqual(claimOwnership(a, p), { ok: true, claimed: true });
  const again = claimOwnership(a, p);
  assert.equal(again.ok, false);
  assert.match(again.reason, /ID activo duplicado/);
  assert.equal(claimOwnership({ ...a, ownerFiles: ['docs/operations/z.md'] }, p).ok, false);
  assert.deepEqual(Object.keys(loadActive(p)), ['qa-same']);
});
test('QA-02: solo lectura tambien registra ID; solicitudes en carrera: gana una y la otra se rechaza', () => {
  const p = path.join(mkdtempSync(path.join(tmpdir(), 'own-')), 'active.json');
  assert.deepEqual(claimOwnership({ taskId: 'R', ownerFiles: [] }, p), { ok: true, claimed: true });
  assert.equal(claimOwnership({ taskId: 'R', ownerFiles: [] }, p).ok, false);
  writeLock(p); // otra solicitud "concurrente" sostiene el bloqueo
  const rr = claimOwnership({ taskId: 'R2', ownerFiles: [] }, p);
  assert.equal(rr.ok, false);
  assert.match(rr.reason, /bloqueado/);
  rmSync(`${p}.lock`);
  const p2 = path.join(mkdtempSync(path.join(tmpdir(), 'own-')), 'active.json');
  const res = [claimOwnership({ taskId: 'X', agent: 'a', ownerFiles: ['docs/x.md'] }, p2), claimOwnership({ taskId: 'Y', agent: 'b', ownerFiles: ['docs/x.md'] }, p2)];
  assert.deepEqual(res.map((r) => r.ok), [true, false]);
});
test('QA2: registro bloqueado => rechazo sin reintento ciego', () => {
  const p = path.join(mkdtempSync(path.join(tmpdir(), 'own-')), 'active.json');
  writeLock(p);
  const r = claimOwnership({ taskId: 'X', agent: 'codex', ownerFiles: ['docs/x.md'] }, p);
  assert.equal(r.ok, false);
  assert.match(r.reason, /bloqueado/);
});
function writeLock(p) { writeFileSyncSafe(`${p}.lock`, ''); }
import { writeFileSync as writeFileSyncSafe } from 'node:fs';

test('QA3: el plan nunca declara modelo efectivo; solo el recibo de Orca lo observa', () => {
  const plan = route(T({ text: 'Corrige el bug del endpoint y agrega tests' }), cfg, O);
  assert.equal(plan.effectiveModel, null);
  assert.match(plan.modelStatus, /NO confirmado/);
  assert.equal(buildWorkerStartArgs(plan).includes('--model'), false);
  const none = observeEffective({ result: { dispatch: { id: 'x', status: 'ready' } } }, plan);
  assert.equal(none.observed, false);
  const same = observeEffective({ result: { worker: { startOptions: { launch: { effective: { model: 'gpt-6.1-sol', effort: 'high' } } } } } }, plan);
  assert.deepEqual([same.observed, same.model, same.effort, same.matchesPreference], [true, 'gpt-6.1-sol', 'high', true]);
  const diff = observeEffective({ result: { worker: { startOptions: { launch: { effective: { model: 'otro-modelo' } } } } } }, plan);
  assert.equal(diff.matchesPreference, false);
  assert.match(diff.note, /difiere/);
  assert.equal(findDispatchId({ result: { dispatchId: 'disp_1' } }), 'disp_1');
});

// Disponibilidad por transporte: CLI util no equivale a worker disponible.
function blockedWorkerConfig() {
  const c = structuredClone(cfg);
  c.agents.codex.capabilities = { cli: { status: 'verified' } };
  c.agents.codex.availability.transports['orca-worker'] = { status: 'blocked', evidence: 'agent-hooks-review-prompt' };
  return c;
}
test('worker Codex bloqueado con CLI verificado: engineering usa Claude y explica respaldo', () => {
  const c = blockedWorkerConfig();
  const r = route(T({ text: 'Corrige el bug del endpoint y agrega tests' }), c, O);
  assert.equal(r.agent, 'claude');
  assert.equal(r.fallbackUsed, true);
  assert.match(r.skipped.join(' '), /codex\/orca-worker.*blocked.*agent-hooks-review-prompt/);
  assert.equal(r.reviewRequired, true);
  assert.equal(r.effectiveModel, null);
});
test('revisor externo Codex independiente conservado; review Orca no usa un worker bloqueado', () => {
  const c = blockedWorkerConfig();
  const reviewer = pickReviewer('claude', 'engineering-security-qa', c, O);
  assert.equal(reviewer.agent, 'codex');
  assert.equal(reviewer.transport, 'external-review');
  assert.equal(reviewer.launchable, false);
  assert.equal(route(T({ text: 'Revision del endpoint api', mode: 'review', implementer: 'claude' }), c, O).decision, 'reject');
  assert.equal(route(T({ text: 'Revision del endpoint api', mode: 'review', implementer: 'claude' }), c, { ...O, transport: 'external-review' }).decision, 'reject', 'no convertir una revision externa en worker');
  assert.equal(pickReviewer('codex', 'engineering-security-qa', c, O).agent, 'claude');
  assert.equal(canAccept({ implementer: 'claude', review: { reviewer: 'claude', verdict: 'PASS', evidence: 'tests' } }).accepted, false);
});
test('preflight permite un worker elegible y rechaza cero: no exige todos los proveedores', () => {
  const c = blockedWorkerConfig();
  const args = { cfg: c, opts: O, env: { ORCA_TERMINAL_HANDLE: HANDLE }, run: fakeRun(true) };
  const ready = preflight(args);
  assert.equal(ready.executeReady, true);
  assert.equal(ready.checks.find(x => x.name === 'codex: worker seleccionable').pass, false);
  assert.equal(preflight({ ...args, env: {} }).executeReady, false, 'retorno propio sigue obligatorio');
  c.agents.claude.availability.transports['orca-worker'].status = 'blocked';
  const unavailable = preflight(args);
  assert.equal(unavailable.launchReady, false);
  assert.equal(unavailable.executeReady, false);
});
test('disponibilidad general legacy y CLI verified nunca habilitan un worker', () => {
  const c = blockedWorkerConfig();
  c.agents.codex.availability = { status: 'verified' };
  assert.equal(route(T({ text: 'Corrige el bug del endpoint y agrega tests' }), c, O).agent, 'claude');
});

test('QA retorno: ok true no acredita coordinador conectado y escribible del handle exacto', () => {
  const healthy = { handle: HANDLE, connected: true, writable: true, orphaned: false };
  const fixture = (terminal, extra = {}) => (c, a) => a[0] === 'terminal'
    ? { status: 0, stdout: JSON.stringify({ ok: true, result: { terminal }, ...extra }) }
    : fakeRun(true)(c, a);
  const check = (terminal, extra) => preflight({ cfg, opts: O, env: { ORCA_TERMINAL_HANDLE: HANDLE }, run: fixture(terminal, extra) });
  assert.equal(check(healthy).executeReady, true);
  for (const terminal of [
    { ...healthy, orphaned: true, connected: false, writable: false },
    { ...healthy, connected: false }, { ...healthy, writable: false },
    { ...healthy, orphaned: true }, { ...healthy, orphaned: undefined },
    { ...healthy, connected: undefined }, { ...healthy, writable: undefined },
    { ...healthy, handle: 'term_00000000-0000-0000-0000-000000000000' },
    { ...healthy, handle: undefined }, undefined, null,
  ]) {
    const result = check(terminal);
    assert.equal(result.launchReady, true, 'el fallo pertenece al canal de retorno');
    assert.equal(result.returnReady, false, JSON.stringify(terminal));
    assert.equal(result.executeReady, false);
  }
  assert.equal(check(healthy, { ok: false }).returnReady, false);
});

function agyCatalogFixture() {
  const c = structuredClone(cfg);
  c.agents.antigravity = {
    model: 'gemini-3.8-flash-medium', efforts: ['low', 'medium', 'high'],
    modelsByEffort: { low: 'gemini-3.8-flash-low', medium: 'gemini-3.8-flash-medium', high: 'gemini-4-argon-high' },
    capabilities: { cli: { status: 'verified' } },
    availability: { transports: { 'orca-worker': { status: 'unverified' } } },
  };
  return c;
}
test('Antigravity CLI/catalogo verificados no habilitan worker; 3D conserva respaldo', () => {
  const c = agyCatalogFixture();
  const result = route(T({ text: 'Crear shader webgl con gsap y scroll' }), c, O);
  assert.equal(result.agent, 'claude');
  assert.equal(result.fallbackUsed, true);
  assert.match(result.skipped.join(' '), /antigravity\/orca-worker.*unverified/);
});
test('Antigravity elige preferencia tras normalizar esfuerzo, grande solo high', () => {
  const c = agyCatalogFixture();
  for (const [effort, model] of Object.entries(c.agents.antigravity.modelsByEffort)) {
    const result = pickModel('antigravity', effort, c);
    assert.equal(result.model, model);
    assert.equal(result.effort, effort);
    assert.match(result.status, /preferencia/);
  }
  assert.deepEqual(pickModel('antigravity', 'xhigh', c), pickModel('antigravity', 'high', c));
});
test('spec Antigravity exige contexto vigente en cada delegacion, sin snapshot', () => {
  const plan = { taskId: 'agy-fixture', domain: 'immersive-3d-motion', agent: 'antigravity', ownerFiles: ['docs/example.md'], roles: ['web-engineer'], effort: 'medium', evidenceRequired: ['evidencia'] };
  const spec = buildSpec(plan, { text: 'Encargo fixture' });
  for (const source of ['GEMINI.md', 'AGENTS.md', 'docs/operations/ESTADO-ACTUAL.md', '.altiora/coordinator.json', 'git rev-parse --show-toplevel']) assert.ok(spec.includes(source), source);
  assert.ok(spec.includes('referencias vivas'));
  assert.ok(spec.includes('QA independiente'));
  assert.equal(buildWorkerStartArgs(plan).includes('--model'), false);
  assert.equal(buildSpec({ ...plan, agent: 'claude' }, { text: 'Encargo fixture' }).includes('Contexto Altiora vigente:'), false);
});

test('Antigravity worker verificado primero en 3D; blocked conserva fallback Claude', () => {
  const c = agyCatalogFixture();
  c.agents.antigravity.availability.transports['orca-worker'].status = 'verified';
  const task = T({ text: 'Crear shader webgl con gsap y scroll' });
  const primary = route(task, c, O);
  assert.equal(primary.agent, 'antigravity');
  assert.equal(primary.fallbackUsed, false);
  assert.equal(primary.model, 'gemini-4-argon-high');
  assert.equal(primary.effectiveModel, null);
  assert.equal(primary.reviewRequired, true);
  c.agents.antigravity.availability.transports['orca-worker'].status = 'blocked';
  const fallback = route(task, c, O);
  assert.equal(fallback.agent, 'claude');
  assert.equal(fallback.fallbackUsed, true);
  assert.match(fallback.skipped.join(' '), /antigravity\/orca-worker.*blocked/);
});
test('Antigravity ultimo respaldo UX e ingenieria con Codex/Claude no elegibles', () => {
  const c = agyCatalogFixture();
  c.domains['ux-copy-frontend'].chain = ['claude', 'codex', 'antigravity'];
  c.domains['engineering-security-qa'].chain = ['codex', 'claude', 'antigravity'];
  c.agents.antigravity.availability.transports['orca-worker'].status = 'verified';
  const unavailable = { ...O, availability: { codex: { ok: false }, claude: { ok: false } } };
  for (const domain of ['ux-copy-frontend', 'engineering-security-qa']) {
    const result = route(T({ text: 'Encargo de respaldo', domain }), c, unavailable);
    assert.equal(result.agent, 'antigravity');
    assert.equal(result.fallbackUsed, true);
    assert.equal(result.skipped.length, 2);
    assert.equal(result.model, 'gemini-3.8-flash-medium');
    assert.equal(result.effectiveModel, null);
  }
  const invalid = structuredClone(c);
  invalid.agents.codex.model = null;
  invalid.agents.claude.model = null;
  assert.equal(route(T({ text: 'Encargo de respaldo', domain: 'engineering-security-qa' }), invalid, O).agent, 'antigravity');
});

test('modelo efectivo: requested/plan/metadata y effective null nunca acreditan ejecucion', () => {
  for (const record of [
    { requested: { model: 'haiku', effort: 'low' } },
    { model: 'haiku', effort: 'low', plan: { model: 'sonnet' }, metadata: { model: 'gemini' } },
    { result: { agent: { model: 'haiku' } } },
    { result: { worker: { startOptions: { launch: { requested: { model: 'haiku' }, effective: null } } } } },
    { result: { worker: { startOptions: { launch: { effective: { model: ' ', effort: 'high' } } } } } },
  ]) {
    const observed = observeEffective(record, { model: 'haiku' });
    assert.equal(observed.observed, false);
    assert.equal(observed.model, null);
    assert.equal(observed.status, 'no_observado');
    assert.equal(observed.source, null);
  }
});
test('modelo efectivo: path Orca exacto gana a valores conflictivos y conserva procedencia', () => {
  const record = { model: 'parent-ui', metadata: { model: 'wrong' }, result: { worker: { startOptions: { launch: {
    requested: { model: 'haiku', effort: 'low' }, effective: { model: 'actual-worker', effort: 'high' },
  } } } } };
  const observed = observeEffective(record, { model: 'haiku' });
  assert.equal(observed.model, 'actual-worker');
  assert.equal(observed.effort, 'high');
  assert.equal(observed.matchesPreference, false);
  assert.equal(observed.source, 'result.worker.startOptions.launch.effective.model');
  assert.equal(observed.effortSource, 'result.worker.startOptions.launch.effective.effort');
  assert.equal(observeEffective({ ...record, ok: false }).observed, false);
});
test('spec de las tres IAs referencia contrato local vigente sin imponer JSON', () => {
  for (const agent of ['codex', 'claude', 'antigravity']) {
    const spec = buildSpec({ agent, taskId: 'contract', domain: 'test', ownerFiles: [], roles: [], effort: 'low', evidenceRequired: [] }, { text: 'fixture' });
    assert.ok(spec.includes('docs/operations/AI-REPORT-CONTRACT.md'));
    assert.ok(spec.includes('modelo planeado separado'));
    assert.ok(spec.includes('JSON solo si el handoff lo necesita'));
    assert.ok(spec.includes('workspace/repositorio saneado'));
  }
});

test('alias de dominios de team/ROUTING.md: solo equivalentes, sin cambiar la cadena', () => {
  const c = agyCatalogFixture();
  c.domainAliases = { 'brand-copy-frontend': 'ux-copy-frontend', 'immersive-3d-qa': 'immersive-3d-motion' };
  const a = route(T({ text: 'Encargo de marca', domain: 'brand-copy-frontend' }), c, O);
  assert.equal(a.domain, 'ux-copy-frontend');
  assert.equal(a.requestedDomain, 'brand-copy-frontend');
  assert.equal(a.agent, route(T({ text: 'Encargo de marca', domain: 'ux-copy-frontend' }), c, O).agent);
  assert.equal(route(T({ text: 'Encargo 3D', domain: 'immersive-3d-qa' }), c, O).domain, 'immersive-3d-motion');
  for (const d of ['strategy-finance-backend', 'cloud-data-engineering']) {
    const r = route(T({ text: 'Encargo', domain: d }), c, O);
    assert.equal(r.decision, 'abstain');
    assert.match(r.reason, new RegExp(`dominio desconocido: ${d}`));
  }
});
