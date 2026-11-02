# Briefing de reincorporación para Codex (ChatGPT)

**Corte:** 2026-11-01. **Uso:** leer al volver tras renovar la cuota, antes de cualquier tarea de Altiora.
**Fuente de verdad:** el repositorio en `main`, no este resumen. Si algo aquí contradice un archivo, manda el archivo.

## 1. Principios de trabajo

- **Estrategia antes que diseño; evidencia antes que opinión.**
- Respuestas en español, directas, sin cortesías vacías. Separar siempre lo verificado de lo supuesto (`VERIFICADO`, `SUPUESTO`, `NOT_VERIFIED`).
- No inventar métricas, costes de terceros ni capacidades. Si no está ejecutado o medido en el repo, se marca.
- Alcance: el encargo comercial de referencia es un proyecto de US$10.000 con techo de 75 horas (margen objetivo 25 %). Defender el alcance antes que ampliarlo.

## 2. Grafo de conocimiento (Graphify)

- Skill válida: `skills/graphify/SKILL.md` del repo (en `main` desde el PR #45). **No instalar** `graphify install` ni ninguna skill con ese nombre en inglés: es la versión original, calificada DO_NOT_INSTALL, y se retiró de Claude, Gemini y Codex.
- Grafo vigente, fuera del repo: `C:/Users/Usuario/.altiora-tools/graphs/altiora/graphify-out/` — 21.353 nodos, 24.193 aristas, 782 comunidades sin nombrar. Regenerado el 02/11/2026 desde el commit `83853a4` (solo código, sin modelo); comparar con `GRAPH_REPORT.md` antes de fiarse.
- **Siempre** con `GRAPHIFY_BACKEND=none`. Sin esa variable, Graphify puede llamar en silencio a `claude -p` y consumir la suscripción (ya ocurrió: ~1,1 M de tokens).
- Usar `query`, `path` y `explain` antes de releer código; confirmar siempre en el archivo real.
- No hay servidor MCP de Graphify: se retiró de `.mcp.json` el 02/11/2026 porque fallaba al arrancar (faltaba el módulo `mcp`). Usar el CLI, igual en Claude, Codex y Antigravity.

## 3. Estado verificado al 2026-11-01

- **`main`** contiene la unificación (PR #43), Graphify (PR #45) y la documentación de ROUTING (PR #46). El punto de entrada para decidir a quién delegar es `team/ROUTING.md`.
- **Cambios sin integrar:** en la copia canónica (`altiora-unificado`) hay trabajo sin commitear de Antigravity y Claude (por ejemplo `.altiora/*.json`, `.mcp.json`, `docs/altiora-business/CLAUDE-CALCULATOR-REVIEW.md`). Antes de tocarlo, leerlo y preguntar al dueño.
- **Revisión de la calculadora:** `docs/altiora-business/CLAUDE-CALCULATOR-REVIEW.md` existe; sus conclusiones deben leerse en el archivo, no en este resumen.
- **Pendiente de decisión del dueño:** cerrar o fusionar los PRs abiertos (#1, #6, #8, #9, #11–#18). Ninguno se cierra ni fusiona sin orden explícita.
- **Tilicheros:** espera datos del negocio (SKU, precio, stock, responsable de WhatsApp). No inventar cifras.
- **Google Cloud:** el estado de la cuenta no está verificado en el repo (`NOT_VERIFIED`). No afirmar que esté cerrada ni que la réplica del Data Agent Kit funcione sin evidencia.

## 4. Próxima tarea sugerida

Si el dueño pide trabajo de propuesta comercial, el dominio de Codex es `strategy-finance-backend`: leer `docs/altiora-business/PROPUESTA-MAESTRA-ALTIORA.md` y `docs/altiora-business/OFERTA.md` y redactar la propuesta B2B con exclusiones explícitas, respetando el techo de 75 horas. Entregar con el formato de `team/ROUTING.md` §5.

## 5. Protocolo al recibir «sigue» o «continúa»

1. Leer `continuity/checkpoint.json`, `AGENTS.md` y `team/ROUTING.md`.
2. Actualizar la rama con `main` antes de trabajar.
3. Elegir un paso desbloqueado; no preguntar por lo que ya está documentado.
4. Entregar con resultado, evidencia, verificado/supuesto, pendiente y siguiente paso.
