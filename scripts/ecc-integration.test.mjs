import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, copyFileSync, writeFileSync, readFileSync, rmSync, realpathSync, chmodSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join, dirname } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { inspectIntegration, installHooks } from './ecc-integration.mjs';
const source = fileURLToPath(new URL('../', import.meta.url));
const git = (cwd, ...args) => execFileSync('git', args, { cwd, encoding: 'utf8', windowsHide: true }).trim();
function fixture(t) {
  const temp = realpathSync(tmpdir());
  const root = mkdtempSync(join(temp, 'altiora-ecc-fixture-'));
  t.after(() => { assert.equal(dirname(root), temp); rmSync(root, { recursive: true, force: true }); });
  git(root, 'init', '-q');
  git(root, 'config', 'user.name', 'ECC fixture');
  git(root, 'config', 'user.email', 'ecc-fixture@example.invalid');
  return root;
}
function seed(root) {
  for (const file of ['.githooks/pre-commit', 'scripts/secret-guard.mjs', 'third_party/ecc/SOURCE.md', 'third_party/ecc/LICENSE.txt', 'references/ecc-adoption.json']) {
    mkdirSync(dirname(join(root, file)), { recursive: true });
    copyFileSync(join(source, file), join(root, file));
  }
  const manifest = JSON.parse(readFileSync(join(root, 'references/ecc-adoption.json'), 'utf8'));
  manifest.capabilities = [{ id: 'secret-guard', paths: ['scripts/secret-guard.mjs', '.githooks/pre-commit'] }];
  writeFileSync(join(root, 'references/ecc-adoption.json'), JSON.stringify(manifest));
}
test('missing files do not become integrated merely because hooksPath is configured', t => {
  const root = fixture(t);
  git(root, 'config', 'core.hooksPath', '.githooks');
  const r = inspectIntegration(root);
  assert.equal(r.integrated, false);
  assert.equal(r.hook.status, 'missing');
  assert.equal(r.nativePlugin, 'not_assessed');
});
test('present adaptation without hook activation is reported separately', t => {
  const root = fixture(t); seed(root);
  const r = inspectIntegration(root);
  assert.equal(r.adaptationsPresent, true);
  assert.equal(r.hook.status, 'not_configured');
  assert.equal(r.integrated, false);
});
test('installer preserves a custom hook configuration', t => {
  const root = fixture(t); seed(root);
  git(root, 'config', 'core.hooksPath', '.custom-hooks');
  assert.throws(() => installHooks(root), /custom/i);
  assert.equal(git(root, 'config', 'core.hooksPath'), '.custom-hooks');
});
test('worktree-scoped activation does not set hooksPath in the other worktree', t => {
  const root = fixture(t); seed(root);
  git(root, 'add', '.');
  git(root, '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture');
  const linked = join(root, 'linked checkout');
  git(root, 'worktree', 'add', '-qb', 'linked-ecc', linked);
  const r = installHooks(linked);
  assert.equal(r.hook.status, 'configured');
  assert.equal(r.integrated, true);
  assert.equal(spawnSync('git', ['config', '--get', 'core.hooksPath'], { cwd: root, encoding: 'utf8' }).status, 1);
  assert.equal(inspectIntegration(root).hook.status, 'not_configured');
  assert.equal(installHooks(linked).hook.status, 'configured');
});
test('actual Git commit blocks a staged fake secret without printing it, then accepts clean content', t => {
  const root = fixture(t); seed(root); installHooks(root);
  const fake = 'gh' + 'p_' + 'z'.repeat(36);
  writeFileSync(join(root, 'sample.txt'), fake + '\n');
  git(root, 'add', '.');
  const denied = spawnSync('git', ['-c', 'commit.gpgsign=false', 'commit', '-m', 'fixture'], { cwd: root, encoding: 'utf8', windowsHide: true });
  assert.notEqual(denied.status, 0);
  assert.match(denied.stderr, /secret-guard/);
  assert.ok(!(denied.stdout + denied.stderr).includes(fake));
  writeFileSync(join(root, 'sample.txt'), 'clean fixture\n');
  git(root, 'add', 'sample.txt');
  git(root, '-c', 'commit.gpgsign=false', 'commit', '-qm', 'clean fixture');
});
test('adoption manifest cannot escape the root or claim integration from invalid provenance', t => {
  const root = fixture(t); seed(root);
  const path = join(root, 'references/ecc-adoption.json');
  const m = JSON.parse(readFileSync(path, 'utf8'));
  m.capabilities[0].paths = ['../outside'];
  writeFileSync(path, JSON.stringify(m));
  assert.throws(() => inspectIntegration(root), /path/i);
  m.capabilities[0].paths = ['scripts/secret-guard.mjs']; m.reviewedCommit = 'main';
  writeFileSync(path, JSON.stringify(m));
  assert.throws(() => inspectIntegration(root), /commit/i);
});

test('same-path custom/no-op hook is preserved and never reported integrated', t => {
  const root = fixture(t); seed(root);
  writeFileSync(join(root, '.githooks/pre-commit'), '#!/bin/sh\nexit 0\n');
  git(root, 'config', 'core.hooksPath', '.githooks');
  assert.equal(inspectIntegration(root).integrated, false);
  assert.equal(inspectIntegration(root).hook.status, 'custom_not_verified');
  assert.throws(() => installHooks(root), /custom/i);
  assert.equal(readFileSync(join(root, '.githooks/pre-commit'), 'utf8'), '#!/bin/sh\nexit 0\n');
});
test('a hook directory is not a regular hook file', t => {
  const root = fixture(t); seed(root);
  rmSync(join(root, '.githooks/pre-commit'));
  mkdirSync(join(root, '.githooks/pre-commit'));
  assert.equal(inspectIntegration(root).integrated, false);
  assert.throws(() => installHooks(root), /files|hook/i);
});
test('POSIX non-executable hook is rejected before any configuration write', { skip: process.platform === 'win32' }, t => {
  const root = fixture(t); seed(root);
  chmodSync(join(root, '.githooks/pre-commit'), 0o644);
  assert.equal(inspectIntegration(root).hook.status, 'not_executable');
  assert.throws(() => installHooks(root), /executable/i);
  assert.equal(spawnSync('git', ['config', '--get', 'extensions.worktreeConfig'], { cwd: root }).status, 1);
});

test('bare common repository is rejected without changing configuration or breaking its worktree', t => {
  const root = fixture(t); seed(root);
  git(root, 'add', '.'); git(root, '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture');
  const bare = join(root, 'bare repo');
  git(root, 'clone', '--bare', '.', bare);
  const linked = join(root, 'bare worktree');
  git(bare, 'worktree', 'add', '-qb', 'bare-ecc', linked);
  for (const raw of ['true', 'yes', '1']) {
    git(bare, 'config', '--local', 'core.bare', raw);
    assert.throws(() => installHooks(linked), /bare/i);
    assert.equal(spawnSync('git', ['config', '--local', '--get', 'extensions.worktreeConfig'], { cwd: bare }).status, 1);
    assert.equal(realpathSync(git(linked, 'rev-parse', '--show-toplevel')), realpathSync(linked));
  }
});
