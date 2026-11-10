import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { runChecks, checkHttp, checkWorkers, ROOT, ENDPOINTS } from './altiora-ready.mjs';

// Sin red real: fetch inyectado; registro y configuracion por fixture.
const mk = () => mkdtempSync(path.join(tmpdir(), 'ready-'));
const okFetch = async () => ({ status: 200 });
const goodReg = (d) => {
  const p = path.join(d, 'reg.json');
  writeFileSync(p, JSON.stringify({ t1: { files: ['a.md'], state: 'launched', claimedAt: '2026-11-10T00:00:00Z' } }));
  return p;
};
const cfg = (claude, codex) => ({ agents: {
  claude: { availability: { transports: { 'orca-worker': { status: claude } } } },
  codex: { availability: { transports: { 'orca-worker': { status: codex, evidence: 'hooks' } } } },
} });

test('ruta sana: claims activos no son fallo, Codex bloqueado es limite, Claude elegible', async () => {
  const d = mk();
  try {
    const rep = await runChecks({ root: ROOT, registryPath: goodReg(d), fetchFn: okFetch, loader: () => cfg('verified', 'blocked') });
    assert.equal(rep.ready, true);
    assert.equal(rep.exitCode, 0);
    assert.equal(rep.claimsActive, 1);
    assert.deepEqual(rep.eligibleWorkers, ['claude']);
    assert.ok(rep.limits.some((l) => /codex orca-worker no elegible/.test(l)));
  } finally { rmSync(d, { recursive: true, force: true }); }
});
test('servicio caido: exit 1 y JSON serializable', async () => {
  const d = mk();
  try {
    const down = async () => { throw Object.assign(new Error('x'), { cause: { code: 'ECONNREFUSED' } }); };
    const rep = await runChecks({ root: ROOT, registryPath: goodReg(d), fetchFn: down, loader: () => cfg('verified', 'blocked') });
    assert.equal(rep.exitCode, 1);
    assert.equal(rep.checks.filter((c) => !c.pass).length, 2);
    assert.match(rep.checks.at(-1).detail, /ECONNREFUSED/);
    JSON.parse(JSON.stringify(rep));
  } finally { rmSync(d, { recursive: true, force: true }); }
});
test('registro corrupto: falla con motivo', async () => {
  const d = mk();
  try {
    const p = path.join(d, 'reg.json');
    writeFileSync(p, '{no json');
    const rep = await runChecks({ root: ROOT, registryPath: p, fetchFn: okFetch, loader: () => cfg('verified', 'blocked') });
    const r = rep.checks.find((c) => c.id === 'registro');
    assert.equal(r.pass, false);
    assert.match(r.detail, /corrupto/);
    assert.equal(rep.exitCode, 1);
  } finally { rmSync(d, { recursive: true, force: true }); }
});
test('sin worker elegible: falla', async () => {
  const r = checkWorkers(cfg('blocked', 'blocked'));
  assert.equal(r.check.pass, false);
  assert.equal(r.eligible.length, 0);
  assert.equal(r.limits.length, 2);
  const d = mk();
  try {
    const rep = await runChecks({ root: ROOT, registryPath: goodReg(d), fetchFn: okFetch, loader: () => cfg('blocked', 'blocked') });
    assert.equal(rep.exitCode, 1);
  } finally { rmSync(d, { recursive: true, force: true }); }
});
test('HTTP: redirect manual, timeout acotado, status != 200 falla, solo loopback', async () => {
  let seen;
  const r = await checkHttp(ENDPOINTS[0], async (u, o) => { seen = o; return { status: 302 }; });
  assert.equal(r.pass, false);
  assert.equal(seen.redirect, 'manual');
  assert.ok(seen.signal);
  let called = false;
  const bad = await checkHttp({ name: 'x', url: 'http://example.com/health' }, async () => { called = true; return { status: 200 }; });
  assert.equal(bad.pass, false);
  assert.equal(called, false);
});
