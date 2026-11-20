// Nota de preparación empresarial V4, calculada y común a todas las IAs.
// Solo lectura: no inicia servicios, no conecta cuentas y no lee secretos.
// Pesos y escala 0-5: docs/operations/NOTA-V4.md. Ninguna IA la estima a ojo.
import {readFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT=fileURLToPath(new URL('../',import.meta.url));
const load=(root,p)=>readFileSync(resolve(root,p),'utf8');
const json=(root,p)=>JSON.parse(load(root,p));

export const V4_AXES={integrity_recovery:20,automation_agents_qa:15,connectors_live:15,demand_sales:25,deliverable_quality:15,economy_capacity:10};
const KIND_LEVEL={design:1,partial:2,test:3,real:4};
const sourceOk=(root,s)=>typeof s==='string'&&s.length>0&&(/^(cmd|url):/.test(s)||existsSync(resolve(root,s.replace(/[#:].*$/,''))));

export function demandCap(pipeline){
  const paying=Number.isInteger(pipeline.confirmed_paying_clients)?pipeline.confirmed_paying_clients:0;
  const rs=pipeline.research_status||{};
  if(paying>=2)return 5;
  if(paying>=1)return 4;
  if((rs.interviews_completed||0)>0||(pipeline.opportunities||[]).length>0)return 3;
  if(pipeline.outreach_sent===true||(rs.contacts_sent||0)>0)return 2;
  return 1;
}

export function scoreV4(root,evidence,pipeline,documentScore=null){
  const p0=(evidence.p0_open||[]).map(p=>p.id);
  const caps={demand_sales:demandCap(pipeline),deliverable_quality:p0.length?2:5};
  const axes={};const warnings=[];let total=0;
  for(const [id,weight] of Object.entries(V4_AXES)){
    const a=evidence.axes?.[id]||{};
    const items=Array.isArray(a.evidence)?a.evidence:[];
    const valid=items.filter(e=>KIND_LEVEL[e.kind]&&sourceOk(root,e.source));
    if(valid.length<items.length)warnings.push(`${id}: ${items.length-valid.length} evidencia(s) sin tipo o fuente válida ignorada(s)`);
    const realDates=new Set(valid.filter(e=>e.kind==='real').map(e=>e.date));
    const supported=realDates.size>=2?5:Math.max(0,...valid.map(e=>KIND_LEVEL[e.kind]));
    const declared=Number.isInteger(a.level)?Math.min(Math.max(a.level,0),5):0;
    const cap=caps[id]??5;
    const level=Math.min(declared,supported,cap);
    if(level<declared)warnings.push(`${id}: declarado ${declared}, aplicado ${level} (evidencia ${supported}, tope ${cap})`);
    const points=Math.round(weight*level/5*10)/10;
    total+=points;
    axes[id]={weight,declared,supported,cap,level,points,status:level===0?'NOT_VERIFIED':'EVIDENCED'};
  }
  const L=id=>axes[id].level;
  const decision=p0.length||L('demand_sales')<2?'HOLD_SCALE':L('demand_sales')>=4&&L('deliverable_quality')>=4&&L('economy_capacity')>=3?'READY_FOR_REPEATABLE_DELIVERY':L('deliverable_quality')>=3?'READY_FOR_PILOT':'HOLD_SCALE';
  const score=Math.round(total*10)/10;
  const doc=documentScore===null?'':` La nota documental de skills (${documentScore}/100) mide la redacción de las skills, no la madurez de la empresa.`;
  return {rubric:evidence.rubric||'NOTA-V4',assessed_on:evidence.assessed_on||null,score,max:100,decision,p0_open:p0,axes,warnings,summary:`Preparación empresarial V4: ${score}/100 (${decision}), evaluada el ${evidence.assessed_on||'sin fecha'}.${doc}`};
}

export function assessAltiora(root){
  const evidencePath='quality/readiness-evidence.json';
  const m=existsSync(resolve(root,'quality/skills-report.md'))?load(root,'quality/skills-report.md').match(/media \*\*([\d.,]+)\/100\*\*/i):null;
  const documentScore=m?Number(m[1].replace(',','.')):null;
  if(!existsSync(resolve(root,evidencePath)))return {readiness_v4:{score:null,decision:'HOLD_SCALE',summary:`Preparación empresarial V4: NOT_VERIFIED (falta ${evidencePath}).`}};
  return {readiness_v4:scoreV4(root,json(root,evidencePath),json(root,'docs/altiora-business/pipeline.json'),documentScore)};
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  try{const r=assessAltiora(ROOT);process.stdout.write(process.argv.includes('--resumen')?r.readiness_v4.summary+'\n':JSON.stringify(r,null,2)+'\n')}
  catch(e){process.stderr.write('Readiness NO_VERIFICADO: '+e.message+'\n');process.exitCode=1}
}
