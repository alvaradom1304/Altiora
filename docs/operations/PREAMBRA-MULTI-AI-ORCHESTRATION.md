# PREAMBRA OS · política compartida de orquestación multi-IA
**Revisión de fuentes públicas:** 2026-11-17. **Marca comercial:** PREAMBRA; rutas históricas Altiora se conservan. **Estado:** política versionada; no equivale a sesiones de otras IAs autenticadas ni a Orca ejecutándose.

## Instrucción universal: se aplica desde ChatGPT, Codex, Claude Code o Antigravity
Al recibir un encargo, la IA debe conocer y considerar **ChatGPT, Codex, Claude Code, Antigravity y Orca**, incluso si la IA inicial no tiene acceso directo a ellos. Consultar `AGENTS.md`, `team/ROUTING.md`, este documento, y los metadatos relevantes; **no** abrir toda la biblioteca. Informar: (a) qué puede hacer aquí mismo; (b) qué convendría delegar a otro agente; (c) su modelo/esfuerzo adecuado; (d) si la ejecución real está verificada, no verificada o bloqueada.

Ningún rol está «encendido» solo por figurar en Markdown. ChatGPT en una conversación **no puede iniciar Orca ni operar la laptop** sin un ejecutor/conector capaz, ni modificar su propio backend a voluntad. Claude Code, Codex y Antigravity **no comparten** por sí mismos la misma cuenta, cuota, modelo ni MCP. GitHub sirve como fuente versionada de estado, no como transporte de una sesión viva.

## Gobierno mínimo
- La persona fundadora aprueba objetivos, presupuesto, credenciales, publicación y acciones externas.
- ChatGPT: discovery, diagnóstico, dirección empresarial y revisión ejecutiva. No asignar un modelo de ChatGPT al ejecutor Orca como si fuera una CLI sin prueba.
- Claude Code: director operativo de iniciativas multifase, marca, copy, interfaz y revisión de estrategia.
- Codex: arquitectura, código, integraciones, unit economics y QA reproducible.
- Antigravity: producción web inmersiva, 3D, navegador, motion y auditoría visual, o como alternativa cuando tenga las capacidades requeridas.
- Orca: **transporte y coordinación** de terminales/worktrees/Run/Task, no motor de razonamiento ni «cuarta IA». Usar el Orca instalado solo cuando `orca status --json` responda y la versión/adaptador hayan sido verificados.
- QA: agente distinto o pase separado cuando el riesgo importe; un único escritor por archivo y por etapa; no ejecutar tareas dependientes como si fueran paralelas.
- Cerrar siempre con evidencia (artefacto, log/test, commit, dueño, estado, siguiente paso). Si no se ejecutó, escribir `NOT_RUN`.

## Router: modelo y esfuerzo por necesidad, no por prestigio
| Tarea | Ejecutor preferido | Esfuerzo inicial | Escalar solo cuando |
|---|---|---|---|
| Resumen, limpieza, listados, ajustes cortos | IA actual | low | No pasa un criterio de aceptación |
| Brief comercial y copy de PREAMBRA | Claude Code o ChatGPT | medium | Hay conflicto de posicionamiento, múltiples audiencias o requisitos rigurosos |
| Arquitectura backend, seguridad, cálculo de márgenes | Codex | high | Riesgo económico/seguridad material: xhigh y QA independiente |
| Experiencia visual/3D, navegador y GSAP | Antigravity | medium/high | Scene complexity y pruebas visuales exigen más, con presupuesto |
| Plan de varias dependencias, auditoría interfuncional | Claude Code coordina; Codex/Antigravity ejecutan dominios propios | medium para router, high para tareas complejas | Evidencia de error/impacto o complejidad medible |

El enrutador debe consultar primero los **modelos disponibles de esa sesión**, cuota, precio/consumo y flags aceptados; luego elegir el menor esfuerzo que pase los tests. Aliases de familias (Haiku/Sonnet/Opus, GPT/Codex, Gemini Flash/Pro/Argon/Carbon/Hydrogen) son **candidatos**, no nombres de CLI garantizados. Si falla un modelo: fallback explícito con registro; nunca cambiar a uno más caro en silencio. Evitar loops abiertos: máximo dos intentos correctivos automáticos por tarea, luego revisión.

### Información actualizada: fuentes oficiales, no supuestos sobre instalaciones
- **OpenAI:** las familias GPT-6/GPT-6.1/GPT-6.2 y el esfuerzo `reasoning.effort` dependen del modelo. No asumir que `max`, `none` o un alias específico funciona en un Codex local. Ver https://developers.openai.com/api/docs/guides/reasoning y https://developers.openai.com/api/docs/models .
- **Anthropic:** su documentación enumera Claude Haiku, Sonnet y Opus (incluidas generaciones 5); esfuerzo y thinking dependen del modelo y del cliente. No fijar `opus` como la única opción «high». Ver https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices .
- **Google Antigravity:** la documentación de Gemini Enterprise incluye Gemini 4 Hydrogen/Carbon/Argon, 3.8/3.7/3.6 Flash y Claude 5.5 según permisos; la lista en una licencia empresarial **no prueba** que la cuenta personal los tenga. Ver https://docs.cloud.google.com/gemini/enterprise/docs/ai-developer-tools-settings .
- **Orca:** la documentación actual exige verificar el runtime (`orca status --json`) y habilitar la función experimental donde corresponda; comandos antiguos como `orca orchestration run` no realizan acciones. Ver https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx y https://github.com/stablyai/orca/releases .
- **No usar** como fuente de verdad perpetua las versiones que aparezcan en documentos históricos de octubre de 2026. Actualizar solo después de comprobar fecha, changelog, compatibilidad, permisos y costo.

## Puntuación de capacidades: escala reproducible, no «potencia de IQ»
Cada ejecutor obtiene **0–10 puntos de preparación operativa**: instrucciones compartidas 2; documentación oficial vigente 2; test de enrutamiento reproducible 2; invocación real del ejecutor autenticado desde el entorno correspondiente 2; prueba completa con handoff/QA 2. Registrar también fecha, evidencia y `UNKNOWN` para lo no probado. Este score **no** clasifica inteligencia, calidad intrínseca de modelos ni ahorro medido. Se documenta la matriz en `docs/operations/preambra-model-matrix.json`.

## Primera tarea: PMO-ORCA-001 — prueba del sistema
1. Ejecutar en checkout actualizado `python scripts/preambra-orca-smoke.py` (sin red, sin tokens y sin iniciar agentes); exige **3 rutas correctas**, salida de contrato, guard de ejecución y señala las incertidumbres.
2. En la PC propia: `orca status --json`; `claude --version`; `codex --version`; `agy --help`; consultar modelos y logins por los medios vigentes del cliente. No revelar credenciales ni guardar respuestas personales en repo público.
3. Ejecutar `npm run orca:dispatch -- --router heuristic "Revisar el branding y copy comercial de PREAMBRA"` para un plan seguro y revisar `preferred_ai`, `effort` y `skills`.
4. Para validar **Orca real**, crear **una tarea de lectura solamente** dentro de Orca desde su interfaz o comando vigente y registrado, asignar Claude Code o Codex, generar el resultado y registrar ID/estado/evidencia. **No usar `ALTIORA_DISPATCH_EXECUTE=1`** para saltarse la protección. No ejecutar trabajo paralelo ni modificar producción en el primer piloto.
5. QA: resultado del test, respuesta real del agente, permisos, costos expuestos por el proveedor si existen y checkpoint. Si el runtime no responde, estado `BLOCKED_RUNTIME`, no `PASS`.

## Handoff universal
Campos obligatorios: `job_id`, `brand`, `goal`, `agent`, `model_observed` (o `UNKNOWN`), `effort`, `inputs`, `owned_paths`, `dependencies`, `budget_limit`, `acceptance`, `artifacts`, `checks`, `status`, `evidence`, `next_action`. No guardar prompts enteros con datos privados, tokens o credenciales.

## Gate de aceptación
`npm run check` en CI/local tras cambios; comparar evidencia con test real del ejecutor. Esta versión establece la **decisión, el contrato y un smoke reproducible**; la sesión Orca y los modelos de la laptop permanecen `NOT_VERIFIED` hasta ejecutar la etapa 4.
