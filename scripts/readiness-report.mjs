// Informe conservador: distingue existencia en Git de disponibilidad en sesión
// y de resultados comerciales. Solo lectura. No escanea secretos ni inicia conectores.
import {readFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {verifyCapabilityBaseline} from './verify-capability-baseline.mjs';
import {verifySkillContents} from './verify-skill-content.mjs';

const ROOT=fileURLToPath(new URL('../',import.meta.url));
const load=(root,p)=>readFileSync(resolve(root,p),'utf8');
const json=(root,p)=>JSON.parse(load(root,p));

// Nota V4 común a todas las IAs: pesos de INDEPENDENT-READINESS-AUDIT-V4, nivel limitado
// por el tipo de evidencia y por hechos del repo. Ninguna IA la estima a ojo.
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

export function scoreV4(root,evidence,pipeline,integrityPass,documentScore=null){
  const p0=(evidence.p0_open||[]).map(p=>p.id);
  const caps={integrity_recovery:integrityPass?5:1,demand_sales:demandCap(pipeline),deliverable_quality:p0.length?2:5};
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
  return {rubric:evidence.rubric||'INDEPENDENT-READINESS-AUDIT-V4',assessed_on:evidence.assessed_on||null,score,max:100,decision,p0_open:p0,axes,warnings,summary:`Preparación empresarial V4: ${score}/100 (${decision}).${doc}`};
}

export function assessAltiora(root){
  const manifest=json(root,'references/capability-protection-baseline-2026.json');
  const protectedState=verifyCapabilityBaseline(root,manifest);
  const contentManifest=json(root,'references/protected-skill-content-baseline-2026.json');
  const contentState=verifySkillContents(root,contentManifest);
  const pipeline=json(root,'docs/altiora-business/pipeline.json');
  const score=load(root,'quality/skills-report.md');
  const match=score.match(/(\d+) skills; media \*\*([\d.,]+)\/100\*\*/i);
  const scoreInfo=match?{reported_skills:Number(match[1]),reported_document_score:Number(match[2].replace(',','.')),type:'DOCUMENT_STRUCTURE_NOT_BUSINESS_READINESS'}:{reported_skills:null,reported_document_score:null,type:'NOT_PARSED'};
  const clients=Number.isInteger(pipeline.confirmed_paying_clients)?pipeline.confirmed_paying_clients:null;
  const pipelineDeals=Array.isArray(pipeline.opportunities)?pipeline.opportunities.length:null;
  const status=(clients===0)?'NOT_VALIDATED':clients===null?'UNKNOWN':'REPORTED_NOT_INDEPENDENTLY_VERIFIED';
  const evidencePath='quality/readiness-evidence.json';
  const integrityPass=protectedState.status==='PASS'&&contentState.status==='PASS';
  const v4=existsSync(resolve(root,evidencePath))?scoreV4(root,json(root,evidencePath),pipeline,integrityPass,scoreInfo.reported_document_score):{score:null,decision:'HOLD_SCALE',summary:`Preparación empresarial V4: NOT_VERIFIED (falta ${evidencePath}).`};
  return {
    schema_version:1,
    generated_at:new Date().toISOString(),
    source:'LOCAL_FILES_READ_ONLY',
    repository:{canonical:'alvaradom1304/Altiora',protected_capabilities:protectedState.status,protected_counts:protectedState.verified,skill_content_integrity:contentState.status,skill_files_checked:contentState.counts.checked,baseline:manifest.baseline_commit,errors:[...protectedState.errors,...contentState.errors]},
    skill_report:scoreInfo,
    ai_connectors:{configuration_files_present:existsSync(resolve(root,'.mcp.json')),status:'CONFIGURED_NOT_LIVE_TESTED',reason:'Los archivos, la CI y los simuladores no acreditan una sesión autenticada de Claude/Codex/Antigravity ni acceso a apps locales.'},
    commercial:{paying_clients_reported:clients,pipeline_opportunities_reported:pipelineDeals,status,pricing_target_usd:pipeline.target_project_price?.amount??null,pricing_validated:false,note:'El pipeline es un registro interno: ingresos, contratos y cobros deben verificarse con evidencia apropiada.'},
    scaling_gate:integrityPass&&clients>0?'MANUAL_REVIEW_REQUIRED':'HOLD',
    readiness_v4:v4,
    follow_up:[
      'Ejecutar npm run check y revisar resultados de CI en el mismo commit.',
      'Verificar conectores necesarios en sesiones nativas con permisos reales.',
      'Validar problema, decisor y presupuesto de compradores; registrar cobros aceptados.',
      'Entregar a Claude pruebas, límites y hallazgos de esta evaluación sin inflar porcentajes.'
    ]
  };
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  try{const report=assessAltiora(ROOT);process.stdout.write(process.argv.includes('--resumen')?report.readiness_v4.summary+'\n':JSON.stringify(report,null,2)+'\n');if(report.repository.protected_capabilities!=='PASS'||report.repository.skill_content_integrity!=='PASS')process.exitCode=1}
  catch(e){process.stderr.write('Readiness NO_VERIFICADO: '+e.message+'\n');process.exitCode=1}
}
