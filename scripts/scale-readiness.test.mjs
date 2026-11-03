// Guardias no destructivas del programa de escalamiento Altiora.
// No requieren red, secretos, apps locales ni llamadas a modelos.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=(p)=>readFileSync(resolve(root,p),'utf8').replace(/\r\n/g,'\n');
const policy='docs/operations/ALTIORA-SCALE-ZERO-LOSS-V4.md';
const revenue='docs/altiora-business/REVENUE-SPRINT-30-60-90.md';

test('la política preserva el inventario y exige rollback y QA',()=>{
  const text=read(policy);
  for(const term of ['Graphify','altiora-shared','rollback','Revenue Engine','Cash-First','Loops adaptativos','No declarar']) {
    assert.ok(text.toLowerCase().includes(term.toLowerCase()),'Falta control: '+term);
  }
});

test('la regla Antigravity sigue conectada a la fuente canónica',()=>{
  const rule=read('.agents/rules/altiora-sync.md');
  const generator=read('scripts/build-antigravity.mjs');
  const routing=read('team/ROUTING.md');
  for(const source of [rule,generator,routing]){
    assert.ok(source.includes('ALTIORA-SCALE-ZERO-LOSS-V4.md'),'Una entrada no incluye la política canónica');
  }
  assert.ok(rule.includes('trigger: always_on'));
  assert.ok(rule.includes('No declarar «todo activo»'));
  assert.ok(routing.includes('REVENUE-SPRINT-30-60-90.md'));
});

test('los 18 repositorios son candidatos únicos; ninguno se declara instalado',()=>{
  const data=JSON.parse(read('references/scale-enhancement-repositories-2026.json'));
  assert.equal(data.repositories.length,18);
  assert.equal(new Set(data.repositories.map(x=>x.id.toLowerCase())).size,18);
  for(const item of data.repositories){
    assert.equal(item.url,'https://github.com/'+item.id);
    assert.equal(item.state,'DISCOVERED_NOT_INSTALLED');
    assert.equal(item.verification,'PENDING_LICENSE_SECURITY_VERSION_COMPATIBILITY');
  }
  for(const group of ['consulting','growth','audiovisual','quality']){
    assert.ok(data.repositories.some(x=>x.category===group));
  }
});

test('el motor de ingresos no inventa ventas y exige cobros, costos y consentimiento',()=>{
  const text=read(revenue);
  for(const term of ['pipeline.json','cero clientes de pago','consentimiento','cobro','contribución','Gate 30','Gate 60','Gate 90']){
    assert.ok(text.toLowerCase().includes(term.toLowerCase()),'Falta control de negocio: '+term);
  }
});
