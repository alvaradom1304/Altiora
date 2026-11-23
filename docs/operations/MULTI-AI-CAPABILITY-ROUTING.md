# PREAMBRA | Enrutamiento multi-IA y evaluación de capacidades
**Revisión de fuentes públicas:** 2026-11-23 (Costa Rica); línea base: 2026-11-17. **Estado:** política operativa propuesta, no prueba de acceso a modelos ni benchmark.

## Propósito y precedencia
PREAMBRA es la firma comercial; Altiora sigue siendo el núcleo técnico y el nombre del repositorio. Esta guía forma parte de las reglas compartidas de `AGENTS.md`, visibles también desde `CLAUDE.md` y `GEMINI.md`. Cada IA debe conocer las otras plataformas, Orca, sus modelos, esfuerzos, límites, cuota y rutas de traspaso, aunque se inicie fuera de Orca. ChatGPT usa [su entrada específica](CHATGPT-ENTRY.md). No se instalan conectores ni se heredan permisos por leer documentación.

## Catálogo oficial contrastado
| Plataforma | Opciones comprobadas en documentación | Esfuerzo | Uso propuesto (no superioridad medida) |
|---|---|---|---|
| ChatGPT / Codex | GPT-6 Luna, GPT-6.1 Terra/Sol, GPT-6.2 Sol/Astra en las superficies y planes indicados por OpenAI | Low, Medium, High, Extra High; Max/Ultra solo donde esté disponible; los nombres cambian por cliente y modelo | ChatGPT: discovery, análisis empresarial, integración de información y dirección; Codex: código, backend, seguridad, pruebas |
| Claude Code | Haiku/Sonnet/Opus 5.5 y Fable 5.2 según proveedor; alias `opusplan` usa Opus al planear y Sonnet al implementar (**no** otro modelo) | low, medium, high, xhigh, max sujetos a modelo y CLI; `ultracode` no es esfuerzo | Copy, estrategia, arquitectura y ejecución; ensayar `opusplan` tras comprobar CLI y costos |
| Antigravity | Gemini 3.8 Flash y Gemini 4 Hydrogen/Argon/Carbon/**Neon**; Orchestrator planifica con Neon/Argon/Carbon y ejecuta con Hydrogen, sujeto a plan; terceros si están habilitados | Low, Medium, High y Extra/xhigh en Neon y Hydrogen; Orchestrator no ajusta /effort | Browser QA y trabajo visual; ensayar Orchestrator solo en trabajos complejos donde supere el modelo directo |
| Orca | Runtime externo para coordinar CLI, Runs, Tasks, Dispatches, workers y worktrees | No reemplaza esfuerzo del modelo subyacente | Puente opcional entre CLIs, no es otro LLM |

**Orca:** línea base documentada `v1.4.245` y revisión pública `v1.4.261` al 17-11. La release pública más reciente verificada al **2026-11-23** es **`v1.4.272`**, con notas de recuperación de bots, reanudación de sesiones y trabajadores interrumpidos. Estado **PUBLIC_ONLY**, no versión instalada ni prueba de compatibilidad con el dispatcher. Nunca actualizar Orca, hooks o perfiles sin inspección, backup y prueba aislada.

**Fuentes oficiales, revisadas 2026-11-23:**
- OpenAI Codex/Work: https://learn.chatgpt.com/docs/models ; créditos y cuotas: https://learn.chatgpt.com/docs/pricing .
- Claude Code: https://code.claude.com/docs/en/model-config ; precios API: https://platform.claude.com/docs/en/about-claude/pricing
- Antigravity: https://antigravity.google/docs/models , https://antigravity.google/docs/cli/commands/effort y https://antigravity.google/docs/plans
- Orca: https://github.com/stablyai/orca/releases/tag/v1.4.272 y https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx

## Delta público frente al 2026-11-17; NO_VERIFICADO en el PC
| Fuente | Cambio verificado en documentación | Restricción y decisión |
|---|---|---|
| OpenAI | GPT-6.2 Astra/Sol siguen documentados para Work/Codex; no se atribuye a una fecha de lanzamiento posterior | Créditos Standard por 1M entrada/caché/salida: Sol 50/2.5/250 y Astra 200/10/1000. Dependen de plan/velocidad; facturación API es distinta. Mantener modelo bajo viable |
| Claude Code | Alias opusplan: Opus plan + Sonnet ejecuta; mínimos de CLI: Opus 5.5 >=2.1.280, Sonnet 5.5 >=2.1.284, Haiku 5.5 >=2.1.293 | API USD por 1M entrada/salida: Haiku 5.5 0.10/0.50 hasta prompts 100K (más después), Sonnet 5.5 2/10, Opus 5.5 4/20. No equivale a cuota de suscripción. Probar modo híbrido si CLI compatible |
| Antigravity | Gemini 4 Neon (hasta 512K contexto, xhigh), Orchestrator: planner Neon/Argon/Carbon + ejecutor Hydrogen según plan | Neon no está en Free/Plus; Pro/Ultra/Enterprise sujetos a oferta. Cuotas de cinco horas y semanales, saldo personal desconocido. No convertir en predeterminado |
| stablyai/Orca | Release v1.4.272 frente a v1.4.261 del 17-11; recuperación de workers y sesiones indicada en changelog | Compatibilidad con scripts locales, estado de instalación y continuidad real NO_VERIFICADOS. No actualizar binarios |

**Control de gastos:** nunca confundir precio API en USD, créditos Codex/Work, cuotas de suscripción y costos del runtime. Decidir por entregable aprobado, minutos, revisión y fallos; tarea sencilla -> solución directa; solo delegar cuando haya ahorro o mejora comprobada. Fuentes y tarifas consultadas 2026-11-23; sujetas a cambio.

**Pruebas pendientes, sin ejecución de agentes:** JSON parse + contratos de routing; smoke heurístico plan-only; posteriormente preflight de versión/modelos/cuotas en el PC autorizado; luego piloto A/B con datos anonimizados y métricas costo/calidad; finalmente ensayo aislado de recuperación de Orca. No se ha medido ahorro ni ejecutado workers en esta revisión.

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
