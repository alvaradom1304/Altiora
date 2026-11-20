#!/usr/bin/env node
// Diagnostico de solo lectura para usar Altiora. Sin dependencias nuevas.
// No inicia servicios, no instala, no lee .env/claves, no envia solicitudes autenticadas, no modifica config.
// Solo loopback (127.0.0.1), timeout 5 s por solicitud, sin seguir redirects.
// Uso: node scripts/altiora-ready.mjs [--json]   (exit 0 = operativo, 1 = faltan comprobaciones)
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadConfig, readRegistry, availabilityOf } from './orca-coordinator.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(HERE, '..');
export const TIMEOUT_MS = 5000;
export const ENDPOINTS = [
  { name: 'omniroute-health', url: 'http://127.0.0.1:20128/api/health' },
  { name: 'omniroute-ready', url: 'http://127.0.0.1:20129/readyz' },
];
const norm = (p) => path.resolve(String(p)).replace(/\\/g, '/').toLowerCase();
const chk = (id, label, pass, detail) => ({ id, label, pass: !!pass, detail });

export function checkRootConfig(root = ROOT, loader = loadConfig) {
  const cfgPath = path.join(root, '.altiora', 'coordinator.json');
  const label = 'raiz y configuracion';
  if (!existsSync(cfgPath)) return { check: chk('config', label, false, `falta ${cfgPath}`), cfg: null };
  let cfg;
  try { cfg = loader(cfgPath); } catch (e) { return { check: chk('config', label, false, `coordinator.json ilegible: ${e.message}`), cfg: null }; }
  if (!cfg || typeof cfg !== 'object' || !cfg.agents || typeof cfg.agents !== 'object') return { check: chk('config', label, false, 'coordinator.json sin "agents"'), cfg: null };
  if (cfg.root && norm(cfg.root) !== norm(root)) return { check: chk('config', label, false, `root de config (${cfg.root}) distinto de la raiz activa (${root})`), cfg };
  return { check: chk('config', label, true, `raiz ${root}`), cfg };
}

export function checkRegistry(registryPath, reader = readRegistry) {
  const label = 'esquema del registro de claims';
  const r = registryPath ? reader(registryPath) : reader();
  if (!r.ok) return { check: chk('registro', label, false, r.reason), claims: null };
  const n = Object.keys(r.active).length;
  return { check: chk('registro', label, true, `${n} claim(s) activo(s); informativo, no es fallo`), claims: n };
}

export function checkWorkers(cfg) {
  const label = 'transporte orca-worker elegible';
  if (!cfg) return { check: chk('worker', label, false, 'sin configuracion'), eligible: [], limits: [] };
  const eligible = [], limits = [];
  for (const agent of Object.keys(cfg.agents)) {
    const av = availabilityOf(agent, cfg, {}, 'orca-worker');
    if (av.ok) eligible.push(agent); else limits.push(`${agent} orca-worker no elegible: ${av.reason}`);
  }
  const detail = eligible.length ? `elegible(s): ${eligible.join(', ')}` : 'ningun agente con orca-worker verificado';
  return { check: chk('worker', label, eligible.length > 0, detail), eligible, limits };
}

export async function checkHttp(ep, fetchFn = globalThis.fetch) {
  const id = ep.name, label = `HTTP 200 ${ep.url}`;
  let u;
  try { u = new URL(ep.url); } catch { return chk(id, label, false, 'URL invalida'); }
  if (u.protocol !== 'http:' || u.hostname !== '127.0.0.1') return chk(id, label, false, 'rechazado: solo loopback 127.0.0.1');
  try {
    const res = await fetchFn(ep.url, { method: 'GET', redirect: 'manual', signal: AbortSignal.timeout(TIMEOUT_MS) });
    return chk(id, label, res.status === 200, `status ${res.status}`);
  } catch (e) {
    return chk(id, label, false, `sin respuesta (${e?.name === 'TimeoutError' ? 'timeout 5s' : e?.cause?.code || e?.message || 'error'})`);
  }
}

export async function runChecks({ root = ROOT, registryPath, fetchFn, endpoints = ENDPOINTS, loader } = {}) {
  const cfgR = checkRootConfig(root, loader);
  const reg = checkRegistry(registryPath);
  const wk = checkWorkers(cfgR.cfg);
  const http = await Promise.all(endpoints.map((e) => checkHttp(e, fetchFn)));
  const checks = [cfgR.check, reg.check, wk.check, ...http];
  const ready = checks.every((c) => c.pass);
  const limits = [
    ...wk.limits,
    'Revision QA independiente por otro agente sigue siendo requerida; este diagnostico no la sustituye.',
    'Solo prueba disponibilidad local; no acredita cuota, inferencia ni autenticacion.',
  ];
  return { ready, exitCode: ready ? 0 : 1, claimsActive: reg.claims, eligibleWorkers: wk.eligible, checks, limits };
}

export function formatText(rep) {
  const L = rep.checks.map((c) => `${c.pass ? 'OK   ' : 'FALLA'} ${c.label}: ${c.detail}`);
  L.push('', ...rep.limits.map((l) => `LIMITE: ${l}`), '', rep.ready ? 'LISTO' : 'NO LISTO');
  return L.join('\n');
}

async function main() {
  const json = process.argv.includes('--json');
  let rep;
  try { rep = await runChecks(); } catch (e) { rep = { ready: false, exitCode: 1, checks: [chk('interno', 'diagnostico', false, e.message)], limits: [] }; }
  console.log(json ? JSON.stringify(rep, null, 2) : formatText(rep));
  process.exit(rep.exitCode);
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
