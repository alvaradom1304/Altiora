# Registro de mejora continua de skills

Un bloque por ciclo, el más reciente arriba. Proceso: [mejora continua de skills](../docs/workflows/skill-improvement.md).

## Ciclo 4 — 2026-11-09

**Planificar.** Ciclo semanal automático. Todas las skills propias ya están en 100; las únicas sin casos de evaluación eran 2 de terceros (`n8n-expressions-official`, `n8n-error-handling-official`). Objetivo y métrica: skills sin casos 2 → 0, media 98.3 → ≥ 98.4, un caso ejecutado como mínimo por skill modificada. Solo se eligieron 2 de las 5 posibles: el resto del backlog son reglas de `SKILL.md` de terceros, que no se editan aquí.

**Hacer.** `evals/evals.json` propio (3 casos por skill: normal, borde o datos insuficientes, rechazo o redirección) en inglés, como las skills, y nota en sus `SOURCE.md`. Sus `SKILL.md` no se tocaron, así que la versión no cambia.

**Verificar.** `npm run check`: OK, sin regresiones. Media **98.3 → 98.4**; terceros 93.9 → 94.2; skills con menos de 3 casos: 0. Casos ejecutados: 4, todos PASA ([eval-runs/2026-11-09](eval-runs/2026-11-09.md)); autoevaluación. NO EJECUTADOS: 2 casos nuevos y los pendientes de ciclos anteriores.

**Actuar.** Objetivo cumplido; línea base actualizada con `npm run skills:baseline`. Ningún error repetido nuevo en skills propias.

**Backlog del ciclo 5.**
- Terceros con fallos de forma en `SKILL.md` (un H1, versión, entregable, descripción sin disparador; p. ej. `gcp-pipeline-orchestration`, `finishing-a-development-branch`, `ai-seo`): actualizar desde origen o proponer el cambio al proyecto original.
- Revisión humana de al menos un caso por skill de los ciclos 1–4 y ejecución de los pendientes.
- Decidir la regla `evals-executed` del auditor (propuesta del ciclo 2, aún sin añadir).

## Ciclo 3 — 2026-11-01/02

**Planificar.** Tras revertir un intento que llevó la media a un 100 artificial (casos de plantilla idénticos, secciones «Entregable» genéricas y prefijos «Usar para:» que rompieron el enrutamiento de «brand»), el dueño pidió llegar al 100 con mejoras reales. Primero se endureció la auditoría (#50): un caso o párrafo repetido en 5 skills o más no puntúa, y el informe separa propias y terceros. Objetivo: todas las skills propias a 100; las de terceros mejoran solo con casos propios, sin editar su `SKILL.md`.

**Hacer.**
- 43 skills propias: descripciones con cuándo usarla y cuándo no (sin añadir términos que compitan con las skills de marca), versión declarada, sección Entregable concreta y 3 casos propios (normal, borde o datos insuficientes, rechazo). Las 5 de menor puntuación (`altiora-session-handoff`, `aem-stage-03/04/06/07`) incluyen además reglas de decisión nuevas; el resto lo hicieron 4 agentes con lotes disjuntos y revisión del coordinador.
- 68 skills de terceros: solo `evals/evals.json` propio, en el idioma de la skill. Sus `SKILL.md`, `SOURCE.md` y `references/` no se tocaron.
- Correcciones de contenido detectadas en la revisión: `elite-web-experience-os` ya no promete «60–120 FPS estables» (objetivo medido, no promesa); `altiora-session-handoff` registra commits locales y stashes en `pending` (causa de trabajo perdido en el traspaso del 2026-11-01) y alinea la regla de varias tareas con el schema de una sola tarea; `aem-stage-07-growth` marca como proyección un LTV con ventana distinta del CAC; `aem-stage-06-automation` cubre el umbral exacto de 3 veces por semana y no repite preguntas ya respondidas.
- `vercel-react-best-practices`: sin registro de procedencia; se trata como resumen local y se anota en `metadata.provenance`.

**Verificar.**
- Auditoría endurecida: propias **260/260 en 100**; terceros media 83,2 → 94,2; total 93,5 → 98,5. Sin regresiones.
- Enrutamiento del Bibliotecario: 17/17 casos PASA, incluido «brand».
- Casos ejecutados por evaluadores independientes (no los autores): ciclo 3 inicial, 4 PASA y 1 NO EJECUTABLE en solo lectura (se corrigieron los errores que señaló); muestra amplia de 12 skills: ver [eval-runs/2026-11-02](eval-runs/2026-11-02.md).
- NO EJECUTADOS: el resto de los casos nuevos.

**Actuar.** Línea base actualizada con `npm run skills:baseline`.
Pendiente para terceros: varias fallan por reglas de su `SKILL.md` (un H1, versión, entregable). Se mejoran actualizando desde su origen o proponiendo el cambio al proyecto original, no editándolas aquí. Referencias de origen a skills que no existen en este repo (`google-cloud-storage-diagnostic`, `bigquery`): documentarlas o importarlas en un ciclo propio.

## Ciclo 2 — 2026-10-19

**Planificar.** Ciclo semanal automático, máximo 5 skills. Primero el backlog: ejecutar casos pendientes del ciclo 1. Después, las de menor puntuación del informe: `webapp-testing` (70), `aem-core-philosophy`, `aem-stage-01-discovery`, `aem-stage-02-research` y `altiora-repository-research` (75).
Objetivo y métrica: las 4 propias a 100 y `webapp-testing` a 85 sin tocar su SKILL.md (es de terceros); media 97.4 → ≥ 97.6; skills sin casos 29 → 24; al menos un caso ejecutado por skill modificada y por cada skill del ciclo 1.

**Hacer.**
- `aem-core-philosophy` 1.1.0: descripción con cuándo usarla y cuándo no; quitados los encabezados duplicados y vacíos («1.» dos veces, «2.» dos veces); tabla fase → skill; pasos para ubicar la fase y contrastar los 7 principios (Cumple / No cumple / Sin datos); reglas de decisión; entregable verificable.
- `aem-stage-01-discovery` 1.1.0: descripción con cuándo usarla y cuándo no; reglas para información incompleta (`PENDIENTE`), cifras solo del cliente o calculadas, criterios de éxito medibles; verificación del entregable. Se conserva la plantilla original.
- `aem-stage-02-research` 1.1.0: descripción con cuándo usarla y cuándo no; reglas de evidencia (fuente con URL y fecha o marca `Hipótesis`, competidores confirmados, jobs-to-be-done); verificación del entregable.
- `altiora-repository-research` 1.1.0: sección Entregable con tabla por candidato y regla «sin licencia clara no se adopta»; cuándo no usarla.
- `webapp-testing`: solo casos propios en `evals/evals.json` (en inglés, como la skill) y nota en `SOURCE.md`.
- 3 casos de evaluación por skill (15 en total) en `evals/evals.json`. Bridges de `.claude/skills` e `INDEX.md` regenerados con `npm run agents:build`.

**Verificar.**
- `npm run check`: OK, sin regresiones. Media **97.8/100** (antes 97.4); skills sin casos 29 → 24; 226 skills en 90–100 y ninguna por debajo de 75.
- Casos ejecutados: 12, todos PASA (5 de este ciclo y 7 del ciclo 1, uno por skill). Detalle y evidencia en [eval-runs/2026-10-19](eval-runs/2026-10-19.md). Los ejecutó el mismo agente que editó las skills: sesgo de autoevaluación, pendiente de revisión humana.
- NO EJECUTADOS: 14 casos del ciclo 1 y 10 de este ciclo.
- Diff revisado: el contenido propio de las 4 skills se conserva (principios, plantilla de Discovery, instrucciones de Research y texto de selección de fuentes); solo se añaden reglas, verificación e historial.

**Actuar.** Objetivo cumplido; línea base actualizada con `npm run skills:baseline`.
Error repetido detectado: las 5 `aem-stage-*` restantes (03, 04, 05, 06, 07) y otras descripciones del tipo «Ejecuta la Fase 0X de AEM…» no dicen cuándo usarlas ni cuándo no; la regla `description-trigger` ya lo mide. Propuesta de regla nueva (no añadida): `evals-executed`, que dé puntos solo si existe un registro en `quality/eval-runs/` con resultado para la skill, para que la rúbrica premie casos ejecutados y no solo escritos, como pide la revisión trimestral.

**Backlog del ciclo 3.**
- `aem-stage-03-strategy`, `aem-stage-04-brand`, `aem-stage-06-automation`, `aem-stage-07-growth` (75) y `aem-stage-05-digital` (80): mismo patrón que las fases 01–02.
- Casos propios para externas sin `evals/`: `skill-creator`, `vercel-react-best-practices`, `vercel-composition-patterns`, `writing-plans`, `systematic-debugging`, `verification-before-completion`, `web-design-guidelines`.
- Ejecutar los 24 casos pendientes (14 del ciclo 1, 10 del ciclo 2) y que una persona revise al menos uno por skill.
- `webapp-testing` caso 3: la skill no cubre producción ni credenciales; proponer la nota al proyecto original o documentarla en `SOURCE.md`.
- Decidir si se añade la regla `evals-executed` al auditor.

## Incorporación de skills externas — 2026-10-18

- 14 skills de terceros con licencia y procedencia: webapp-testing, skill-creator, web-design-guidelines, vercel-composition-patterns, events, referrals, offers, emails, schema, ab-testing, analytics, writing-plans, systematic-debugging, verification-before-completion. Atribución añadida a 4 importadas antes (cro, free-tools, lead-magnets, marketing-psychology).
- Línea base recalculada con 251 skills; la media baja porque varias externas no declaran versión ni entregable con el formato de la rúbrica. No es una regresión de las existentes.
- Backlog: casos de evaluación propios para las externas sin `evals/` (webapp-testing, skill-creator, web-design-guidelines, vercel-composition-patterns, writing-plans, systematic-debugging, verification-before-completion) y adaptar ejemplos de marketing a La Central del Queso en `evals/`, sin tocar su SKILL.md.

## Ciclo 1 — 2026-10-18

**Planificar.** Primera auditoría con `scripts/audit-skills.mjs`: media **78.1/100**, solo 84 de 237 skills en 100. Causa principal: un envoltorio «Executive Protocol» insertado durante la integración del catálogo, duplicado en 132 skills (secciones y párrafos repetidos, encabezados vacíos) y que en 125 skills con contrato contradecía su protocolo: pedía hablar «como consultor de Bain/McKinsey», hacer preguntas antes de actuar y entregar Markdown libre, frente al contrato que exige `output-schema.json`, no pedir permiso para análisis autorizado y estado `SUCCESS/FAILED/BLOCKED/NEEDS_REVIEW`.
Objetivo: eliminar duplicados y contradicciones sin perder contenido propio, y rehacer las 7 skills de menor puntuación.

**Hacer.**
- Migración revisada en 136 `SKILL.md`: en las 125 con contrato se quitan el envoltorio y el SOP genérico (se conserva la Regla de Oro una vez); en las 11 sin contrato se deja una sola copia de cabecera y SOP.
- Reescritas con disparador, procedimiento concreto, entregable y 3 casos de evaluación (`evals/evals.json`): `spin-selling`, `consumer-psychology`, `cybersecurity-owasp`, `financial-forecasting`, `logistics-supply-chain`, `premium-branding` (de 50 a 100) y `modular-docs-architect` (de 70 a 100; además sustituye el consejo de enlazar con rutas absolutas `file:///` por rutas relativas).
- Nuevo auditor con gate de no-regresión dentro de `npm run check`.

**Verificar.**
- `npm run check`: OK, sin regresiones. Media **98.0/100**; 212 skills en 100, ninguna por debajo de 75.
- Revisión del diff de la migración: solo se eliminan líneas del envoltorio repetido.
- Casos de evaluación de las 7 skills reescritas: **NO EJECUTADOS** todavía. Primer punto del próximo ciclo.

**Actuar.** Línea base actualizada. Lección convertida en regla: `no-legacy-conflict` y `no-duplicate-paragraphs` impiden que vuelva a entrar el envoltorio.

**Backlog del ciclo 2.**
- Ejecutar los 21 casos de evaluación de este ciclo y anotar PASA/FALLA.
- 21 skills sin casos de evaluación (las 7 `aem-stage-*`, `altiora-*`, `frontend-design`, `vercel-react-best-practices`, orquestadores).
- 12 descripciones sin indicar cuándo usarlas y 16 skills sin versión.
- Las skills con contrato listan fuentes poco pertinentes a su dominio (p. ej. `accessibility` cita GSAP y Next.js). Candidata a nueva regla del auditor.
- Las descripciones generadas («X: dominio. Usar para producir…») se parecen entre sí; revisar si disparan bien entre skills vecinas.
