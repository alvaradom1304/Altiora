import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {verifyCapabilityBaseline} from './verify-capability-baseline.mjs';

const root=fileURLToPath(new URL('../',import.meta.url));
const manifest=JSON.parse(readFileSync(resolve(root,'references/capability-protection-baseline-2026.json'),'utf8'));

test('no se perdió ninguna skill, rol, workflow ni archivo del baseline de Altiora',()=>{
  assert.equal(manifest.skills.length,355);
  assert.equal(manifest.roles.length,22);
  assert.equal(manifest.workflows.length,5);
  const out=verifyCapabilityBaseline(root,manifest);
  assert.equal(out.status,'PASS',out.errors.join('\n'));
  assert.equal(out.verified.skills,355);
});

test('un retiro de skill y un conector ausente se detectan sin modificar nada',()=>{
  const dir=mkdtempSync(join(tmpdir(),'altiora-baseline-'));
  try{
    mkdirSync(join(dir,'skills','keep'),{recursive:true});
    writeFileSync(join(dir,'skills','keep','SKILL.md'),'# skill');
    const mini={schema_version:1,baseline_commit:'fixture',skills:['keep','deleted'],roles:[],workflows:[],critical_files:['.mcp.json']};
    const out=verifyCapabilityBaseline(dir,mini);
    assert.equal(out.status,'FAIL');
    assert.ok(out.errors.some(e=>e.includes('skills/deleted/SKILL.md')));
    assert.ok(out.errors.some(e=>e.includes('.mcp.json')));
  }finally{rmSync(dir,{recursive:true,force:true})}
});

test('un manifiesto con rutas peligrosas o duplicadas falla cerrado',()=>{
  const dir=mkdtempSync(join(tmpdir(),'altiora-baseline-'));
  try{
    const out=verifyCapabilityBaseline(dir,{schema_version:1,skills:['../escape','../escape'],roles:[],workflows:[],critical_files:[]});
    assert.equal(out.status,'FAIL');
    assert.ok(out.errors.some(e=>e.includes('duplicadas')));
    assert.ok(out.errors.some(e=>e.includes('insegura')));
  }finally{rmSync(dir,{recursive:true,force:true})}
});
