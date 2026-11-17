# Enrutamiento y delegación de Altiora

Punto de entrada único para **Claude Code, Codex y Antigravity**, se lancen directamente o desde Orca. El usuario solo delega; la IA que recibe el encargo decide qué hacer con él aplicando este archivo. Objetivo: **el mismo resultado, con la misma calidad y el mismo formato, sea cual sea la IA**.

Lo que lo garantiza no es la IA, sino que todas compartan:
- las mismas fuentes: `skills/`, `team/` y este archivo;
- el mismo contrato de encargo y de entrega: [protocolo](../altiora-os/docs/protocol.md);
- la misma verificación: `npm run check`, [Definition of Done](../quality/definition-of-done.md) y revisión independiente.


## 0. Gobierno operativo de Altiora OS (2026-11-03)

La **dirección ejecutiva humana** aprueba objetivos, alcance, contratos, presupuesto, publicación, contacto con terceros y cambios de riesgo. **Claude Code actúa como director operativo de ejecución** para proyectos multifase: recibe un brief aprobado, organiza hitos, consulta el router y coordina handoffs cuando existan sesiones, permisos y conexiones reales. **ChatGPT dirige discovery, consultoría y estrategia**, sin reclamar acceso local por defecto. **Codex** es especialista en ingeniería y QA técnico; **Antigravity** en producción visual interactiva. Las especialidades y respaldos de la matriz de dominios de la sección 3 se mantienen, por lo que el nombramiento de Claude **no reemplaza automáticamente las preferencias por dominio** ni implica lanzar agentes.

Cada delegación debe documentar `job_id`, responsable, inputs, propiedad de archivos, skills, criterios de aceptación, riesgos y evidencia. No se permite que dos agentes editen simultáneamente el mismo archivo. Trabajos de cliente requieren QA independiente y revisión humana donde aplique. La disponibilidad de MCP, Blender, After Effects y coordinación entre IAs **solo se declara verificada** tras pruebas en sesiones reales. Ver [gobierno y gates](../docs/operations/CLAUDE-OPERATIONAL-DIRECTOR-PROPOSAL-2026-11-03.md) y [validación #65](https://github.com/alvaradom1304/Altiora/issues/65).

> **Catálogo actualizado de modelos:** [MULTI-AI-CAPABILITY-ROUTING.md](../docs/operations/MULTI-AI-CAPABILITY-ROUTING.md) (revisión 2026-11-17). Conoce las opciones de ChatGPT/Codex, Claude Code, Antigravity y Orca antes de elegir; el ajuste de esfuerzo, modelos admitidos y cuotas se verifica en cada runtime. Los nombres concretos de modelos de la tabla histórica inferior son ejemplos de 2026-11-01, no garantías de disponibilidad actual.

## 1. Al recibir un encargo (siempre, cualquier IA)

1. **Entender:** objetivo, entregable, criterio de aceptación, proyecto y riesgo. Si falta algo que cambia el resultado, preguntarlo **una vez** y no avanzar en lo que dependa de eso.
2. **Clasificar:** dominios que toca (sección 3), tamaño y riesgo.
3. **Decidir** con el árbol de la sección 2.
4. **Ejecutar** con el rol, las skills y el esfuerzo de la sección 3. Para orientarse en el código (dónde se usa algo, qué depende de qué), consultar primero el grafo con la skill [graphify](../skills/graphify/SKILL.md) y confirmar en el archivo real; siempre con `GRAPHIFY_BACKEND=none`. Conectores pesados (Vercel, Ahrefs, Notion, Canva, Figma, Gmail, HubSpot, Slack, Supermetrics) apagados por defecto: activar solo el que la tarea pida y apagarlo al terminar ([conectores y ahorro](../docs/operations/CONECTORES-Y-AHORRO.md)). Una sesión por tarea. Antes de una tarea grande, de lanzar subagentes u otra IA, o cuando la sesión se alarga, consultar al rol [ai-economist](roles/ai-economist.md) (conectores, IA, modelo, esfuerzo y cierre de sesión sin bajar la calidad).
5. **Entregar** con el formato de la sección 5. Nada se da por terminado sin evidencia.

## 2. Árbol de decisión

| Situación | Decisión |
|---|---|
| Cambio pequeño o pregunta, un solo dominio | **Hacerlo yo**, sin delegar |
| Un solo dominio, sustancial, y soy la IA preferida de ese dominio | **Hacerlo yo** con el subagente del rol (sección 4) |
| Un solo dominio, sustancial, y **no** soy la IA preferida | **Avisar y proponer** pasarlo a la IA preferida con el comando de Orca (sección 4). Si el usuario dice que siga yo, sigo con el mismo rol, skills y contrato |
| Varias partes independientes, archivos distintos, más de unos 45 minutos | **Proponer reparto en Orca** con `altiora-os-delegation`: partes, IA, esfuerzo y comando por parte |
| Partes encadenadas o que editan los mismos archivos | **Una sola IA**, por pasos y un rol a la vez |
| Decisiones de precio, legales, financieras o de producción | **Una sola IA responsable** y revisión humana; nunca repartir |
| La IA preferida está sin créditos (`.altiora/orchestration.json` → `ai_status`) | Siguiente IA de la cadena de respaldo (sección 3) |

Lanzar agentes en Orca, crear worktrees, enviar mensajes, publicar o gastar requiere autorización expresa del usuario para esa acción. Proponer el comando no es ejecutarlo.

## 3. Matriz de dominios

Coincide con `DOMAIN_RULES` de `scripts/orca-dispatch.py`; el test `scripts/routing.test.mjs` comprueba que no se desalineen.

| Dominio | IA preferida | Respaldo | Rol (subagente) | Skills de entrada |
|---|---|---|---|---|
| `strategy-finance-backend`: estrategia, finanzas, precios, outbound B2B, backend, automatización | codex | claude → antigravity | business-strategist, commerce-growth-director | aem-company-builder, high-ticket-offer, pricing, unit-economics, cold-outbound-system, n8n-webhook-architect |
| `brand-copy-frontend`: marca, copy, propuestas, ventas, UI/Next.js | claude | codex → antigravity | brand-strategist, content-designer, commerce-growth-director, ui-designer | premium-branding, copywriting, sales-proposal, draft-outreach, conversion-ux, nextjs-architecture |
| `immersive-3d-qa`: 3D/WebGL, GSAP/scroll, auditoría visual | antigravity | claude → codex | creative-director → web-engineer → qa-reviewer | immersive-interaction-lab, threejs-experience, react-three-fiber, gsap-animation, web-quality-assurance |
| `cloud-data-engineering`: Google Cloud, BigQuery, pipelines | antigravity | claude → codex | web-engineer | gcp-data-pipelines, dbt-bigquery |

Otros encargos se enrutan por intención con los mismos roles: anuncios y video → creative-ads-director ([WORK_ROUTER](../creative-ads-os/WORK_ROUTER.md)); audio → audio-specialist; medición → growth-analyst; coordinación de varios roles → experience-director. Las skills fuera del listado automático se usan leyendo `skills/<nombre>/SKILL.md`.

**Esfuerzo de razonamiento:** el más bajo que cumpla el criterio. `low` para tareas mecánicas, `medium` por defecto, `high` para arquitectura, auditoría, investigación o diseño de escenas, y `xhigh`/`max` solo con riesgo económico, legal o de seguridad, o si el usuario pide profundidad. El tema no sube el nivel; lo sube lo que se pide. Modelo grande solo en `high` o más. Si la tarea resulta no ser la adecuada para la IA asignada, detenerse y decirlo en vez de seguir gastando.

## 3.1. PREAMBRA OS V2 — Modos adaptativos integrados (solo planificación segura)

El despachador existente `scripts/orca-dispatch.py` incluye una política determinista en `scripts/preambra_v2_routing.py`. No es un nuevo orquestador. Responde con `policy_v2` y contratos `handoffs` además del JSON histórico:

- **A/directo:** tarea pequeña; resolver desde la IA actual, sin Orca.
- **B/constructor + revisor:** tarea sustancial, de varios dominios o de riesgo; revisor independiente propuesto.
- **C/paralelo selectivo:** *solo* cuando el encargo declara independencia, no hay dependencias y los caminos de escritura no se solapan; los worktrees aún requieren creación real en Orca.
- **D/proyecto integral:** fases empresariales y aprobaciones, no workers paralelos lanzados automáticamente.

`--router heuristic` es el modo por defecto y no invoca ningún LLM. `--router model` es opcional y puede consumir cuota. `--entrypoint` describe el origen pero NO demuestra autenticación. Los nombres de modelos son sugerencias: `model_observed=UNKNOWN` hasta preflight del ejecutor.

**Seguridad:** `--execute` y `--launch-workers` conservan el gate `ALTIORA_DISPATCH_EXECUTE=1`. Además, V2 rechaza `--launch-workers` si el plan implica worktrees todavía no creados o un proyecto de varias fases. No usar el bit del plan `new-child` como prueba de un worktree existente. `npm run routing:v2:test` y `npm run check` son los gates de tests. Guía operativa: [PREAMBRA-V2-ROUTER-RUNBOOK](../docs/operations/PREAMBRA-V2-ROUTER-RUNBOOK.md).

## 4. Cómo delegar en cada herramienta

| Herramienta | Subagentes del rol | Fijar esfuerzo y modelo |
|---|---|---|
| Claude Code | `.claude/agents/<rol>.md` (herramienta Agent) | `claude --effort <nivel> --model <haiku\|sonnet\|opus>` |
| Codex | `.codex/agents/<rol>` | `codex -c model_reasoning_effort=<nivel>` (sin `max`; usar `xhigh`) |
| Antigravity | `.agents/agents/<rol>.md` | `agy --effort <nivel> --model <gemini-3.8-flash-<nivel>\|gemini-4-argon-high>` |
| Orca (otra IA) | — | `orca worktree create --name <parte> --agent <codex\|claude\|antigravity> --prompt "<encargo>"` |

Para un plan de reparto sin coste: `npm run orca:dispatch -- --json "mensaje"` (**heurístico por defecto**). Si se desea pagar una decisión LLM, optar explícitamente por `--router model` y verificar Claude CLI, modelo y cuotas. El plan no ejecuta agentes.

**Encargo al delegar** (plantilla única): objetivo verificable · entradas concretas · archivos que puede tocar (un escritor por archivo) · dependencias · rol y skills · esfuerzo · criterio de aceptación · qué no hacer.

## 5. Formato de entrega (idéntico en todas las IAs)

1. **Resultado:** qué está hecho, en una o dos frases.
2. **Evidencia:** archivos, commits, comandos ejecutados y su resultado real.
3. **Verificado / supuesto:** separar lo comprobado de lo inferido; lo no ejecutado se marca `NOT_RUN`.
4. **Pendiente y bloqueos:** qué falta y quién debe actuar.
5. **Siguiente paso:** uno, concreto.

Para entregas entre IAs, usar el JSON del [protocolo](../altiora-os/docs/protocol.md) (`status`, `artifacts`, `evidence`, `checks`, `limitations`, `next_actions`).

**Puerta de calidad antes de decir «terminado»:**
- `npm run check` pasa si se tocaron skills, agentes, documentos o scripts.
- Lo que aplique de la [Definition of Done](../quality/definition-of-done.md) para webs y entregas a clientes.
- Revisión independiente con `qa-reviewer` (o `altiora-quality-review`) para todo lo que vea un cliente; si solo hay una IA, declarar que la revisión fue secuencial.
- Sin hechos comerciales inventados, sin secretos y sin afirmar conexiones o ejecuciones no comprobadas.
- Apuntar a la mejor calidad posible dentro del alcance acordado: no ampliar el alcance ni entrar en bucles de mejora sin fin.
