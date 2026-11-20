import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {gitBlobSha1,verifySkillContents} from './verify-skill-content.mjs';

const root=fileURLToPath(new URL('../',import.meta.url));
const manifest=JSON.parse(readFileSync(resolve(root,'references/protected-skill-content-baseline-2026.json'),'utf8'));

test('la biblioteca original conserva exactamente el contenido de sus 2757 archivos',()=>{
  const r=verifySkillContents(root,manifest);
  assert.equal(Object.keys(manifest.files).length,2757);
  assert.equal(r.status,'PASS',r.errors.join('\n'));
  assert.equal(r.counts.checked,2757);
});

test('detecta recorte, pérdida y ampliación no revisada de archivos',()=>{
  const dir=mkdtempSync(join(tmpdir(),'altiora-content-'));
  try{
    mkdirSync(join(dir,'skills','example'),{recursive:true});
    writeFileSync(join(dir,'skills','example','SKILL.md'),'# versión completa');
    const data={schema_version:1,hash_algorithm:'git_blob_sha1',files:{
      'example/SKILL.md':gitBlobSha1(Buffer.from('# versión completa')),
      'example/SOURCE.md':gitBlobSha1(Buffer.from('fuente'))
    }};
    const first=verifySkillContents(dir,data);
    assert.equal(first.status,'FAIL');
    assert.equal(first.counts.missing,1);
    writeFileSync(join(dir,'skills','example','SKILL.md'),'# recortado');
    writeFileSync(join(dir,'skills','example','NEW.md'),'nuevo');
    mkdirSync(join(dir,'skills','example','__pycache__'),{recursive:true});
    writeFileSync(join(dir,'skills','example','__pycache__','generated.cpython-312.pyc'),'generated cache');
    const second=verifySkillContents(dir,data);
    assert.equal(second.counts.modified,1);
    assert.equal(second.counts.new,1,'solo archivos fuente nuevos deben bloquear; bytecode transitorio se ignora');
  }finally{rmSync(dir,{recursive:true,force:true})}
});

test('impide rutas con escape del checkout',()=>{
  const dir=mkdtempSync(join(tmpdir(),'altiora-content-'));
  try{
    mkdirSync(join(dir,'skills'));
    const r=verifySkillContents(dir,{schema_version:1,hash_algorithm:'git_blob_sha1',files:{'../secrets':gitBlobSha1(Buffer.from('x'))}});
    assert.equal(r.status,'FAIL');
    assert.ok(r.counts.unsafe>0);
  }finally{rmSync(dir,{recursive:true,force:true})}
});
