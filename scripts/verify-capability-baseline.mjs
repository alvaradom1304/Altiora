// Compara capacidades del checkout contra un inventario protegido de Git.
// No escribe archivos, no conecta servicios ni elimina conocimientos.
// Cualquier retiro deliberado exige una modificación explícita y revisada del manifiesto.
import {readFileSync,lstatSync,existsSync} from 'node:fs';
import {resolve,relative,sep} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT=fileURLToPath(new URL('../',import.meta.url));
const DEFAULT='references/capability-protection-baseline-2026.json';

export function verifyCapabilityBaseline(root,manifest){
  const errors=[], stats={skills:0,roles:0,workflows:0,critical:0};
  const groups=[
    {key:'skills',names:manifest.skills,make:n=>'skills/'+n+'/SKILL.md',type:'skills'},
    {key:'roles',names:manifest.roles,make:n=>'team/roles/'+n,type:'roles'},
    {key:'workflows',names:manifest.workflows,make:n=>'.github/workflows/'+n,type:'workflows'},
    {key:'critical_files',names:manifest.critical_files,make:n=>n,type:'critical'}
  ];
  if(manifest.schema_version!==1)errors.push('Versión de manifiesto desconocida');
  for(const g of groups){
    if(!Array.isArray(g.names)){errors.push('Lista inválida: '+g.key);continue}
    if(new Set(g.names).size!==g.names.length)errors.push('Entradas duplicadas: '+g.key);
    for(const name of g.names){
      if(typeof name!=='string'||!name||name.includes('\\')||name.startsWith('/')||name.split('/').includes('..')){
        errors.push('Ruta insegura en '+g.key+': '+String(name));continue
      }
      const rel=g.make(name),path=resolve(root,rel),inside=relative(root,path);
      if(inside.startsWith('..'+sep)||inside==='..'||inside.startsWith(sep)){
        errors.push('Ruta fuera del checkout: '+rel);continue
      }
      try{
        const stat=lstatSync(path);
        if(!stat.isFile()||stat.isSymbolicLink())errors.push('No es archivo regular: '+rel);
        else if(stat.size===0)errors.push('Archivo protegido vacío: '+rel);
        else stats[g.type]++;
      }catch{
        errors.push('Capacidad protegida desaparecida: '+rel);
      }
    }
  }
  return {status:errors.length?'FAIL':'PASS',baseline_commit:manifest.baseline_commit,verified:stats,errors};
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  let report;
  try{
    const manifest=JSON.parse(readFileSync(resolve(ROOT,DEFAULT),'utf8'));
    report=verifyCapabilityBaseline(ROOT,manifest);
  }catch(error){
    report={status:'FAIL',errors:['No se pudo verificar inventario: '+error.message]};
  }
  process.stdout.write(JSON.stringify(report,null,2)+'\n');
  if(report.status!=='PASS')process.exitCode=1;
}
