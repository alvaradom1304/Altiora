#!/usr/bin/env node
// Orquestador de Altiora: router heuristico + preflight + lanzamiento Orca (worker-start).
// Sin dependencias. NO clasifica a la perfeccion: ante ambiguedad material se ABSTIENE.
// No usa scripts antiguos del toolkit ni ALTIORA_DISPATCH_EXECUTE. Lanza solo con --execute --approved.
import { readFileSync, writeFileSync, existsSync, openSync, closeSync, unlinkSync, mkdirSync, statSync, lstatSync, realpathSync, renameSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
export const loadConfig = (p = path.join(ROOT, '.altiora', 'coordinator.json')) => JSON.parse(readFileSync(p, 'utf8'));

const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
const hits = (text, kws) => kws.filter((k) => new RegExp(`(^|[^a-z0-9])${norm(k).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`).test(text));
const ok = (o) => ({ decision: 'delegate', ...o });
const refuse = (decision, reason, extra = {}) => ({ decision, reason, ...extra });
const RESERVED_IDS = new Set([...Object.getOwnPropertyNames(Object.prototype), 'prototype']);
const validTaskId = (id) => typeof id === 'string' && !!id.trim() && id === id.trim() && !RESERVED_IDS.has(id);

// Incluso un archivo NUEVO puede estar bajo una junction. Resolver el primer ancestro existente
// antes de recomponer el sufijo evita que ENOENT se interprete como una ruta local segura.
function canonicalPath(abs) {
  let ancestor = abs;
  const suffix = [];
  for (;;) {
    try { lstatSync(ancestor); break; } catch (e) {
      if (e.code !== 'ENOENT') throw e;
      const parent = path.dirname(ancestor);
      if (parent === ancestor) throw e;
      suffix.unshift(path.basename(ancestor));
      ancestor = parent;
    }
  }
  return path.resolve(realpathSync(ancestor), ...suffix);
}

// ---- propiedad de archivos -------------------------------------------------
// QA-03: la propiedad son ARCHIVOS concretos. Se rechazan directorios (con o sin barra, existentes en
// disco), nombres protegidos exactos ("app" igual que "app/"), caracteres de comodin/flujo alterno y
// enlaces cuyo destino real salga de la raiz o caiga en ruta protegida.
export function validateOwnership(files, cfg, root = ROOT) {
  if (!Array.isArray(files) || files.length === 0) return { ok: false, reason: 'sin propiedad de archivos' };
  const protectedHit = (n) => cfg.forbiddenPathPatterns.find((p) => { const re = new RegExp(p, 'i'); return re.test(n) || re.test(`${n}/`); });
  const clean = [];
  for (const f of files) {
    if (typeof f !== 'string') return { ok: false, reason: `ruta no valida (no es texto): ${String(f)}` };
    const raw = f.replace(/\\/g, '/');
    if (!raw.trim() || path.isAbsolute(raw) || /^[a-z]:/i.test(raw) || raw.split('/').includes('..')) return { ok: false, reason: `ruta fuera de la raiz: ${f}` };
    if (/[*?<>|"]/.test(raw) || raw.includes(':')) return { ok: false, reason: `comodin o caracter no permitido (propiedad debe ser concreta): ${f}` };
    if (raw.endsWith('/')) return { ok: false, reason: `directorio no permitido (propiedad debe ser un archivo): ${f}` };
    const n = path.posix.normalize(raw); // docs//a.md y docs/./a.md se reducen a docs/a.md
    if (!n || n === '.') return { ok: false, reason: `ruta fuera de la raiz: ${f}` };
    const bad = protectedHit(n);
    if (bad) return { ok: false, reason: `ruta protegida (${bad}): ${f}` };
    const abs = path.resolve(root, n);
    const rel = path.relative(root, abs);
    if (rel.startsWith('..') || path.isAbsolute(rel)) return { ok: false, reason: `ruta fuera de la raiz: ${f}` };
    if (existsSync(abs)) {
      let st;
      try { st = statSync(abs); } catch { return { ok: false, reason: `ruta ilegible: ${f}` }; }
      if (st.isDirectory()) return { ok: false, reason: `es un directorio, no un archivo: ${f}` };
      if (!st.isFile()) return { ok: false, reason: `no es un archivo regular: ${f}` };
    }
    try {
      const real = path.relative(realpathSync(root), canonicalPath(abs)).replace(/\\/g, '/');
      if (real === '..' || real.startsWith('../') || path.isAbsolute(real)) return { ok: false, reason: `enlace que sale de la raiz: ${f}` };
      const bad2 = protectedHit(real);
      if (bad2) return { ok: false, reason: `el destino real cae en ruta protegida (${bad2}): ${f}` };
      clean.push(real); // aliases reales reclaman el mismo archivo
    } catch { return { ok: false, reason: `no se pudo resolver la ruta real: ${f}` }; }
  }
  return { ok: true, files: clean };
}

// Un escritor por archivo: dos tareas concurrentes no pueden compartir propiedad.
const ownKey = (f, root) => canonicalPath(path.resolve(root, String(f).replace(/\\/g, '/'))).replace(/\\/g, '/').toLowerCase();
export function checkOwnershipConflicts(tasks, root = ROOT) {
  const seen = new Map();
  for (const t of tasks) for (const f of t.files || []) {
    let k;
    try { k = ownKey(f, root); } catch { return { ok: false, reason: `propiedad no resoluble: ${f}` }; }
    if (seen.has(k) && seen.get(k) !== t.id) return { ok: false, reason: `archivo ${f} asignado a ${seen.get(k)} y ${t.id}` };
    seen.set(k, t.id);
  }
  return { ok: true };
}

// Registro de asignaciones ACTIVAS: `launch` lo consulta y reclama de forma atomica (bloqueo exclusivo)
// ANTES de lanzar cualquier worker (tambien los de solo lectura: un ID activo no se lanza dos veces).
// Estados: claimed (reclamado, aun sin lanzar) | launched (Orca confirmo) | unknown-launch (fallo incierto:
// pudo haber arrancado). Los claims NO se liberan a ciegas: `release` exige dispatch terminal comprobado o
// conciliacion humana explicita (--reconciled).
const ACTIVE_FILE = path.join(ROOT, '.altiora', 'active-ownership.json');
const CLAIM_STATES = ['claimed', 'launched', 'unknown-launch'];

// QA-01: inexistente => vacio; ilegible, corrupto o con esquema invalido => ERROR (bloquea el lanzamiento).
export function validateRegistry(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) return { ok: false, reason: 'la raiz debe ser un objeto {taskId: claim}' };
  for (const [id, e] of Object.entries(data)) {
    if (!validTaskId(id)) return { ok: false, reason: 'taskId vacio, reservado o no valido' };
    if (!e || typeof e !== 'object' || Array.isArray(e)) return { ok: false, reason: `${id}: claim no es objeto` };
    if (!Array.isArray(e.files) || !e.files.every((f) => typeof f === 'string' && f.trim())) return { ok: false, reason: `${id}: files debe ser lista de rutas` };
    if (!CLAIM_STATES.includes(e.state)) return { ok: false, reason: `${id}: state invalido` };
    if (typeof e.claimedAt !== 'string' || !e.claimedAt) return { ok: false, reason: `${id}: claimedAt ausente` };
    if (e.dispatch !== undefined && (typeof e.dispatch !== 'string' || !e.dispatch.trim())) return { ok: false, reason: `${id}: dispatch invalido` };
    if (e.agent !== undefined && typeof e.agent !== 'string') return { ok: false, reason: `${id}: agent invalido` };
  }
  return { ok: true };
}
export function readRegistry(p = ACTIVE_FILE) {
  let txt;
  try { txt = readFileSync(p, 'utf8'); } catch (e) {
    return e.code === 'ENOENT' ? { ok: true, active: {}, exists: false } : { ok: false, reason: `registro ilegible (${e.code || 'error'}): ${p}` };
  }
  let data;
  try { data = JSON.parse(txt); } catch { return { ok: false, reason: `registro corrupto (JSON invalido): ${p}` }; }
  const v = validateRegistry(data);
  return v.ok ? { ok: true, active: data, exists: true } : { ok: false, reason: `registro con esquema invalido: ${v.reason}` };
}
export function loadActive(p = ACTIVE_FILE) {
  const r = readRegistry(p);
  if (!r.ok) throw new Error(r.reason);
  return r.active;
}
// QA-02: ID activo duplicado => rechazo (nunca idempotente a ciegas); conflicto de archivos => rechazo.
export function checkLaunchOwnership(plan, reg = readRegistry()) {
  if (!reg || reg.ok !== true) return { ok: false, reason: reg?.reason || 'registro de propiedad no comprobable' };
  if (!validTaskId(plan.taskId)) return { ok: false, reason: 'taskId ausente, reservado o no valido' };
  if (Object.hasOwn(reg.active, plan.taskId)) {
    const e = reg.active[plan.taskId];
    return { ok: false, reason: `ID activo duplicado: ${plan.taskId} (estado ${e.state}${e.dispatch ? `, dispatch ${e.dispatch}` : ''}); conciliar y liberar antes de relanzar` };
  }
  if (!plan.ownerFiles || plan.ownerFiles.length === 0) return { ok: true };
  const others = Object.entries(reg.active).map(([id, v]) => ({ id, files: v.files }));
  return checkOwnershipConflicts([...others, { id: plan.taskId, files: plan.ownerFiles }]);
}
function withLock(p, fn) {
  mkdirSync(path.dirname(p), { recursive: true });
  const lock = `${p}.lock`;
  let fd;
  try { fd = openSync(lock, 'wx'); } catch { return { ok: false, reason: `registro de propiedad bloqueado (${lock}): otro lanzamiento en curso; no se reintenta a ciegas` }; }
  try { return fn(); } finally { closeSync(fd); try { unlinkSync(lock); } catch { /* ya borrado */ } }
}
function writeRegistry(p, active) {
  const tmp = `${p}.tmp`;
  writeFileSync(tmp, JSON.stringify(active, null, 2));
  renameSync(tmp, p); // escritura atomica: nunca queda un JSON a medias
}
export function claimOwnership(plan, p = ACTIVE_FILE, now = () => new Date().toISOString()) {
  return withLock(p, () => {
    const reg = readRegistry(p);
    const c = checkLaunchOwnership(plan, reg);
    if (!c.ok) return c;
    reg.active[plan.taskId] = { files: plan.ownerFiles || [], agent: plan.agent, claimedAt: now(), state: 'claimed' };
    writeRegistry(p, reg.active);
    return { ok: true, claimed: true };
  });
}
export function markClaim(taskId, patch, p = ACTIVE_FILE) {
  return withLock(p, () => {
    const reg = readRegistry(p);
    if (!reg.ok) return reg;
    if (!Object.hasOwn(reg.active, taskId)) return { ok: false, reason: `sin claim para ${taskId}` };
    const next = { ...reg.active[taskId], ...patch };
    const v = validateRegistry({ [taskId]: next });
    if (!v.ok) return { ok: false, reason: v.reason };
    reg.active[taskId] = next;
    writeRegistry(p, reg.active);
    return { ok: true };
  });
}
// Descarte interno: solo para un fallo de lanzamiento comprobadamente limpio (nada arranco).
export function dropClaim(taskId, p = ACTIVE_FILE) {
  return withLock(p, () => {
    const reg = readRegistry(p);
    if (!reg.ok) return reg;
    const had = Object.hasOwn(reg.active, taskId);
    delete reg.active[taskId];
    writeRegistry(p, reg.active);
    return { ok: true, released: had };
  });
}
// worker-show: el trabajo exacto vive en result.state/stage. Un terminal retained/live
// puede conservarse despues de worker_done; no representa trabajo aun activo.
const TERMINAL = /^(succeeded|completed|failed|stopped|abandoned|cancelled|canceled)$/;
export function isTerminalDispatch(record, expectedDispatch) {
  const dispatch = record?.result;
  return record?.ok === true && typeof dispatch?.dispatchId === 'string' && !!dispatch.dispatchId
    && (!expectedDispatch || dispatch.dispatchId === expectedDispatch)
    && dispatch.stage === 'settled' && TERMINAL.test(dispatch.state);
}
// Liberar: con dispatch conocido exige worker-show terminal; sin dispatch exige conciliacion explicita.
export function releaseOwnership(taskId, p = ACTIVE_FILE, { run = (c, a) => spawnSync(c, a, { encoding: 'utf8', timeout: 30000 }), reconciled = false } = {}) {
  const reg = readRegistry(p);
  if (!reg.ok) return reg;
  if (!validTaskId(taskId)) return { ok: false, reason: 'taskId reservado o no valido' };
  const e = Object.hasOwn(reg.active, taskId) ? reg.active[taskId] : undefined;
  if (!e) return { ok: true, released: false };
  if (e.dispatch) {
    const sh = run('orca', ['orchestration', 'worker-show', '--dispatch', e.dispatch, '--json']);
    const rec = safeJson(sh.stdout);
    if (sh.error || sh.status !== 0 || !isTerminalDispatch(rec, e.dispatch)) return { ok: false, reason: `dispatch ${e.dispatch} sin estado terminal comprobado: no se libera ${taskId}` };
  } else if (!reconciled) {
    return { ok: false, reason: `${taskId} sin dispatch conocido (estado ${e.state}): conciliar con 'orca orchestration worker-list' y repetir con --reconciled` };
  }
  return dropClaim(taskId, p);
}

// ---- modelo/esfuerzo (preferencia, no recibo) --------------------------------
export function loadCodexCatalog(p) {
  try { return JSON.parse(readFileSync(p, 'utf8')).models || []; } catch { return null; }
}
const EFFORT_ORDER = ['low', 'medium', 'high', 'xhigh'];

export function pickModel(agent, effort, cfg, opts = {}) {
  const a = cfg.agents[agent];
  if (!a) return { ok: false, reason: `${agent} sin modelo configurado/validado` };
  let eff = effort;
  if (!a.efforts.includes(eff)) eff = EFFORT_ORDER.filter((e) => a.efforts.includes(e)).pop();
  if (!eff) return { ok: false, reason: `${agent} sin esfuerzo soportado` };
  // Resolver el modelo DESPUES de normalizar esfuerzo (p.ej. xhigh -> high).
  const model = a.modelsByEffort?.[eff] || a.model;
  if (!model) return { ok: false, reason: `${agent} sin modelo configurado/validado` };
  if (agent === 'codex') {
    const cat = opts.codexCatalog !== undefined ? opts.codexCatalog : loadCodexCatalog(a.catalog);
    if (!cat) return { ok: false, reason: 'catalogo de Codex ilegible: no se valida el modelo' };
    const m = cat.find((x) => x.slug === model && x.visibility === 'list');
    if (!m) return { ok: false, reason: `modelo ${model} ausente o no listado en el catalogo de Codex` };
    const levels = (m.supported_reasoning_levels || []).map((l) => (typeof l === 'string' ? l : l.effort));
    if (!levels.includes(eff)) return { ok: false, reason: `esfuerzo ${eff} no soportado por ${model}` };
  }
  return { ok: true, model, effort: eff, status: 'preferencia; modelo efectivo NO confirmado hasta el recibo de lanzamiento' };
}

export function pickEffort(text, task, cfg) {
  if (task.risk === 'critical') return cfg.autoEffortCeiling; // xhigh solo con riesgo declarado
  if (task.effort && EFFORT_ORDER.includes(task.effort)) return task.effort;
  if (hits(text, cfg.criticalKeywords).length || hits(text, cfg.deepKeywords).length) return 'high';
  if (hits(text, cfg.mechanicalKeywords).length) return 'low';
  return 'medium';
}

// ---- disponibilidad y respaldo ----------------------------------------------
export function availabilityOf(agent, cfg, overrides = {}, transport = 'orca-worker') {
  const o = overrides[agent];
  if (o) return o.ok ? { ok: true } : { ok: false, reason: o.reason || 'fallo de proveedor' };
  // Una capacidad CLI o setup autenticado no prueba el transporte worker.
  const av = cfg.agents[agent]?.availability?.transports?.[transport];
  const s = av?.status;
  return s === 'verified' ? { ok: true } : { ok: false, reason: `${agent}/${transport}: ${s || 'unverified'} (${av?.evidence || 'sin prueba actual'})` };
}

function walkChain(chain, cfg, effort, opts, exclude = []) {
  const skipped = [];
  for (const agent of chain) {
    if (exclude.includes(agent)) continue;
    const av = availabilityOf(agent, cfg, opts.availability, opts.transport);
    if (!av.ok) { skipped.push(`${agent}: ${av.reason}`); continue; }
    const m = pickModel(agent, effort, cfg, opts);
    if (!m.ok) { skipped.push(`${agent}: ${m.reason}`); continue; }
    return { agent, ...m, skipped };
  }
  return { agent: null, skipped };
}

// ---- inferencia OmniRoute (via EXPLICITA, no agentica) ----------------------------
// task.transport='omniroute' + task.mode='inference'. Texto in -> texto out: sin herramientas, sin archivos,
// sin worker Orca, sin identidad de retorno (cliente sincrono). NO sustituye escritura ni revision de codigo.
export function planInference(task, cfg, opts = {}) {
  const o = cfg.omniroute;
  if (!o) return refuse('reject', 'omniroute no configurado en coordinator.json');
  if (task.transport !== 'omniroute') return refuse('reject', `transport desconocido: ${String(task.transport)}`);
  if (task.mode !== 'inference') return refuse('reject', `transport=omniroute exige mode=inference (recibido ${String(task.mode)}): una inferencia no ejecuta ni revisa codigo, no se acepta como escritura/revision`);
  if (Array.isArray(task.files) ? task.files.length > 0 : task.files !== undefined) return refuse('reject', 'inferencia sin archivos: no escribe ni revisa; use delegacion Orca');
  if (typeof task.text !== 'string' || !task.text.trim()) return refuse('reject', 'prompt vacio');
  if (task.text.length > o.maxPromptChars) return refuse('reject', `prompt excede ${o.maxPromptChars} caracteres`);
  if (!validTaskId(task.id)) return refuse('reject', 'id de tarea ausente, reservado o no valido');
  const model = task.model ?? o.defaultModel;
  if (typeof model !== 'string' || !o.allowedModels.includes(model)) return refuse('reject', `modelo fuera de la lista permitida: ${String(model)}`);
  const maxTokens = task.maxTokens ?? o.defaultMaxTokens;
  if (!Number.isInteger(maxTokens) || maxTokens < 1 || maxTokens > o.maxTokens) return refuse('reject', `maxTokens debe ser entero 1..${o.maxTokens}`);
  if (Array.isArray(opts.omnirouteCatalog) && !opts.omnirouteCatalog.includes(model)) return refuse('reject', `modelo ausente del catalogo OmniRoute autenticado: ${model}`);
  return {
    decision: 'inference', transport: 'omniroute', taskId: task.id, model, maxTokens, promptChars: task.text.length,
    agentic: false, tools: false, executed: false,
    acceptsAs: 'texto generado; NO ejecuta ni revisa codigo ni escribe archivos',
    returnChannel: 'sincrono (sin identidad Orca)',
  };
}
const defaultPy = (c, a, input, timeoutSec) => spawnSync(c, a, { input, encoding: 'utf8', timeout: (timeoutSec + 15) * 1000, env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
export function inferenceArgs(plan, cfg) {
  const o = cfg.omniroute;
  return [path.join(ROOT, o.client), '--config', path.join(ROOT, o.configFile), '--model', plan.model, '--max-tokens', String(plan.maxTokens), '--timeout', String(o.timeoutSec)];
}
// Ejecuta UNA inferencia; el prompt va por stdin; nunca se reintenta; no se imprime ninguna credencial.
export function runInference(plan, prompt, cfg = loadConfig(), run = defaultPy) {
  if (plan?.decision !== 'inference' || plan.agentic !== false || plan.tools !== false)
    return { ok: false, stage: 'validation', error: 'se requiere un plan explicito de inferencia sin herramientas' };
  const checked = planInference({ id: plan.taskId, text: prompt, transport: plan.transport, mode: 'inference', model: plan.model, maxTokens: plan.maxTokens }, cfg);
  if (checked.decision !== 'inference') return { ok: false, stage: 'validation', error: checked.reason };
  const o = cfg.omniroute;
  const r = run(o.python, inferenceArgs(plan, cfg), prompt, o.timeoutSec);
  if (r.error || r.status !== 0) {
    const e = safeJson(r.stderr);
    return { ok: false, stage: 'omniroute', exit: r.status ?? null, http: e.http ?? null, errorType: e.error_type ?? null, error: String(e.error || (r.error ? 'no se pudo ejecutar el cliente' : 'fallo del cliente')).slice(0, 200) };
  }
  const out = safeJson(r.stdout);
  if (out.status !== 'PASS' || typeof out.response !== 'string' || !out.response.trim()) return { ok: false, stage: 'omniroute', error: 'respuesta del cliente invalida o sin PASS' };
  return { ok: true, transport: 'omniroute', taskId: plan.taskId, requestedModel: out.requested_model ?? plan.model, reportedModel: out.reported_model ?? null, http: out.http ?? null, response: out.response, note: plan.acceptsAs };
}

// ---- router ----------------------------------------------------------------
// task:{ id, text, size:'small'|'substantial', mode?:'write'|'review'|'research', files?, domain?, risk?, effort?, implementer? }
export function route(task, cfg = loadConfig(), opts = {}) {
  const text = norm(task.text);
  if (!text.trim()) return refuse('abstain', 'encargo vacio');
  if (task.transport !== undefined) return planInference(task, cfg, opts); // via explicita aparte de la delegacion Orca
  if (task.mode === 'inference') return refuse('reject', 'mode=inference requiere transport=omniroute explicito');
  if (!['small', 'substantial'].includes(task.size)) return refuse('abstain', 'falta size (small|substantial): no se adivina el tamano');
  const mode = task.mode || 'write';
  if (!['write', 'review', 'research'].includes(mode)) return refuse('abstain', `mode invalido: ${mode}`);

  const human = hits(text, cfg.humanDecisionKeywords);
  if (human.length) return refuse('human-decision', `decision comercial/legal (${human.join(', ')}): una sola responsabilidad humana, sin equipo`, { owner: 'usuario' });

  const needsApproval = hits(text, cfg.externalActionKeywords);
  const base = { needsUserApproval: needsApproval.length > 0, approvalTriggers: needsApproval };

  // dominio
  let domain = task.domain;
  let scores = {};
  // Correspondencias con los nombres de dominio de team/ROUTING.md (solo equivalentes con la misma cadena de IAs)
  const requestedDomain = domain;
  if (domain && !cfg.domains[domain] && Object.hasOwn(cfg.domainAliases || {}, domain)) domain = cfg.domainAliases[domain];
  if (domain) {
    if (!cfg.domains[domain]) return refuse('abstain', `dominio desconocido: ${requestedDomain}`);
  } else {
    for (const [d, def] of Object.entries(cfg.domains)) scores[d] = hits(text, def.keywords).length;
    const ranked = Object.entries(scores).sort((x, y) => y[1] - x[1]);
    const [top, second] = [ranked[0], ranked[1]];
    if (top[1] < 2) return refuse('abstain', 'dominio no determinable (menos de 2 senales): aclarar o pasar domain', { scores });
    if (second[1] > 0 && top[1] - second[1] < 2) return refuse('abstain', `ambiguedad entre ${top[0]} y ${second[0]}: dividir por pasos, un rol a la vez`, { scores });
    domain = top[0];
  }

  const def = cfg.domains[domain];
  const effort = pickEffort(text, task, cfg);

  // tarea chica: directo, sin delegar
  if (task.size === 'small' && mode !== 'review') return { decision: 'direct', reason: 'tarea chica: la IA que la recibe la hace', domain, effort, ...base };

  if (mode === 'write') {
    const own = validateOwnership(task.files, cfg);
    if (!own.ok) return refuse('reject', own.reason, { domain });
    task = { ...task, files: own.files };
  }

  let exclude = [];
  if (mode === 'review') {
    if (!task.implementer) return refuse('abstain', 'revision sin implementador declarado: no se puede garantizar independencia', { domain });
    exclude = [task.implementer]; // sin autoaprobacion
  }

  const pick = walkChain(def.chain, cfg, effort, { ...opts, transport: 'orca-worker' }, exclude);
  if (!pick.agent) return refuse('reject', `ningun proveedor disponible${mode === 'review' ? ' e independiente' : ''}: ${pick.skipped.join(' | ')}`, { domain });

  const fallback = pick.agent !== def.chain.find((a) => !exclude.includes(a));
  return ok({
    ...base, taskId: task.id, domain, ...(requestedDomain && requestedDomain !== domain ? { requestedDomain } : {}), mode, agent: pick.agent, model: pick.model, effort: pick.effort,
    modelStatus: pick.status, effectiveModel: null, roles: def.roles, ownerFiles: mode === 'write' ? task.files : [],
    fallbackUsed: fallback, skipped: pick.skipped,
    reviewRequired: mode === 'write', // un implementador nunca se autoaprueba
    evidenceRequired: ['archivos modificados', 'comandos y resultado real', 'limites'],
    returnTo: 'coordinador (worker_done: implementado-pendiente-QA)',
  });
}

// ---- revision independiente ---------------------------------------------------
export function pickReviewer(implementer, domain, cfg = loadConfig(), opts = {}) {
  const d = cfg.domains[domain];
  if (!d) return refuse('abstain', `dominio desconocido: ${domain}`);
  // Recomendacion de revision externa, no un lanzamiento ni un veredicto.
  // Codex revisa primero (rol del encargo); siempre distinto del implementador.
  const order = ['codex', 'claude', 'antigravity'];
  const transport = opts.transport || 'external-review';
  const pick = walkChain(order, cfg, 'high', { ...opts, transport }, [implementer]);
  return pick.agent ? { ok: true, ...pick, transport, launchable: transport === 'orca-worker' } : { ok: false, reason: `sin revisor independiente disponible: ${pick.skipped.join(' | ')}` };
}

// Una entrega solo se acepta con revision de otro agente, veredicto PASS y evidencia.
export function canAccept(delivery) {
  const r = delivery?.review;
  if (!r) return { accepted: false, reason: 'sin revision' };
  if (!r.reviewer || r.reviewer === delivery.implementer) return { accepted: false, reason: 'autoaprobacion o revisor ausente' };
  if (r.verdict !== 'PASS') return { accepted: false, reason: `veredicto ${r.verdict}` };
  if (!r.evidence || !String(r.evidence).trim()) return { accepted: false, reason: 'revision sin evidencia' };
  return { accepted: true };
}

// ---- lanzamiento Orca ---------------------------------------------------------
// Respeta la skill orchestration: --model/--effort SOLO si el usuario nombro modelo (userNamedModel).
export function buildWorkerStartArgs(plan, { userNamedModel = false, worktree = 'current' } = {}) {
  const args = ['orchestration', 'worker-start', '--spec-file', '-', '--worktree', worktree, '--agent', plan.agent, '--task-title', `${plan.domain}: ${plan.taskId}`, '--json'];
  if (userNamedModel && plan.model) args.push('--model', plan.model, '--effort', plan.effort);
  return args;
}

export function buildSpec(plan, task) {
  return [
    `# ${plan.taskId} (${plan.domain})`, '', `Encargo: ${task.text}`, '',
    'Contexto comun: comprobar raiz Git del encargo; leer AGENTS.md y docs/operations/AI-REPORT-CONTRACT.md locales vigentes. Informar workspace/repositorio saneado cuando corresponda; modelo planeado separado de efectivo null/no_observado sin recibo exacto, con procedencia al observarlo. JSON solo si el handoff lo necesita.',
    ...(plan.agent === 'antigravity' ? [
      `Contexto Altiora vigente: comprobar git rev-parse --show-toplevel; raiz de este encargo ${ROOT.replace(/\\/g, '/')}.`,
      'Antes de actuar leer GEMINI.md y AGENTS.md locales; consultar docs/operations/ESTADO-ACTUAL.md y .altiora/coordinator.json solo si existen y pertenecen al encargo; referencias vivas, no snapshots ni exploracion masiva.',
      'La existencia de archivos/catalogos no acredita conexiones; respetar evidencia por transporte, permisos, ownership y QA independiente.',
    ] : []),
    `Puede editar SOLO: ${plan.ownerFiles.join(', ') || '(solo lectura)'}`,
    `Roles: ${plan.roles.join(', ')}. Esfuerzo sugerido: ${plan.effort}.`,
    'No: commit, push, publicar, gastar, instalar, tocar secretos/permisos/app/clientes.',
    `Evidencia: ${plan.evidenceRequired.join('; ')}.`,
    'Devolver: orca orchestration send --type worker_done (3 frases: hecho / hallado / pendiente). Estado: implementado-pendiente-QA; no declarar PASS propio.',
  ].join('\n');
}

// Modelo/esfuerzo EFECTIVOS: solo cuentan si Orca los devuelve (worker-start / worker-show --json).
// Solo el path efectivo verificado de Orca acredita modelo/esfuerzo; nunca requested/plan/metadata.
function findDeep(o, re, depth = 0) {
  if (!o || typeof o !== 'object' || depth > 6) return undefined;
  for (const [k, v] of Object.entries(o)) {
    if (re.test(k) && (typeof v === 'string' || typeof v === 'number') && String(v).trim()) return String(v);
    const d = findDeep(v, re, depth + 1);
    if (d !== undefined) return d;
  }
  return undefined;
}
export function observeEffective(record, plan = {}) {
  const effective = record?.ok !== false ? record?.result?.worker?.startOptions?.launch?.effective : null;
  const model = typeof effective?.model === 'string' && effective.model.trim() ? effective.model : null;
  if (!model) return { observed: false, status: 'no_observado', model: null, effort: null, source: null, effortSource: null, note: 'modelo efectivo NO observado en el recibo; se mantiene como preferencia' };
  const effort = typeof effective.effort === 'string' && effective.effort.trim() ? effective.effort : null;
  const same = !plan.model || model === plan.model;
  return { observed: true, status: 'observado', model, effort,
    source: 'result.worker.startOptions.launch.effective.model',
    effortSource: effort ? 'result.worker.startOptions.launch.effective.effort' : null,
    matchesPreference: same, note: same ? 'modelo efectivo observado, coincide con la preferencia' : `modelo efectivo ${model} difiere de la preferencia ${plan.model}: se informa, no se corrige` };
}
export function findDispatchId(receipt) { return findDeep(receipt, /^dispatch_?id$/i); }

export function checkFlagsAgainstHelp(args, helpText) {
  const used = args.filter((a) => a.startsWith('--'));
  const missing = used.filter((f) => !helpText.includes(f));
  return { ok: missing.length === 0, missing };
}

const findRaw = (o, re, depth = 0) => {
  if (!o || typeof o !== 'object' || depth > 6) return undefined;
  for (const [k, v] of Object.entries(o)) { if (re.test(k)) return v; const d = findRaw(v, re, depth + 1); if (d !== undefined) return d; }
  return undefined;
};
// Clasifica el resultado de worker-start. Solo 'failed-clean' permite descartar el claim; todo lo demas
// (outcome_unknown, JSON ilegible, error de spawn, recursos residuales) es 'uncertain': claim conservado.
export function classifyLaunch(r) {
  if (!r || r.error || r.status === null || r.status === undefined) return { kind: 'uncertain', why: 'el proceso no termino de forma comprobable' };
  if (r.status === 0) return { kind: 'launched' };
  const rec = safeJson(r.stdout);
  if (!rec || typeof rec !== 'object' || Object.keys(rec).length === 0) return { kind: 'uncertain', why: 'salida ilegible tras fallo' };
  const raw = JSON.stringify(rec).toLowerCase();
  const st = String(findDeep(rec, /^status$/i) || '').toLowerCase();
  const stage = findDeep(rec, /^failed_?stage$/i);
  const residual = findRaw(rec, /^residual_?resources$/i);
  const clean = st === 'failed' && !!stage && !raw.includes('outcome_unknown') && Array.isArray(residual) && residual.length === 0;
  return clean ? { kind: 'failed-clean', stage } : { kind: 'uncertain', why: `estado ${st || 'desconocido'}${stage ? `, etapa ${stage}` : ''}: puede haber arrancado` };
}

// Fallo de lanzamiento: nunca reintentar worker-start a ciegas (skill orchestration).
export function handleLaunchFailure(result) {
  const stage = result?.failedStage || result?.stage || 'desconocido';
  return { retry: false, action: `leer failedStage=${stage} y cargar references/recovery-and-cleanup.md; no relanzar worker-start`, escalate: true };
}

// Hallazgo QA 1: poder LANZAR no es poder SUPERVISAR/recibir retorno. Se separan:
//   launchReady  = herramientas + runtime + IA seleccionable (capacidad de lanzar)
//   returnReady  = identidad propia de Orca comprobada (ORCA_TERMINAL_HANDLE de un terminal vivo)
//   executeReady = ambas; `launch --execute` exige executeReady. Nunca se usa un handle ajeno ni se inventa uno.
export function preflight({ cfg = loadConfig(), env = process.env, opts = {}, run = (c, a) => spawnSync(c, a, { encoding: 'utf8', timeout: 30000 }) } = {}) {
  const checks = [];
  const add = (name, pass, detail, optional = false) => checks.push({ name, pass, detail, optional });
  const top = run('git', ['rev-parse', '--show-toplevel']);
  add('raiz git = raiz confirmada', norm(top.stdout.trim()) === norm(cfg.root), top.stdout.trim());
  add('ALTIORA_DISPATCH_EXECUTE inactivo', !env.ALTIORA_DISPATCH_EXECUTE, env.ALTIORA_DISPATCH_EXECUTE ? 'ACTIVO' : 'no definido');
  const help = run('orca', ['orchestration', 'worker-start', '--help']);
  const helpText = `${help.stdout || ''}`;
  const flags = checkFlagsAgainstHelp(buildWorkerStartArgs({ agent: 'codex', domain: 'd', taskId: 't', model: 'm', effort: 'e' }, { userNamedModel: true }), helpText);
  add('flags de worker-start existen en el CLI', help.status === 0 && flags.ok, flags.missing.join(',') || 'ok');
  const st = run('orca', ['status', '--json']);
  let running = false; try { running = JSON.parse(st.stdout).result.runtime.reachable === true; } catch { /* ilegible */ }
  add('runtime Orca alcanzable (necesario para lanzar)', running, running ? 'reachable' : 'NO alcanzable desde este shell');
  let eligibleWorkers = 0;
  for (const ag of Object.keys(cfg.agents)) {
    const av = availabilityOf(ag, cfg, opts.availability);
    const m = av.ok ? pickModel(ag, 'medium', cfg, opts) : { ok: false, reason: av.reason };
    if (m.ok) eligibleWorkers++;
    add(`${ag}: worker seleccionable`, m.ok, m.ok ? `${m.model} (${m.status})` : m.reason, true);
  }
  add('al menos un worker elegible', eligibleWorkers > 0, `${eligibleWorkers} worker(s) con transporte y modelo comprobados`);
  const launchReady = checks.every((c) => c.pass || c.optional);
  const handle = String(env.ORCA_TERMINAL_HANDLE || '').trim();
  const rc = [];
  const radd = (name, pass, detail) => rc.push({ name, pass, detail });
  radd('ORCA_TERMINAL_HANDLE propio presente', /^term_[0-9a-f-]{8,}$/i.test(handle), handle ? 'presente (valor no registrado en salida)' : 'AUSENTE: sesion sin identidad Orca; no puede recibir worker_done');
  if (handle) {
    const sh = run('orca', ['terminal', 'show', '--terminal', handle, '--json']);
    let live = false;
    try {
      const receipt = JSON.parse(sh.stdout);
      const terminal = receipt?.result?.terminal;
      // ok:true tambien puede describir un terminal cerrado: comprobar metadata exacta.
      live = !sh.error && sh.status === 0 && receipt.ok === true && terminal?.handle === handle
        && terminal.connected === true && terminal.writable === true && terminal.orphaned === false;
    } catch { /* ilegible: retorno no acreditado */ }
    radd('el handle propio corresponde a un terminal conectado y escribible de Orca', live, live ? 'terminal propio conectado, escribible y no huerfano' : 'orca terminal show no confirma handle exacto, connected=true, writable=true y orphaned=false');
  }
  const returnReady = rc.every((c) => c.pass);
  return { checks, returnChecks: rc, launchReady, returnReady, executeReady: launchReady && returnReady };
}

// ---- CLI -----------------------------------------------------------------------
async function main() {
  const [cmd, file, ...flags] = process.argv.slice(2);
  const cfg = loadConfig();
  if (cmd === 'preflight') {
    const r = preflight({ cfg }); console.log(JSON.stringify(r, null, 2)); process.exit(r.executeReady ? 0 : 1);
  }
  if (cmd === 'release') {
    if (!file) { console.error('uso: node scripts/orca-coordinator.mjs release <taskId> [--reconciled]'); process.exit(2); }
    const r = releaseOwnership(file, undefined, { reconciled: flags.includes('--reconciled') }); console.log(JSON.stringify(r)); process.exit(r.ok ? 0 : 1);
  }
  if (cmd === 'claims') { const r = readRegistry(); console.log(JSON.stringify(r.ok ? r.active : r, null, 2)); process.exit(r.ok ? 0 : 1); }
  if (cmd === 'infer') {
    if (!file || !existsSync(file)) { console.error('uso: node scripts/orca-coordinator.mjs infer task.json [--execute]  (task: transport=omniroute, mode=inference)'); process.exit(2); }
    const task = safeJson(readFileSync(file, 'utf8'));
    const plan = route(task, cfg);
    if (plan.decision !== 'inference') { console.log(JSON.stringify(plan, null, 2)); process.exit(1); }
    if (!flags.includes('--execute')) { console.log(JSON.stringify({ dryRun: true, command: [cfg.omniroute.python, ...inferenceArgs(plan, cfg)], plan }, null, 2)); process.exit(0); }
    const res = runInference(plan, task.text, cfg);
    console.log(JSON.stringify(res, null, 2)); process.exit(res.ok ? 0 : 1);
  }
  if (cmd === 'route' || cmd === 'launch') {
    if (!file || !existsSync(file)) { console.error('uso: node scripts/orca-coordinator.mjs <route|launch|preflight> task.json [--execute --approved --user-named-model]'); process.exit(2); }
    const task = JSON.parse(readFileSync(file, 'utf8'));
    const plan = route(task, cfg);
    if (cmd === 'route' || plan.decision !== 'delegate') { console.log(JSON.stringify(plan, null, 2)); process.exit(plan.decision === 'delegate' || plan.decision === 'direct' ? 0 : 1); }
    const args = buildWorkerStartArgs(plan, { userNamedModel: flags.includes('--user-named-model') });
    const spec = buildSpec(plan, task);
    if (plan.needsUserApproval && !flags.includes('--approved')) { console.log(JSON.stringify({ ...plan, blocked: 'requiere aprobacion del usuario (accion externa)' }, null, 2)); process.exit(1); }
    const own = checkLaunchOwnership(plan);
    if (!(flags.includes('--execute') && flags.includes('--approved'))) { console.log(JSON.stringify({ dryRun: true, ownership: own, command: ['orca', ...args], spec, plan }, null, 2)); process.exit(own.ok ? 0 : 1); }
    const pf = preflight({ cfg }); if (!pf.executeReady) { console.error(JSON.stringify(pf, null, 2)); process.exit(1); }
    const claim = claimOwnership(plan); if (!claim.ok) { console.error(JSON.stringify({ blocked: 'propiedad en conflicto, ID duplicado, registro invalido o bloqueado', ...claim })); process.exit(1); }
    const r = spawnSync('orca', args, { input: spec, encoding: 'utf8' });
    console.log(r.stdout);
    const receipt = safeJson(r.stdout);
    const did = findDispatchId(receipt);
    const cl = classifyLaunch(r);
    if (cl.kind === 'failed-clean') { dropClaim(plan.taskId); console.error(JSON.stringify({ ...handleLaunchFailure(receipt), claim: 'liberado (fallo limpio comprobado)' })); process.exit(1); }
    if (cl.kind === 'uncertain') { markClaim(plan.taskId, { state: 'unknown-launch', ...(did ? { dispatch: did } : {}) }); console.error(JSON.stringify({ ...handleLaunchFailure(receipt), claim: `CONSERVADO (estado incierto: ${cl.why}); conciliar con worker-list/worker-show y liberar con release --reconciled` })); process.exit(1); }
    markClaim(plan.taskId, { state: 'launched', ...(did ? { dispatch: did } : {}) });
    // Modelo efectivo: solo del recibo de Orca (worker-start, y si falta, worker-show).
    let eff = observeEffective(receipt, plan);
    if (!eff.observed && did) { const sh = spawnSync('orca', ['orchestration', 'worker-show', '--dispatch', did, '--json', '--full'], { encoding: 'utf8', timeout: 30000 }); eff = observeEffective(safeJson(sh.stdout), plan); }
    console.log(JSON.stringify({ launched: true, ids: { run: findDeep(receipt, /^run_?id$/i) ?? null, task: findDeep(receipt, /^task_?id$/i) ?? null, dispatch: did ?? null }, effective: eff, release: `node scripts/orca-coordinator.mjs release ${plan.taskId}` }, null, 2));
    return;
  }
  console.error('comandos: route | launch | preflight'); process.exit(2);
}
const safeJson = (s) => { try { const value = JSON.parse(s); return value && typeof value === 'object' && !Array.isArray(value) ? value : {}; } catch { return {}; } };
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
