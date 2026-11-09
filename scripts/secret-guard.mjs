#!/usr/bin/env node
// Altiora · guardián de secretos para commits.
// Revisa solo las líneas AÑADIDAS en el área de preparación (git diff --cached) y
// bloquea el commit si alguna parece una credencial. Nunca imprime el valor encontrado.
//
// Patrones base adaptados de ECC (affaan-m/ECC, scripts/hooks/governance-capture.js,
// commit d2ef2680594f9a17526a6e1a2e18b3d242c5d17b, licencia MIT; ver third_party/ecc/).
// Altiora añade patrones de proveedores que usa y la lista de marcadores de ejemplo.
//
// Uso: node scripts/secret-guard.mjs            (lo llama .githooks/pre-commit)
// Falso positivo revisado por una persona: añadir «secret-guard: allow» en esa línea.

import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

export const PATTERNS = [
  // De ECC (governance-capture.js)
  { name: 'clave AWS', re: /(?<![A-Za-z0-9])(?:AKIA|ASIA)[A-Z0-9]{16}/ },
  { name: 'secreto asignado', re: /(?:secret|password|passwd|token|api[_-]?key)\s*[:=]\s*["'][^"'\s]{8,}/i, generic: true },
  { name: 'clave privada', re: /-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/ },
  { name: 'JWT', re: /eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/ },
  { name: 'token de GitHub', re: /gh[pousr]_[A-Za-z0-9_]{36,}/ },
  // Añadidos por Altiora
  { name: 'clave de Anthropic', re: /(?<![A-Za-z0-9])sk-ant-[A-Za-z0-9_-]{20,}/ },
  { name: 'clave de OpenAI', re: /(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{32,}/ },
  { name: 'clave de Google', re: /AIza[0-9A-Za-z_-]{35}/ },
  { name: 'token de Slack', re: /xox[abprs]-[A-Za-z0-9-]{10,}/ },
  { name: 'clave de Stripe', re: /[rs]k_live_[0-9A-Za-z]{20,}/ },
  { name: 'clave de NVIDIA', re: /nvapi-[A-Za-z0-9_-]{30,}/ },
];

// Valores de ejemplo que no son secretos (solo se aplican al patrón genérico).
const PLACEHOLDER = /(your|tu|example|ejemplo|placeholder|changeme|dummy|fake|redacted|xxxx|\*\*\*\*|<[^>]+>|\$\{|process\.env|os\.environ)/i;
const SAFE_FILES = /(^|\/)\.env\.(example|sample|template)$/i;
const ALLOW_MARK = 'secret-guard: allow';

export function scanLine(line) {
  if (line.includes(ALLOW_MARK)) return [];
  const hits = [];
  for (const { name, re, generic } of PATTERNS) {
    const m = re.exec(line);
    if (!m) continue;
    if (generic && PLACEHOLDER.test(m[0])) continue;
    hits.push(name);
  }
  return hits;
}

// Recorre un diff unificado (-U0) y devuelve [{ file, line, names }].
export function scanDiff(diffText) {
  const findings = [];
  let file = null;
  let lineNo = 0;
  for (const raw of diffText.split(/\r?\n/)) {
    if (raw.startsWith('+++ ')) {
      const p = raw.slice(4).trim();
      file = p === '/dev/null' ? null : p.replace(/^b\//, '');
      continue;
    }
    const hunk = /^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@/.exec(raw);
    if (hunk) { lineNo = Number(hunk[1]); continue; }
    if (!file || SAFE_FILES.test(file)) continue;
    if (raw.startsWith('+') && !raw.startsWith('+++')) {
      const names = scanLine(raw.slice(1));
      if (names.length) findings.push({ file, line: lineNo, names });
      lineNo += 1;
    }
  }
  return findings;
}

function main() {
  let diff;
  try {
    diff = execFileSync('git', ['diff', '--cached', '-U0', '--no-color', '--no-ext-diff', '--diff-filter=ACMR'], {
      encoding: 'utf8',
      maxBuffer: 256 * 1024 * 1024,
    });
  } catch (error) {
    console.error(`secret-guard: no pude leer el área de preparación (${error.message}). Commit bloqueado por seguridad.`);
    return 1;
  }
  const findings = scanDiff(diff);
  if (!findings.length) return 0;
  console.error('secret-guard: el commit contiene posibles credenciales. No se ha hecho el commit.');
  for (const f of findings) console.error(`  ${f.file}:${f.line}  ${f.names.join(', ')}`);
  console.error('Quita el valor y léelo de una variable de entorno o de un .env que no se versiona.');
  console.error(`Si una persona revisó que es un falso positivo, añade «${ALLOW_MARK}» en esa línea.`);
  console.error('Las IAs de Altiora no usan --no-verify ni añaden la marca sin aprobación del dueño.');
  return 1;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = main();
}
