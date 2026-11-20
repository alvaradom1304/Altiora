// Reglas de contexto: no truncar silenciosamente ni perder instrucciones históricas.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {gitBlobSha1} from './verify-skill-content.mjs';

const root=fileURLToPath(new URL('../',import.meta.url));
const load=p=>readFileSync(new URL('../'+p,import.meta.url));

test('AGENTS.md se mantiene bajo presupuesto de carga de reglas de 24KB',()=>{
  const bytes=load('AGENTS.md');
  assert.ok(bytes.length<24000,'AGENTS.md supera 24KB: '+bytes.length);
  for(const term of ['AGENTS-FULL-ARCHIVE-2026-11-02.md','ALTIORA-SCALE-ZERO-LOSS-V4.md','team/ROUTING.md','continuity/checkpoint.json']){
    assert.ok(bytes.toString('utf8').includes(term),'Falta referencia obligatoria: '+term);
  }
});

test('archivo completo original de agentes preservado exactamente por SHA de Git',()=>{
  const original=load('AGENTS-FULL-ARCHIVE-2026-11-02.md');
  assert.equal(gitBlobSha1(original),'6a9be69879b2b87a25ca154aff80d72a012859b6');
  assert.ok(original.toString('utf8').includes('ALTIORA_COORDINATOR_MODE_END'));
  assert.ok(original.length>26000);
});

test('reglas on-demand no borran las secciones de negocio ni herramientas del archivo recuperable',()=>{
  const text=load('AGENTS-FULL-ARCHIVE-2026-11-02.md').toString('utf8');
  for(const term of ['Selección automática de skills','Economía de razonamiento','Meta Ads','Dirección de proyectos integrales','Seguridad de habilidades externas']){
    assert.ok(text.includes(term), 'Falta bloque histórico: '+term);
  }
});
