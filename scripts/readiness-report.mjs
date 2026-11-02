// Informe conservador: distingue existencia en Git de disponibilidad en sesión
// y de resultados comerciales. Solo lectura. No escanea secretos ni inicia conectores.
import {readFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {verifyCapabilityBaseline} from './verify-capability-baseline.mjs';

const ROOT=fileURLToPath(new URL('../',import.meta.url));
const load=(root,p)=>readFileSync(resolve(root,p),'utf8');
const json=(root,p)=>JSON.parse(load(root,p));

export function assessAltiora(root){
  const manifest=json(root,'references/capability-protection-baseline-2026.json');
  const protectedState=verifyCapabilityBaseline(root,manifest);
  const pipeline=json(root,'docs/altiora-business/pipeline.json');
  const score=load(root,'quality/skills-report.md');
  const match=score.match(/(\d+) skills; media \*\*([\d.,]+)\/100\*\*/i);
  const scoreInfo=match?{reported_skills:Number(match[1]),reported_document_score:Number(match[2].replace(',','.')),type:'DOCUMENT_STRUCTURE_NOT_BUSINESS_READINESS'}:{reported_skills:null,reported_document_score:null,type:'NOT_PARSED'};
  const clients=Number.isInteger(pipeline.confirmed_paying_clients)?pipeline.confirmed_paying_clients:null;
  const pipelineDeals=Array.isArray(pipeline.opportunities)?pipeline.opportunities.length:null;
  const status=(clients===0)?'NOT_VALIDATED':clients===null?'UNKNOWN':'REPORTED_NOT_INDEPENDENTLY_VERIFIED';
  return {
    schema_version:1,
    generated_at:new Date().toISOString(),
    source:'LOCAL_FILES_READ_ONLY',
    repository:{canonical:'alvaradom1304/Altiora',protected_capabilities:protectedState.status,protected_counts:protectedState.verified,baseline:manifest.baseline_commit,errors:protectedState.errors},
    skill_report:scoreInfo,
    ai_connectors:{configuration_files_present:existsSync(resolve(root,'.mcp.json')),status:'CONFIGURED_NOT_LIVE_TESTED',reason:'Los archivos, la CI y los simuladores no acreditan una sesión autenticada de Claude/Codex/Antigravity ni acceso a apps locales.'},
    commercial:{paying_clients_reported:clients,pipeline_opportunities_reported:pipelineDeals,status,pricing_target_usd:pipeline.target_project_price?.amount??null,pricing_validated:false,note:'El pipeline es un registro interno: ingresos, contratos y cobros deben verificarse con evidencia apropiada.'},
    scaling_gate:protectedState.status==='PASS'&&clients>0?'MANUAL_REVIEW_REQUIRED':'HOLD',
    follow_up:[
      'Ejecutar npm run check y revisar resultados de CI en el mismo commit.',
      'Verificar conectores necesarios en sesiones nativas con permisos reales.',
      'Validar problema, decisor y presupuesto de compradores; registrar cobros aceptados.',
      'Entregar a Claude pruebas, límites y hallazgos de esta evaluación sin inflar porcentajes.'
    ]
  };
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  try{const report=assessAltiora(ROOT);process.stdout.write(JSON.stringify(report,null,2)+'\n');if(report.repository.protected_capabilities!=='PASS')process.exitCode=1}
  catch(e){process.stderr.write('Readiness NO_VERIFICADO: '+e.message+'\n');process.exitCode=1}
}
