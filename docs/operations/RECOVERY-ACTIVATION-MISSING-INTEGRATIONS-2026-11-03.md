# Altiora — recuperación y activación de integraciones pendientes (2026-11-03)

## Objetivo
Reconciliar **todos** los intentos anteriores de integrar skills, subagentes, plugins, servidores MCP y conectores. No confundir una referencia, un adaptador generado, una instalación local y una conexión probada. Prioridades: **Headroom (compresión de contexto), Palacio Mental, OmniRoute, Claude Red/claudered**, y revalidar Frontend Design y Playwright.

### Estado inicial comprobado desde GitHub
- `CLAUDE.md` remite a `skills/`, `.claude/skills/` generada por `npm run agents:build`, `references/discovery-manifest.json` y reglas de routing. No editar archivos generados a mano.
- `team/ROUTING.md` define enrutamiento y ahorro; evita encender conectores pesados por defecto.
- `package.json` incluye `capability:doctor`, `skills:audit`, `security:scan`, `routing:eval`, `check`.
- OmniRoute preflight del PR #69 debe revisarse e integrarse antes de usarlo; nada de esto certifica un servicio local.
- La identidad del proyecto exacto «Palacio Mental» y de «Claude Red/claudered» NO está resuelta; **no instalar un repositorio por similitud de nombre**.
- Hay varios proyectos Headroom. Para compresión de contexto el candidato es `headroomlabs-ai/headroom`; otros Headroom solo muestran cuotas. Verificar identidad, licencia, seguridad y compatibilidad con la configuración existente.

## Ejecución local guiada: Claude Code, desde checkout confiable
1. `git status --short`; `git branch --show-current`; inspeccionar PR #67, #68, #69 y sus cambios; no asumir que las ramas de PR están fusionadas.
2. `npm run resume`, `npm run capability:doctor -- --text`, `npm run skills:audit`, `npm run security:scan`. Si no existe el script en la rama usada, reportar ese hecho, no inventar un éxito.
3. Reconciliar manifest, índice y directorios de cada runtime, incluyendo `skills/`, `.claude/skills/`, `.claude/agents/`, `.agents/`, `.gemini/`, archivos MCP, configuración de usuario de Claude/Codex/Antigravity, lockfiles, workflows y PRs no fusionados. Crear un inventario con ID canónico, fuente, versión, runtime, dependencia, riesgo, último test y evidencia.
4. Buscar nombres exactos y variantes (Headroom, Palacio Mental, mental palace, memory palace, Claude Red, claudered, OmniRoute, Frontend Design, Playwright), y **también todos los ítems** del historial de manifest, registros, documentación, PRs, referencias y carpetas temporales. Los ausentes deben aparecer en el informe; no reducir el alcance a los cuatro nombres prioritarios.
5. Clasificar por separado: `REFERENCED`, `CONFIGURED`, `INSTALLED`, `SERVER_RUNNING`, `AUTHENTICATED`, `TOOL_CALL_VERIFIED`, `BLOCKED`, `FAILED`. Cada nivel requiere evidencia fechada y verificable, con secretos redactados.

## OmniRoute: activación bajo prueba
- Fuente candidata: https://github.com/cheaper-inference/OmniRoute . Revisar release, licencia y changelog antes de instalar/actualizar.
- Verificar proceso, versión, servicio en `127.0.0.1:20128`, salud del dashboard, modelos mediante API autenticada, MCP y proveedor elegible. Una página HTTP que abre NO certifica inferencia.
- Usar cuentas/proveedores ya autorizados. **No registrar ni pagar nuevos proveedores** sin permiso. No imprimir tokens, claves ni URLs con credenciales.
- Probar `auto/cheap`, `auto/coding`, `auto/smart`, solo cuando estén realmente disponibles. Límite estricto de costo, fallback solo a modelos aprobados; prohibido fan-out pago por defecto. La compatibilidad Claude/Codex/Antigravity debe probarse por cliente sin alterar globalmente su proveedor predeterminado.
- Benchmark del mismo conjunto de tareas con y sin router: calidad evaluada ciegamente, tokens entrada/salida, latencia, costo real (y caché). No afirmar ahorro sin línea base comparable.

## Headroom: evitar confusión entre homónimos
- Para optimización de contexto investigar https://github.com/headroomlabs-ai/headroom y su CLI/MCP. Contrastar con las variantes de cuota/burn rate; no sustituir uno por otro.
- Auditoría previa de interceptación de tráfico, tratamiento de datos, variables de entorno, puertos, hooks y cambios de configuración. **No activar simultáneamente dos proxies que compitan por la misma BASE_URL**.
- Primero ejecutar un ensayo reversible con archivos sintéticos, verificar rehidratación del contenido original, ausencia de pérdida de requisitos, caché y métricas reales.
- Integrar Headroom con OmniRoute solo si arquitectura, seguridad y pruebas demuestran que combinarlos aporta valor; de lo contrario elegir uno por flujo.

## Palacio Mental y Claude Red
- Rastrear referencias del usuario, README/URLs del repositorio, manifests, commits, PRs y skills previas.
- Confirmar URL exacta, propietario, licencia, dependencias, finalidad, scopes, reputación y riesgos antes de instalar.
- Si no se identifica unívocamente, marcar `BLOCKED_IDENTITY` y documentar los candidatos. No fabricar implementación que suplante la herramienta original.
- Si «Palacio Mental» es memoria persistente, comprobar consentimiento, separación por cliente, TTL/retención, capacidad de borrado, redacción de PII y aislamiento del contexto.
- Para «Claude Red», auditar scripts, permisos y comportamiento antes de conectarlo a credenciales o repositorios privados.

## Frontend Design, Playwright y resto de ecosistema
- Frontend Design: verificar skill canónica, generación de adaptadores, descubrimiento en la sesión de Claude y una tarea UI pequeña validada con capturas, accesibilidad y QA.
- Playwright: iniciar MCP y listar herramientas; abrir una página de prueba local autorizada, ejecutar operación segura y cerrar el proceso. Una prueba histórica no certifica la sesión actual.
- Revisar Blender, After Effects, Orca, Figma, Vercel, GitHub, n8n, Graphify, bibliotecario, Metricool, HubSpot, Notion, Gmail, Slack, Ahrefs, Canva y demás entradas encontradas en manifiestos. No activar todo indiscriminadamente: disponibilidad bajo demanda cuando corresponde.
- Cotejar todos los PRs y carpetas que hayan agregado skills/conectores; detectar configuraciones omitidas en builds y rutas rotas.

## Criterios de aceptación
- Inventario **completo**, con fuente y estado por componente, comparado contra histórico.
- Para cada activación exitosa: versión, runtime, comando/proceso, resultado de operación funcional y fecha.
- Para cada bloqueo: motivo y acción específica necesaria.
- Validaciones: `npm run agents:build` (solo si cambios a fuente canónica), `npm run check` y pruebas específicas, sin falsear resultados.
- Un informe `docs/operations/ALTIORA-REAL-INTEGRATION-STATUS.md` con matriz, benchmarks y riesgos. No modificar archivos críticos, instalar binarios no auditados, tocar credenciales, publicar, fusionar PRs o incurrir en gastos sin autorización adecuada.
- Ciclos de reparar -> probar -> comparar máximo 3 por incidencia; revertir si rompe una capacidad existente.

## Mensaje operativo
«Claude Code: abre Altiora en la computadora y ejecuta de forma inmediata este runbook. Empieza por el inventario histórico completo, después activa de forma segura OmniRoute y Headroom solo cuando no compitan, identifica unívocamente Palacio Mental y Claude Red, revalida Frontend Design/Playwright y todos los MCP ausentes. Demuestra cada activación con una llamada real. Entrega el estado comprobado y lo bloqueado; sin inventar instalaciones ni tocar secretos.»
