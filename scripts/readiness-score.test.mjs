import test from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {assessAltiora,scoreV4,demandCap,V4_AXES} from './readiness-score.mjs';

const root=fileURLToPath(new URL('../',import.meta.url));
const axis=(level,...kinds)=>({level,evidence:kinds.map((kind,i)=>({kind,source:'cmd:prueba',date:`2026-11-0${i+1}`}))});
const allAxes=(level,...kinds)=>({axes:Object.fromEntries(Object.keys(V4_AXES).map(id=>[id,axis(level,...kinds)]))});
const paid={confirmed_paying_clients:2,opportunities:[],research_status:{}};

test('la nota V4 del repo es reproducible, suma sus ejes y se declara aparte de la nota de skills',()=>{
  const v=assessAltiora(root).readiness_v4;
  assert.equal(Object.values(V4_AXES).reduce((a,b)=>a+b,0),100);
  assert.equal(v.score,Math.round(Object.values(v.axes).reduce((a,x)=>a+x.points,0)*10)/10);
  for(const x of Object.values(v.axes))assert.ok(x.level<=x.supported&&x.level<=x.cap);
  assert.match(v.summary,/Preparación empresarial V4: [\d.]+\/100/);
  assert.match(v.summary,/no la madurez de la empresa/);
  if(v.p0_open.length)assert.equal(v.decision,'HOLD_SCALE');
});
test('un nivel declarado sin evidencia suficiente se rebaja',()=>{
  const v=scoreV4(root,allAxes(5,'design'),paid);
  for(const x of Object.values(v.axes))assert.equal(x.level,1);
  assert.equal(v.score,20);
});
test('un 5 exige dos evidencias reales en fechas distintas',()=>{
  assert.equal(scoreV4(root,allAxes(5,'real'),paid).axes.economy_capacity.level,4);
  assert.equal(scoreV4(root,allAxes(5,'real','real'),paid).score,100);
});
test('fuentes inexistentes o tipos desconocidos no cuentan',()=>{
  const ev={axes:{economy_capacity:{level:3,evidence:[{kind:'test',source:'no/existe.md'},{kind:'opinion',source:'cmd:x'}]}}};
  const v=scoreV4(root,ev,paid);
  assert.equal(v.axes.economy_capacity.level,0);
  assert.equal(v.axes.economy_capacity.status,'NOT_VERIFIED');
  assert.ok(v.warnings.length>=1);
});
test('la demanda queda topada por los hechos de pipeline.json',()=>{
  assert.equal(demandCap({confirmed_paying_clients:0,opportunities:[],outreach_sent:false,research_status:{contacts_sent:0}}),1);
  assert.equal(demandCap({confirmed_paying_clients:0,opportunities:[],outreach_sent:true,research_status:{}}),2);
  assert.equal(demandCap({confirmed_paying_clients:0,opportunities:[],research_status:{interviews_completed:1}}),3);
  assert.equal(demandCap({confirmed_paying_clients:1}),4);
  assert.equal(demandCap({confirmed_paying_clients:2}),5);
});
test('un P0 abierto limita la entrega a 2 y bloquea la decisión de piloto',()=>{
  const v=scoreV4(root,{...allAxes(4,'real'),p0_open:[{id:'P0-X'}]},paid);
  assert.equal(v.axes.deliverable_quality.level,2);
  assert.equal(v.decision,'HOLD_SCALE');
  assert.equal(scoreV4(root,allAxes(4,'real'),paid).decision,'READY_FOR_REPEATABLE_DELIVERY');
});
