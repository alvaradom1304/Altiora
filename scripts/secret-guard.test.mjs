import test from 'node:test';
import assert from 'node:assert/strict';
import { scanDiff, scanLine } from './secret-guard.mjs';

// Los valores falsos se arman en tiempo de ejecución para que este archivo
// no contenga cadenas que el propio guardián detectaría.
const rep = (c, n) => c.repeat(n);
const fake = {
  aws: 'AK' + 'IA' + rep('Q', 16),
  github: 'gh' + 'p_' + rep('a', 36),
  anthropic: 'sk-' + 'ant-' + rep('b', 30),
  google: 'AI' + 'za' + rep('c', 35),
  nvidia: 'nv' + 'api-' + rep('d', 32),
  pem: '-----BEGIN ' + 'PRIVATE KEY-----',
};

const diffOf = (file, lines) =>
  [`diff --git a/${file} b/${file}`, `--- a/${file}`, `+++ b/${file}`, `@@ -0,0 +1,${lines.length} @@`, ...lines.map((l) => `+${l}`)].join('\n');

test('detecta claves de proveedores conocidos', () => {
  for (const [name, value] of Object.entries(fake)) {
    assert.ok(scanLine(`const k = "${value}";`).length > 0, `no detectó ${name}`);
  }
});

test('detecta secreto asignado y respeta valores de ejemplo', () => {
  assert.deepEqual(scanLine(`api_key = "${'z9'.repeat(8)}"`), ['secreto asignado']);
  assert.deepEqual(scanLine('api_key = "your-api-key-here"'), []);
  assert.deepEqual(scanLine('password: "${DB_PASSWORD}"'), []);
  assert.deepEqual(scanLine('token = process.env.TOKEN'), []);
});

test('no confunde sk- dentro de otra palabra', () => {
  assert.deepEqual(scanLine('task-' + 'Altiora' + rep('x', 40) + '.xml'), []);
});

test('la marca de excepción revisada silencia la línea', () => {
  assert.deepEqual(scanLine(`"${fake.github}" // secret-guard: allow`), []);
});

test('scanDiff informa archivo y línea sin mostrar el valor', () => {
  const findings = scanDiff(diffOf('src/config.js', ['const ok = 1;', `const t = "${fake.github}";`]));
  assert.equal(findings.length, 1);
  assert.equal(findings[0].file, 'src/config.js');
  assert.equal(findings[0].line, 2);
  assert.ok(!JSON.stringify(findings).includes(fake.github));
});

test('ignora líneas borradas y plantillas .env.example', () => {
  const removed = ['--- a/a.js', '+++ b/a.js', '@@ -1 +0,0 @@', `-const t = "${fake.aws}";`].join('\n');
  assert.deepEqual(scanDiff(removed), []);
  assert.deepEqual(scanDiff(diffOf('.env.example', [`API_KEY=${fake.anthropic}`])), []);
});
