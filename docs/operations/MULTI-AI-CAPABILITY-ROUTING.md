# PREAMBRA | Enrutamiento multi-IA y evaluación de capacidades
**Revisión de fuentes públicas:** 2026-11-17 (Costa Rica). **Estado:** política operativa propuesta, no prueba de acceso a modelos ni benchmark.

## Propósito y precedencia
PREAMBRA es la firma comercial; Altiora sigue siendo el núcleo técnico y el nombre del repositorio. Esta guía forma parte de las reglas compartidas de `AGENTS.md`, visibles también desde `CLAUDE.md` y `GEMINI.md`. Cada IA debe conocer las otras plataformas, Orca, sus modelos, esfuerzos, límites, cuota y rutas de traspaso, aunque se inicie fuera de Orca. ChatGPT usa [su entrada específica](CHATGPT-ENTRY.md). No se instalan conectores ni se heredan permisos por leer documentación.

## Catálogo oficial contrastado
| Plataforma | Opciones comprobadas en documentación | Esfuerzo | Uso propuesto (no superioridad medida) |
|---|---|---|---|
| ChatGPT / Codex | GPT-6 Luna, GPT-6.1 Terra/Sol, GPT-6.2 Sol/Astra en las superficies y planes indicados por OpenAI | Low, Medium, High, Extra High; Max/Ultra solo donde esté disponible; los nombres cambian por cliente y modelo | ChatGPT: discovery, análisis empresarial, integración de información y dirección; Codex: código, backend, seguridad, pruebas |
| Claude Code | Familias Haiku, Sonnet, Opus (documentación actual incluye Haiku 5.5, Sonnet 5.5, Opus 5.5; revisar disponibilidad del cliente) | low, medium, high, xhigh; max solo en modelos/CLI compatibles; `ultracode` es una configuración, **no** otro nivel | Copy, propuesta comercial, UX, arquitectura y ejecución multifase |
| Antigravity | Gemini 3.8 Flash; Gemini 4 Hydrogen/Argon/Carbon y Orchestrator (Argon/Carbon), sujetos al plan; también lista modelos de terceros | Low, Medium, High y Extra/xhigh solo donde corresponde; Orchestrator tiene configuración fija | Browser QA, escenas interactivas y trabajo visual; Orchestrator para planificación + ejecución, si está habilitado |
| Orca | Runtime externo para coordinar CLI, Runs, Tasks, Dispatches, workers y worktrees | No reemplaza esfuerzo del modelo subyacente | Puente opcional entre CLIs, no es otro LLM |

**Orca:** el repositorio de Altiora documentaba la release `v1.4.245`. La página oficial de `releases/latest` redirigía a **v1.4.261** el 2026-11-17. Es una **novedad pública**, NO actualización instalada ni validación de compatibilidad con el dispatcher existente. Nunca actualizar Orca, sus hooks o perfiles sin inspección, backup y prueba aislada.

**Fuentes oficiales, revisadas 2026-11-17:**
- OpenAI Codex/Work: https://developers.openai.com/codex/models (redirecciona a https://learn.chatgpt.com/docs/models).
- Claude Code: https://code.claude.com/docs/en/model-config
- Antigravity: https://antigravity.google/docs/models y https://antigravity.google/docs/cli/commands/effort
- Orca: https://github.com/stablyai/orca/releases/latest y https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx

No confundir modelo disponible en el mercado, incluido en el plan, visible en CLI, autenticado, ejecutado y validado; son seis estados diferentes. Detectar modelos realmente utilizables con `/model` en Claude/Codex, `agy models` y el selector de Antigravity, y las capacidades reales del entorno ChatGPT. Anotar fecha, comando y evidencia. No fijar identificadores inexistentes en el dispositivo.

## Enrutamiento: principio único para los cuatro puntos de entrada
1. Entender el encargo y su impacto en caja, ventas, calidad y riesgo. Si es pequeño, resolverlo desde la IA actual sin delegar.
2. Recuperar únicamente `AGENTS.md`, `team/ROUTING.md`, `continuity/checkpoint.json` y 1–3 skills pertinentes. No cargar todo el catálogo.
3. Consultar disponibilidad **real** del ejecutor y cuota restante: `UNKNOWN` no significa `READY`. Elegir una sola IA líder salvo partes realmente independientes.
4. Seleccionar modelo y esfuerzo **más bajos** que satisfagan criterios de aceptación: tareas mecánicas → low; trabajo acotado → medium; arquitectura/revisión compleja → high; decisiones críticas → xhigh cuando el modelo lo admita. `max` solo si está soportado y justificado. Los niveles NO son idénticos entre proveedores.
5. Si intervienen varios agentes, usar contrato `job_id / objective / owner / model / effort / input / owned_paths / dependencies / acceptance / evidence / risks`; un escritor por archivo. Dependencias primero, sin lanzar en paralelo trabajos encadenados.
6. Orca es transporte opcional: `npm run orca:dispatch -- --router heuristic --json "encargo"` para plan sin LLM ni envío. `--execute` o `--launch-workers` requieren `ALTIORA_DISPATCH_EXECUTE=1`, Orca local activo y permisos explícitos, y se deben probar individualmente. La propuesta de `worktree_strategy` NO crea un worktree.
7. Ejecutar validaciones, revisión independiente según riesgo, guardar handoff sin secretos y actualizar `continuity/checkpoint.json` en el PR de cierre. Un modelo que falló se reintenta con esfuerzo superior solo después de comprender por qué.

## Puntuación canónica y control de vigencia
El índice de **preparación operativa 0–10** vive en [preambra-model-matrix.json](preambra-model-matrix.json) y se explica en [PREAMBRA-MULTI-AI-ORCHESTRATION.md](PREAMBRA-MULTI-AI-ORCHESTRATION.md). No debe confundirse con la potencia del modelo ni con un benchmark. Las preferencias de asignación son hipótesis por especialidad, sujetas a coste medido, QA y disponibilidad real. Evitar crear un segundo índice incompatible.

Toda fuente tiene fecha. Antes de un cambio de modelos, herramientas, precio o acceso, comprobar la fuente oficial y el menú de la sesión. Para tareas críticas, revisar la vigencia de esta matriz antes de seleccionar modelo. `UNKNOWN` permanece sin puntuación de acceso hasta el preflight real.

## Primera tarea / prueba de aceptación
`PMO-ORCA-001`: planificar un encargo que combine estrategia/automatización, branding y revisión 3D, **sin lanzar** agentes. Criterios: JSON válido, 3 streams con propietarios y esfuerzos admitidos, un worktree propuesto por stream, guardia bloquea `--execute` sin autorización, y `npm run orca:test` + `npm run check` pasan en CI. Luego, en el PC autorizado: `orca --version`, `orca orchestration run-list --json`, `claude --version`, `codex --version`, `agy models` y `npm run orca:dispatch -- --router heuristic --json "..." `; registrar resultados reales. No declarar un worker funcionando por pasar los tests de planificación.
