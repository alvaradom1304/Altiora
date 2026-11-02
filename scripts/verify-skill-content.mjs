// Verificación de integridad byte-a-byte de la biblioteca de skills original.
// Sin efectos secundarios, sin ejecutar código externo ni conectar modelos.
import {createHash} from 'node:crypto';
import {readFileSync,readdirSync,lstatSync} from 'node:fs';
import {relative,resolve,sep} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT=fileURLToPath(new URL('../',import.meta.url));
const MANIFEST='references/protected-skill-content-baseline-2026.json';

export function gitBlobSha1(bytes){
  return createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
}
function scan(base,prefix=''){
  const found=[],bad=[];
  for(const item of readdirSync(resolve(base,prefix),{withFileTypes:true})){
    // Ignorar exclusivamente resultados de ejecución, nunca documentación o skills nuevas.
    if(item.isDirectory() && ['__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.venv','node_modules'].includes(item.name))continue;
    if(item.isFile() && /\\.(pyc|pyo)$/.test(item.name))continue;
    const rel=prefix?prefix+'/'+item.name:item.name;
    const stat=lstatSync(resolve(base,rel));
    if(stat.isSymbolicLink()){bad.push('Symlink inesperado: skills/'+rel);continue}
    if(stat.isDirectory()){
      const sub=scan(base,rel);found.push(...sub.files);bad.push(...sub.errors);
    }else if(stat.isFile()){
      // Python crea bytecode al ejecutar las suites; no forma parte de una skill fuente.
      // Ignorar únicamente archivos .pyc dentro de __pycache__; otros archivos nuevos siguen bloqueados.
      if(rel.split('/').includes('__pycache__') && rel.endsWith('.pyc'))continue;
      found.push(rel);
    }
    else bad.push('Tipo no permitido: skills/'+rel);
  }
  return {files:found,errors:bad};
}
export function verifySkillContents(root,manifest){
  const errors=[],counts={checked:0,modified:0,missing:0,new:0,unsafe:0};
  if(manifest.schema_version!==1 || manifest.hash_algorithm!=='git_blob_sha1' || !manifest.files || Array.isArray(manifest.files) || typeof manifest.files!=='object'){
    return {status:'FAIL',counts,errors:['Manifiesto de huellas inválido']};
  }
  const skillRoot=resolve(root,'skills');
  let actual;
  try{const s=scan(skillRoot);actual=new Set(s.files);errors.push(...s.errors)}catch(e){
    return {status:'FAIL',counts,errors:['No se pudo explorar skills/: '+e.message]};
  }
  const expected=new Set(Object.keys(manifest.files));
  for(const [name,sha] of Object.entries(manifest.files)){
    if(typeof name!=='string'||name.startsWith('/')||name.includes('\\')||name.split('/').includes('..')||!/^[-_a-zA-Z0-9./]+$/.test(name)||!/^[a-f0-9]{40}$/.test(sha)){
      errors.push('Ruta/hash no permitido: '+name);counts.unsafe++;continue;
    }
    const path=resolve(skillRoot,name),inside=relative(skillRoot,path);
    if(inside.startsWith('..'+sep)||inside==='..'||inside.startsWith(sep)){
      errors.push('Ruta escapa skills/: '+name);counts.unsafe++;continue;
    }
    if(!actual.has(name)){
      errors.push('Falta archivo original: skills/'+name);counts.missing++;continue;
    }
    try{
      const actualSha=gitBlobSha1(readFileSync(path));counts.checked++;
      if(actualSha!==sha){errors.push('Contenido modificado: skills/'+name);counts.modified++}
    }catch(e){errors.push('No se pudo leer: skills/'+name+' ('+e.message+')');counts.missing++}
  }
  for(const name of actual){
    if(!expected.has(name)){errors.push('Archivo nuevo sin revisión: skills/'+name);counts.new++}
  }
  return {status:errors.length?'FAIL':'PASS',baseline_commit:manifest.baseline_commit,counts,errors:errors.slice(0,60),total_errors:errors.length};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  try{
    const manifest=JSON.parse(readFileSync(resolve(ROOT,MANIFEST),'utf8'));
    const report=verifySkillContents(ROOT,manifest);
    process.stdout.write(JSON.stringify(report,null,2)+'\n');
    if(report.status!=='PASS')process.exitCode=1;
  }catch(e){process.stderr.write('Integridad NO_VERIFICADA: '+e.message+'\n');process.exitCode=1}
}
