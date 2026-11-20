#!/usr/bin/env node
// Local integration checks only. Does not install ECC, read credentials, or execute manifest commands.
import { readFileSync, existsSync, realpathSync, lstatSync } from 'node:fs';
import { resolve, relative, isAbsolute, sep } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

function git(root, args, optional = false) {
  try { return execFileSync('git', args, { cwd: root, encoding: 'utf8', windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, GIT_OPTIONAL_LOCKS: '0' } }).trim(); }
  catch (error) { if (optional && error.status === 1) return null; throw new Error('Git metadata operation failed; inspect configuration before retrying.'); }
}
const EXPECTED_HOOK = '#!/bin/sh\n# Altiora: bloquea commits con posibles credenciales (scripts/secret-guard.mjs).\nexec node scripts/secret-guard.mjs\n';
// En Windows, realpathSync (JS) conserva los nombres cortos 8.3 (p. ej. C:\Users\RUNNER~1\...) y Git devuelve la ruta
// larga; realpathSync.native expande ambos a la misma forma. En POSIX el comportamiento no cambia.
function canonical(p) {
  const abs = resolve(p);
  if (process.platform !== 'win32') return abs;
  try { return realpathSync.native(abs).toLowerCase(); } catch { return abs.toLowerCase(); }
}
function same(a, b) {
  return canonical(a) === canonical(b);
}
function localPath(root, name) {
  if (typeof name !== 'string' || !name || isAbsolute(name) || name.includes('\\') || name.split('/').some(p => p === '..' || p === '.git' || p.startsWith('.env'))) throw new Error('Unsafe adoption path');
  const path = resolve(root, name);
  if (relative(root, path).startsWith('..' + sep)) throw new Error('Adoption path escapes root');
  if (existsSync(path)) {
    const actual = realpathSync(path);
    const rel = relative(root, actual);
    if (isAbsolute(rel) || rel === '..' || rel.startsWith('..' + sep) || lstatSync(path).isSymbolicLink()) throw new Error('Adoption path is redirected');
  }
  return path;
}
function requireRoot(input) {
  const root = realpathSync(input);
  if (!same(git(root, ['rev-parse', '--show-toplevel']), root)) throw new Error('Run from the exact Git root');
  return root;
}
export function inspectIntegration(input) {
  const root = requireRoot(input);
  const manifestPath = resolve(root, 'references/ecc-adoption.json');
  let manifest = null;
  if (existsSync(manifestPath)) {
    localPath(root, 'references/ecc-adoption.json');
    manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
    if (manifest.repository !== 'https://github.com/affaan-m/ECC' || !/^[0-9a-f]{40}$/.test(manifest.reviewedCommit || '')) throw new Error('Invalid ECC source commit or repository');
    if (!Array.isArray(manifest.capabilities) || !manifest.capabilities.length) throw new Error('Missing capability inventory');
  }
  const adaptations = (manifest?.capabilities || []).map(c => {
    if (typeof c.id !== 'string' || !Array.isArray(c.paths) || !c.paths.length) throw new Error('Invalid capability paths');
    const missing = c.paths.filter(p => !existsSync(localPath(root, p)));
    return { id: c.id, status: missing.length ? 'missing' : 'present', missing };
  });
  const provenance = ['third_party/ecc/SOURCE.md', 'third_party/ecc/LICENSE.txt'].every(p => existsSync(localPath(root, p)));
  const hookFile = localPath(root, '.githooks/pre-commit');
  const guardFile = localPath(root, 'scripts/secret-guard.mjs');
  const hookConfiguredPath = git(root, ['rev-parse', '--path-format=absolute', '--git-path', 'hooks/pre-commit']);
  let hookStatus = 'not_configured';
  if (!existsSync(hookFile) || !existsSync(guardFile)) hookStatus = 'missing';
  else if (!lstatSync(hookFile).isFile() || !lstatSync(guardFile).isFile()) hookStatus = 'invalid_file';
  else if (readFileSync(hookFile, 'utf8').replace(/\r\n/g, '\n') !== EXPECTED_HOOK) hookStatus = 'custom_not_verified';
  else if (process.platform !== 'win32' && !(lstatSync(hookFile).mode & 0o111)) hookStatus = 'not_executable';
  else if (same(hookConfiguredPath, hookFile)) hookStatus = 'configured';
  else if (existsSync(hookConfiguredPath)) hookStatus = 'custom_not_verified';
  const adaptationsPresent = Boolean(manifest && provenance && adaptations.every(c => c.status === 'present'));
  return {
    schema_version: 1, workspace: root, reviewedCommit: manifest?.reviewedCommit || null,
    adaptationsPresent, adaptations, nativePlugin: 'not_assessed',
    hook: { status: hookStatus, functionalCheck: 'not_run' },
    integrated: adaptationsPresent && hookStatus === 'configured',
    limitation: 'Presence and configuration checks only; functional and security evidence are separate. No model, usage or savings inferred.',
  };
}
export function installHooks(input) {
  const root = requireRoot(input);
  const status = inspectIntegration(root);
  if (!status.adaptationsPresent || ['missing', 'invalid_file'].includes(status.hook.status)) throw new Error('Required reviewed integration files or hook are missing/invalid');
  if (status.hook.status === 'not_executable') throw new Error('Hook is not executable; no configuration changed');
  const current = git(root, ['config', '--get', 'core.hooksPath'], true);
  const expected = resolve(root, '.githooks');
  if ((current && !same(resolve(root, current), expected)) || status.hook.status === 'custom_not_verified') throw new Error('Custom hook configuration preserved; manual integration required');
  // Worktree config prevents redirecting sibling checkouts. Do not migrate special core.worktree setups.
  if (git(root, ['config', '--local', '--get', 'core.worktree'], true)) throw new Error('Custom core.worktree configuration requires manual review');
  if (git(root, ['config', '--local', '--type=bool', '--get', 'core.bare'], true) === 'true') throw new Error('Bare common repository requires manual configuration migration; no configuration changed');
  git(root, ['config', '--local', 'extensions.worktreeConfig', 'true']);
  git(root, ['config', '--worktree', 'core.hooksPath', '.githooks']);
  return inspectIntegration(root);
}
function main(args) {
  let root = process.cwd(), install = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--install-hooks') install = true;
    else if (args[i] === '--root' && args[i + 1]) root = resolve(args[++i]);
    else throw new Error('Usage: node scripts/ecc-integration.mjs [--root Git-root] [--install-hooks]');
  }
  const report = install ? installHooks(root) : inspectIntegration(root);
  console.log(JSON.stringify(report, null, 2));
  if (!report.integrated) process.exitCode = 1;
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(process.argv.slice(2)); } catch (error) { console.error('ECC integration blocked: ' + error.message); process.exitCode = 2; }
}
