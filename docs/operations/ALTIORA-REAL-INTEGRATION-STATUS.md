# Altiora — estado real de integraciones y certificación operativa (2026-11-03, rev. 2)

Ejecutado por Claude Code 2.1.317 (Sonnet 5.5) en esta máquina, desde `origin/main` @ `472dbf7`. Sin instalaciones, sin cambios de configuración de clientes, sin credenciales leídas, sin gasto. Niveles: `REFERENCED < CONFIGURED < INSTALLED < SERVER_RUNNING < AUTHENTICATED < TOOL_CALL_VERIFIED`; además `BLOCKED` y `FAILED`.

## 1. Sincronización
| Hecho | Evidencia |
|---|---|
| PR #68, #69 y #70 fusionados en `main` | `gh pr view`: MERGED 2026-11-03 15:47Z; `git log origin/main` → `472dbf7`, `8a11916`, `bc0cff6` |
| Árbol de trabajo | worktree limpio `wt-cert` creado desde `origin/main`; la copia canónica `altiora-unificado` sigue 6 commits atrás y no se tocó |

## 2. Diagnósticos ejecutados
| Diagnóstico | Resultado | Nota |
|---|---|---|
| `npm run check` | **PASSED**, 0 errores, todas las suites 0 fallos | incluye doctor, handoff, catálogo, routing, build de agentes |
| `npm run skills:audit` | 355 skills, media 98,3 (= línea base) | propias 100; externas 93,9 |
| `npm run routing:eval` | PASS 17/17 | ahorro de tokens NOT_MEASURED |
| `npm run capability:doctor` | Node/FFmpeg/FFprobe/Python/Git OK; **Blender: ERROR**; aerender NOT_DETECTED; antigravity MISSING en el adaptador del repo | no prueba conexión de clientes |
| `node scripts/omniroute-preflight.mjs` | service **UNREACHABLE** en 127.0.0.1:20128 | GET local, sin clave |
| `npm run security:scan` | exit 2: exige `--target`; es el gate de skills nuevas, no un escáner del repo | NOT_RUN sobre el repo |
| `node scripts/integration-inventory.mjs` | 5072 archivos; Headroom, Palacio Mental, Claude Red solo REFERENCED | |

## 3. Matriz de componentes
| Componente | Estado | Evidencia | Siguiente acción |
|---|---|---|---|
| Claude Code | **TOOL_CALL_VERIFIED** | 2.1.317, esta sesión | — |
| Orca | **TOOL_CALL_VERIFIED** | v1.4.247; creó 2 worktrees y lanzó Antigravity (ALT-TRIAD-001) | — |
| Antigravity | **TOOL_CALL_VERIFIED** | lanzado vía Orca, sesión e32db730…, commit `e1d774f` | — |
| Codex | **BLOCKED** | CLI 0.166.0-alpha.5.1, login ChatGPT; no ejecutó el QA: sin créditos (dicho por el usuario) | recargar créditos |
| Colaboración triada (ALT-TRIAD-001) | **PARCIAL** | brief `3c8efc2` + UI `e1d774f` reales; QA de Codex ausente; revisión sustituta de Claude (no cuenta). Informe: rama `altiora-enterprise-os`, commit `6436709` | relanzar QA en `triad-qa` |
| Playwright MCP | **TOOL_CALL_VERIFIED** | v1.65.0-alpha; 25 herramientas; `browser_navigate` a página local + `browser_close` OK | aprobar en `claude` (ver §4) para que cargue en sesión |
| Chrome DevTools MCP | **SERVER_RUNNING** | v1.12.0, initialize OK en 6 s; sin llamada de herramienta | idem aprobación |
| altiora-shared MCP | **CONNECTED** (`claude mcp list`) | apunta a carpeta de 2026-10-18 (`outputs/altiora-connection`), **desactualizada**; en sesión falló por timeout, luego conectó | reapuntar al laboratorio vigente (Codex lo tenía pendiente) |
| altiora-after-effects, dak-* (6), metricool | **CONFIGURED**, Pending approval | `claude mcp list` | aprobar solo los necesarios; dak-* además sin ADC de Google; aerender no detectado |
| Conectores claude.ai: Docs, Vercel, Figma, Notion, Slack, Gmail, Canva, Ahrefs, HubSpot | **AUTHENTICATED (conectados)** | `claude mcp list` ✔; ninguno se invocó | usar bajo demanda |
| Supermetrics, Klaviyo, Windsor.ai | **BLOCKED** | Needs authentication | `/mcp` si se necesitan |
| Plugin marketing (11 MCP), windsor-ai | **BLOCKED** | Needs authentication / 2 sin URL (calendar, gmail) | duplican conectores claude.ai: no autenticar |
| Plugins: marketing, searchfit-seo, windsor-ai (synced), orca-agent-view | **INSTALLED/loaded** | `claude plugin list` | — |
| Plugin adobe-for-creativity | **INSTALLED, disabled** | `claude plugin list` | dejar apagado |
| Agentes `altiora-*` (12+) y 355 skills | **DESCUBIERTOS** | listados en la sesión; `check` valida generación | NO lanzados salvo los de la triada |
| Frontend Design | **DESCUBIERTO (Claude)**; copia en `~/.codex/skills` | skill `frontend-design` en el listado de esta sesión | falta tarea UI validada con capturas y QA |
| OmniRoute | **TOOL_CALL_VERIFIED (catálogo); generación NOT_TESTED** | Ver §7: arranque local aislado en 127.0.0.1:20129, `/api/health` 200, `/v1/models` 401 sin clave y 200 con clave local (468 entradas, alias `auto/*` presentes), **0 proveedores conectados**; sin inferencia | decidir proveedor gratuito/aprobado antes de probar generación |
| Headroom | **REFERENCED** | no hay binario, paquete pip/npm ni carpeta | identificar y auditar `headroomlabs-ai/headroom` antes de instalar |
| Palacio Mental | **BLOCKED_IDENTITY** | no existe en el equipo ni en el historial salvo el runbook | el usuario debe dar la URL o el nombre exacto |
| Claude Red / claudered | **BLOCKED_IDENTITY** | idem | idem |
| Blender | **TOOL_CALL_VERIFIED (arranque headless)** | 5.2.2 LTS, `--background --factory-startup --disable-autoexec` → EEVEE, exit 0; doctor AVAILABLE en 3 ejecuciones aisladas; sin render ni MCP | el `ERROR` previo era un timeout de 5 s bajo carga: corregido a 15 s (§7) |
| After Effects (aerender) | NOT_DETECTED | doctor | no necesario para el piloto |

## 4. Discrepancias y riesgos encontrados
1. **OmniRoute: identidad — RESUELTA.** `diegosouzapw/OmniRoute` es el mismo repositorio que `cheaper-inference/OmniRoute` (la API de GitHub redirige; `full_name` canónico = `cheaper-inference/OmniRoute`, MIT, no es fork). El paquete npm 3.8.52 coincide con el último release `v3.8.52`. Node 24.21.0 cumple `engines >=24`.
2. **OmniRoute carga `.env` del directorio actual** al ejecutar su CLI (lo vimos al pedir `--help`). Ejecutarlo siempre desde un directorio neutro para no mezclar secretos de proyectos.
3. **Solape:** OmniRoute trae módulos `memory` (memoria conversacional) y `compression`. Pueden cubrir parte de lo que se esperaba de Palacio Mental y Headroom. El runbook prohíbe dos proxies sobre la misma BASE_URL: decidir una sola ruta antes de instalar Headroom.
4. **MCP del proyecto en "Pending approval":** playwright, chrome-devtools, dak-*, metricool y after-effects no cargan en sesión hasta aprobarlos. Eso explica los timeouts que vimos antes. Ejecutar `claude` en el repo y aprobar solo los necesarios.
5. **Codex sin créditos:** bloquea la revisión independiente que exige `ROUTING.md` para entregas a clientes.
6. `.mcp.json` contiene rutas absolutas de usuario: no portable.

## 5. ¿Puede Altiora recibir un cliente hoy?
- **Sí, con límites.** Existe el paquete `docs/altiora-business/entrega/` (compuertas G1–G8, plantillas, aceptación), 355 skills y roles verificados por `npm run check`, navegador automatizable (Playwright verificado) y Orca para repartir trabajo.
- **No verificado:** un ciclo completo con un cliente real (cero clientes de pago), la revisión independiente con una IA distinta a la que construye (Codex bloqueado), OmniRoute/Headroom y memoria persistente por cliente.
- Ninguna de las cuatro integraciones prioritarias (OmniRoute, Headroom, Palacio Mental, Claude Red) es necesaria para entregar un proyecto; son optimización.

## 6. Aprobaciones pendientes (no ejecutadas)
1. Arrancar OmniRoute localmente en 127.0.0.1:20128 (sin proveedores de pago) para probar `/v1/models`.
2. Dar URL/identidad exacta de Palacio Mental y Claude Red.
3. Auditar e instalar Headroom (instalación sensible), solo tras decidir la ruta con OmniRoute.
4. Aprobar en `claude` los MCP del proyecto que se usen (playwright y chrome-devtools como mínimo).
5. Recargar Codex y relanzar el QA de ALT-TRIAD-001.

## 7. Rev. 2 — pruebas realizadas tras la autorización de OmniRoute y Blender
**Condiciones de la prueba:** solo 127.0.0.1, directorio neutro sin `.env` de proyectos, `DATA_DIR` aislado (no se tocó `~/.omniroute`), contraseña y clave generadas por mí y borradas al terminar, sin proveedores, sin instalar nada. Puerto 20129 para no interferir con la instancia ajena de 20128.

| Paso | Resultado |
|---|---|
| Identidad/versión/Node | ver riesgo 1 (resuelto) |
| Arranque 1 (puerto 20128, `--headless`) | Arrancó, pero `/` redirigía a `/dashboard` y el puerto ya tenía **otra instancia** (ver hallazgo A). Detenido; solo mis PID |
| Login con la contraseña generada | Falló (401): la base se había inicializado en el primer arranque con otra contraseña. Iteración 1 de 3 |
| Reinicio con base nueva | Login 200, creación de clave local 201. Iteración 2 de 3 |
| `GET /api/health` | 200 `{"status":"ok"}` |
| `GET /v1/models` sin clave | 401 `invalid_api_key` (correcto) |
| `GET /v1/models` con clave local | **200, 468 entradas**; alias `auto/cheap`, `auto/coding`, `auto/smart`, etc. presentes; origen: aihorde 179, devin-cli-agentic 127, codex-app-server 52, combo 37, … |
| `GET /api/providers` | **0 conexiones**: el catálogo no es capacidad usable |
| Inferencia | **NOT_TESTED** (no hay proveedor aprobado) |
| Limpieza | procesos propios detenidos (0 escuchas en 20129), directorio temporal y credenciales borrados |

### Hallazgos nuevos
- **A. Instancia ajena de OmniRoute expuesta a la red.** PID 41288 (hijo de 45220), iniciado hoy 07:26, escucha en `0.0.0.0:20128` y responde también por la IP LAN de esta máquina (`/api/health` 200, `/v1/models` 401). No la inició esta sesión y **no se tocó**. Riesgo: cualquier equipo de la red local puede alcanzar el panel. Acción: el dueño decide si la detiene o la reinicia ligada a 127.0.0.1 (`HOSTNAME=127.0.0.1`).
- **B. Falso negativo del preflight (corregido).** `scripts/omniroute-preflight.mjs` usaba `redirect: 'error'`; como `/` redirige (307) a `/dashboard`, siempre informaba `UNREACHABLE` aunque el servicio respondía. Cambio a `redirect: 'manual'`: ahora informa `HTTP_RESPONDED_NOT_IDENTIFIED` + `AUTH_REQUIRED_OR_DENIED`. Sigue sin identificar el servicio como OmniRoute y sin probar proveedores.
- **C. Falso negativo del doctor de Blender (corregido).** `scripts/visual-preflight.mjs` sondeaba con timeout de 5 s; Blender en frío bajo carga lo superaba y se informaba `ERROR`. Timeout a 15 s; `visual:preflight:test` 10/10.
- **D. El `.env` del paquete OmniRoute** contiene secretos propios (JWT, cifrado, contraseña inicial) y OmniRoute lo carga al ejecutar su CLI. No se leyeron valores. Mantener cwd y `DATA_DIR` neutros.
- **E.** `visual:preflight` informa `npm: NOT_FOUND` y `Python 3: ERROR` cuando se ejecuta vía `npm run`; el doctor sí detecta Python. Sondeo de wrapper de Windows no fiable: no bloquea, pendiente.

## 8. Revisión independiente de ALT-TRIAD-001
Preparada, **no ejecutada**: `tests/triad/ALT-TRIAD-001-qa-request.md` y `tests/triad/contrast-check.py` (recalcula los 11 pares: todos cumplen AA; 9 con valor declarado inexacto). Requiere Codex con créditos u otro revisor que no haya escrito brief ni UI. Hasta entonces el estado de la triada es **PARCIAL** y el issue #65 no debe marcarse PASS.

## 9. Acciones necesarias (actualizado)
| # | Acción | Quién | Bloquea |
|---|---|---|---|
| 1 | Decidir qué hacer con la instancia 20128 abierta a la red (PID 41288) | usuario | seguridad |
| 2 | Recargar Codex y lanzar el QA preparado | usuario | cierre de ALT-TRIAD-001 |
| 3 | Aprobar playwright y chrome-devtools en `claude` | usuario | uso en sesión |
| 4 | Elegir proveedor gratuito/aprobado para probar inferencia en OmniRoute (con tope de gasto 0) | usuario | prueba de generación |
| 5 | URL exacta de Palacio Mental y Claude Red | usuario | integración |
| 6 | Headroom: no instalar hasta decidir ruta con OmniRoute (que ya incluye compresión/memoria) | usuario | — |
| 7 | Reapuntar `altiora-shared` al laboratorio vigente | Codex/usuario | — |
