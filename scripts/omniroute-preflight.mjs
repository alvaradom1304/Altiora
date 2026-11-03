#!/usr/bin/env node
// Read-only OmniRoute probe. Loopback only; no external provider calls or writes.
// Usage: node scripts/omniroute-preflight.mjs [--json]
// Optional: OMNIROUTE_API_KEY (never printed; GET /v1/models only).
import { execFileSync } from 'node:child_process';

const ROOT = 'http://127.0.0.1:20128';
const limit = 3000;
const report = { name: 'OmniRoute', checked_at: new Date().toISOString(),
  base_url: ROOT, execution_context: 'THIS_MACHINE_ONLY',
  service: 'NOT_TESTED', models: 'NOT_TESTED', authenticated: false,
  routing: 'NOT_TESTED', generation: 'NOT_TESTED',
  cost_saving: 'NOT_MEASURED', notes: [] };
const ctl = () => AbortSignal.timeout(limit);
const baseHeaders = { 'Accept': 'application/json' };
async function probe(path, headers) {
  try {
    const response = await fetch(ROOT + path, { method: 'GET', headers, signal: ctl(), redirect: 'error' });
    return {status: response.status, ok: response.ok};
  } catch (err) {
    return {error: err?.name === 'TimeoutError' ? 'TIMEOUT' : 'CONNECTION_FAILED'};
  }
}
const server = await probe('/');
if (server.error) {
  report.service = 'UNREACHABLE';
  report.notes.push('No process could be verified at 127.0.0.1:20128. This does not prove OmniRoute is absent.');
} else {
  report.service = 'HTTP_RESPONDED_NOT_IDENTIFIED';
  report.notes.push('An HTTP response on the port is not proof that the process is OmniRoute.');
  const key = process.env.OMNIROUTE_API_KEY;
  const headers = key ? {...baseHeaders, Authorization: 'Bearer ' + key} : baseHeaders;
  const result = await probe('/v1/models', headers);
  report.authenticated = Boolean(key);
  report.models = result.error ? result.error : result.ok ? 'ENDPOINT_RESPONDED_OK_CONTENT_NOT_VERIFIED'
    : result.status === 401 || result.status === 403 ? 'AUTH_REQUIRED_OR_DENIED'
    : 'HTTP_' + result.status;
  report.notes.push('Model catalog HTTP status only; does not prove a provider can generate content.');
}
report.notes.push('No paid inference, provider activation, prompt rewriting, or client configuration performed.');
if (process.argv.includes('--json')) console.log(JSON.stringify(report,null,2));
else console.log(Object.entries(report).map(([k,v])=>k+': '+(Array.isArray(v)?v.join(' | '):v)).join('\n'));
