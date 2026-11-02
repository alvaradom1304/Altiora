# Enrutamiento y delegación de Altiora

Punto de entrada único para **Claude Code, Codex y Antigravity**, se lancen directamente o desde Orca. El usuario solo delega; la IA que recibe el encargo decide qué hacer con él aplicando este archivo. Objetivo: **el mismo resultado, con la misma calidad y el mismo formato, sea cual sea la IA**.

Lo que lo garantiza no es la IA, sino que todas compartan:
- las mismas fuentes: `skills/`, `team/` y este archivo;
- el mismo contrato de encargo y de entrega: [protocolo](../altiora-os/docs/protocol.md);
- la misma verificación: `npm run check`, [Definition of Done](../quality/definition-of-done.md) y revisión independiente.

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

## 4. Cómo delegar en cada herramienta

| Herramienta | Subagentes del rol | Fijar esfuerzo y modelo |
|---|---|---|
| Claude Code | `.claude/agents/<rol>.md` (herramienta Agent) | `claude --effort <nivel> --model <haiku\|sonnet\|opus>` |
| Codex | `.codex/agents/<rol>` | `codex -c model_reasoning_effort=<nivel>` (sin `max`; usar `xhigh`) |
| Antigravity | `.agents/agents/<rol>.md` | `agy --effort <nivel> --model <gemini-3.8-flash-<nivel>\|gemini-4-argon-high>` |
| Orca (otra IA) | — | `orca worktree create --name <parte> --agent <codex\|claude\|antigravity> --prompt "<encargo>"` |

Para un plan de reparto sin coste: `npm run orca:dispatch -- --router heuristic "mensaje"` (orientativo). Con modelo: `npm run orca:dispatch -- "mensaje"` (usa Claude Sonnet).

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
