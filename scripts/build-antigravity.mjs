// Altiora: generador nativo de Google Antigravity. Se ejecuta después de build-agents.mjs.
// Uso: node scripts/build-antigravity.mjs [--check]
import {readFile,writeFile,mkdir,readdir,rm} from 'node:fs/promises';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {loadSkills,loadAgents} from './skill-catalog.mjs';
const root=fileURLToPath(new URL('../',import.meta.url));
const check=process.argv.includes('--check');
const MARK="<!-- Generado con npm run antigravity:build. No editar manualmente. -->";
const RULE_SYNC="---\ntrigger: always_on\ndescription: \"Mantener sincronizados agentes, skills y reglas de Altiora entre Claude Code y Google Antigravity.\"\n---\n\n# Sincronización de Altiora\n- Las fuentes originales son `team/agents.json`, `team/roles/` y `skills/`; nunca editar los archivos generados en `.claude/` y `.agents/` como fuente.\n- Cuando cambien las fuentes, ejecutar `npm run agents:build` y `npm run check`. Cualquier diferencia debe corregirse antes de integrar a main.\n- Leer AGENTS.md, GEMINI.md y el brief. Los roles son configuraciones; no equivalen a sesiones autónomas abiertas.\n- Solicitar aprobación específica antes de gastar, publicar, contactar clientes, cambiar cuentas o permisos.\n- Para cualquier migración, optimización, integración o escalamiento, aplicar la política canónica en docs/operations/ALTIORA-SCALE-ZERO-LOSS-V4.md: preservar primero, loops acotados, QA y Revenue Engine.\n- No declarar «todo activo»: verificar cada conector en la sesión local y registrar estados distintos de configuración, conexión y pruebas.\n";
const RULE_MARKETING="---\ntrigger: model_decision\ndescription: \"Activar para marketing, branding, anuncios, Reels, TikTok, Instagram, Facebook, investigación de videos, producto ganador, captación, publicidad o ventas.\"\n---\n\n# Selección de equipo Altiora\n1. Leer `creative-ads-os/WORK_ROUTER.md` y el brief del cliente.\n2. Elegir director, especialistas y skills pertinentes: no cargar todo el catálogo indiscriminadamente.\n3. Para anuncios explorar humor, emoción, demostración y valor, según el producto y el público.\n4. Estudiar referencias sin copiarlas; priorizar actuaciones, videos de producto real, sonido y motion graphics originales.\n5. Separar hipótesis, métricas verificadas y entregables. Conversiones y margen importan más que la viralidad sola.\n6. Sin autorización no publicar anuncios, no gastar ni enviar mensajes a terceros.\n";
const agents=await loadAgents(root);
const rows=await loadSkills(root);
const outputs=new Map();
for(const r of rows){
 const {name,folder,description}=r;
 outputs.set(`.agents/skills/${name}/SKILL.md`,`---
name: ${name}
description: ${JSON.stringify(description)}
---

${MARK}

# ${name}
Esta skill se expone a Antigravity. **Leer por completo** el protocolo original \`skills/${folder}/SKILL.md\` (relativo: ../../../skills/${folder}/SKILL.md) antes de actuar.
Respetar documentación de apoyo, evidencias, pruebas, privacidad, derechos y autorizaciones. No inventar resultados.
`);
}
for(const a of agents){
 outputs.set(`.agents/agents/${a.id}.md`,`---
name: ${a.id}
description: ${JSON.stringify(a.when+' Equipo Altiora: '+a.id+'.')}
subagent: true
mainAgent: false
model: inherit
commandExecutionPolicy: sandbox
---

${MARK}

# Subagente ${a.id}
Leer **íntegramente** el prompt del rol en \`team/agents/${a.id}.md\` (relativo: ../../team/agents/${a.id}.md) antes de iniciar la tarea.
Leer AGENTS.md y las instrucciones del brief. Para marketing y anuncios, consultar creative-ads-os/WORK_ROUTER.md.
Usar únicamente las skills pertinentes a este encargo (fuentes en skills/ y espejos en .agents/skills/).
Delegar y coordinar según las herramientas disponibles; nunca fingir sesiones, hechos, acceso o permisos. Reportar evidencia, límites y estado real.
`);
}
outputs.set('.agents/rules/altiora-sync.md',RULE_SYNC);
outputs.set('.agents/rules/altiora-marketing.md',RULE_MARKETING);
let errors=0;
for(const [path,content] of outputs){
 const file=resolve(root,path);
 if(check){let current=null;try{current=(await readFile(file,'utf8')).replace(/\r\n/g,'\n')}catch{}if(current!==content){console.error('Desactualizado: '+path);errors++;}}
 else {await mkdir(resolve(file,'..'),{recursive:true});await writeFile(file,content);}
}
for(const [dir,ext] of [['.agents/skills','SKILL.md'],['.agents/agents',null]]){
 const base=resolve(root,dir);
 for(const item of await readdir(base,{withFileTypes:true}).catch(()=>[])){
  const path=dir+'/'+item.name+(ext?'/'+ext:'');
  if(outputs.has(path))continue;
  let old='';try{old=await readFile(resolve(root,path),'utf8')}catch{}
  if(!old.includes(MARK))continue;
  if(check){console.error('Generado obsoleto: '+path);errors++}
  else await rm(resolve(root,dir,item.name),{recursive:true,force:true});
 }
}
if(errors){console.error('Ejecutar npm run agents:build para re-sincronizar.');process.exit(1)}
console.log(`${check?'OK':'Generados'} Antigravity: ${agents.length} agentes, ${rows.length} skills, 2 reglas.`);
