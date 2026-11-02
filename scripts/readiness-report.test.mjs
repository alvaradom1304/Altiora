import test from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {assessAltiora} from './readiness-report.mjs';

const root=fileURLToPath(new URL('../',import.meta.url));
test('el informe no equipara skills con madurez empresarial ni conecta MCP ficticiamente',()=>{
  const r=assessAltiora(root);
  assert.equal(r.repository.protected_capabilities,'PASS');
  assert.equal(r.skill_report.type,'DOCUMENT_STRUCTURE_NOT_BUSINESS_READINESS');
  assert.equal(r.ai_connectors.status,'CONFIGURED_NOT_LIVE_TESTED');
  assert.equal(r.commercial.pricing_validated,false);
  assert.ok(r.commercial.status!=='VALIDATED');
});
test('cero clientes reportados mantienen en HOLD el escalamiento',()=>{
  const r=assessAltiora(root);
  if(r.commercial.paying_clients_reported===0){
    assert.equal(r.scaling_gate,'HOLD');
    assert.equal(r.commercial.status,'NOT_VALIDATED');
  }
});
