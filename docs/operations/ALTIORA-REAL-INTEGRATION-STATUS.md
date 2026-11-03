# Altiora — estado real de integraciones y certificación operativa (2026-11-03, rev. 3)

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
| OmniRoute | **SERVER_RUNNING, solo loopback, con autenticación; generación NOT_TESTED** | Reiniciado el 03/11 10:31 en `127.0.0.1:20128` (PID 24652) con los datos y credenciales existentes; LAN inaccesible; rutas admin 401 sin sesión (§10). Catálogo `/v1/models` 468 entradas verificado en la prueba aislada (§7) | proveedor aprobado para probar inferencia |
| Headroom | **REFERENCED** | no hay binario, paquete pip/npm ni carpeta | identificar y auditar `headroomlabs-ai/headroom` antes de instalar |
| Palacio Mental | **BLOCKED_IDENTITY** | no existe en el equipo ni en el historial salvo el runbook | el usuario debe dar la URL o el nombre exacto |
| Claude Red / claudered | **BLOCKED_IDENTITY** | idem | idem |
| Blender | **TOOL_CALL_VERIFIED (render CPU); EEVEE FAILED** | 5.2.2 LTS: render Cycles CPU 192×108 en 2,44 s, PNG válido (§10). EEVEE headless falla en esta GPU (AMD Radeon Vega 3: `HW_UNSUPPORTED`, access violation, exit 139) | usar Cycles CPU o EEVEE con ventana; no prometer EEVEE headless; sin MCP de Blender |
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
- **A. [RESUELTO EN §10] Instancia de OmniRoute expuesta a la red.** PID 41288 (hijo de 45220), iniciado hoy 07:26, escucha en `0.0.0.0:20128` y responde también por la IP LAN de esta máquina (`/api/health` 200, `/v1/models` 401). No la inició esta sesión y **no se tocó**. Riesgo: cualquier equipo de la red local puede alcanzar el panel. Acción: el dueño decide si la detiene o la reinicia ligada a 127.0.0.1 (`HOSTNAME=127.0.0.1`).
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

## 10. Rev. 3 — P0: seguridad de OmniRoute (resuelto) y render de Blender
### 10.1 Identificación del PID 41288 (inequívoca)
`node.exe` (`C:\Program Files\nodejs\node.exe --dns-result-order=ipv4first --max-old-space-size=4096 …\npm\node_modules\omniroute\dist\server-ws.mjs`), usuario `Usuario`, iniciado 03/11 07:26:39, hijo de PID 45220 (`omniroute.mjs`, `serve` por defecto, 07:26:32), que cuelga de una consola PowerShell interactiva (PID 39956, desde 02/11 23:02). Datos: `~/.omniroute` (SQLite activo, `call_logs` con llamadas reales de las 08:00, es decir, **el servicio se usaba**). Único listener público: `0.0.0.0:20128`; otros puertos del PID (20131, 20132) solo en 127.0.0.1.

### 10.2 Intervención
| Paso | Resultado | Evidencia |
|---|---|---|
| Respaldo en caliente de `~/.omniroute` + estado de procesos/conexiones | OK | `~/.altiora-backups/omniroute-2026-11-03_pre-intervencion/` (data-en-caliente, procesos.json, conexiones.json); ACL restringida a `Usuario` |
| Parada con `omniroute stop` | **Falló en silencio**: informó «Server stopped» pero el PID 41288 siguió vivo y escuchando | 2 comprobaciones posteriores |
| Parada manual de 45220 (lanzador) con identidad re-verificada | OK; 41288 cayó con él; 0 procesos, 0 escuchas en 20128/20131/20132; la consola 39956 sigue viva | `Get-CimInstance` / `Get-NetTCPConnection` |
| Respaldo consistente tras parada (sqlite + wal + shm) y `.env` del paquete (clave de cifrado) | OK, **sin leer** los archivos; hashes SHA-256 registrados | carpeta `data-tras-parada`, `paquete.env.CONFIDENCIAL` |
| Reinicio en loopback (`HOSTNAME=127.0.0.1`, `serve --daemon --no-open`, cwd neutro, mismos datos) | OK: PID 24652, único proceso OmniRoute | `Get-CimInstance`, log |
| Local | `127.0.0.1`/`localhost`: health 200, `/v1/models` sin clave 401 | curl |
| Desde la red | `192.168.1.113:20128` → **sin respuesta**; 20129, 3000, 8080 en la IP LAN también sin respuesta | curl |
| Autenticación | `/api/providers`, `/api/keys`, `/api/settings` → 401 sin sesión; `/dashboard` → 307 (login) | curl |
| Otro proceso exponiendo el servicio | Ninguno: 1 solo proceso OmniRoute, 0 listeners `0.0.0.0` en 20128–20132 | consultas de procesos y puertos |
No se leyó ni imprimió ninguna credencial; no se borró ni modificó ninguna base ni configuración persistente.

### 10.3 Riesgos residuales (no resueltos)
1. **Regla de firewall de entrada «Node.js JavaScript Runtime» (Allow, perfil Public)**: permite exponer cualquier servicio de Node si se vincula a 0.0.0.0. No se modificó (configuración global). Recomendación: restringirla o pasarla a perfil Private.
2. `omniroute stop` no detuvo el proceso: no fiarse de él; verificar siempre con `Get-NetTCPConnection`.
3. La clave de cifrado de la base vive en el `.env` **del paquete npm**; actualizar/reinstalar el paquete puede dejar la base ilegible. Hay copia en el respaldo.
4. Quien lanzó la instancia original (consola 39956) puede volver a arrancarla con `omniroute` sin `HOSTNAME`. Documentar el comando seguro: `HOSTNAME=127.0.0.1 omniroute serve --daemon --no-open`.
5. La instancia en `--daemon` ya no depende de esa consola, pero **no sobrevive a un reinicio del equipo**.

### 10.4 Blender: prueba de render (sin publicar)
Script `docs/operations/evidence/blender-render-smoke.py` (cubo, luz solar, cámara; 192×108). Resultados:
| Intento | Resultado |
|---|---|
| EEVEE headless | **FAIL**: `Compute link error: HW_UNSUPPORTED`, `EXCEPTION_ACCESS_VIOLATION`, exit 139 (GPU AMD Radeon Vega 3, driver 26.20.14046.3) |
| Cycles CPU, ruta `//…` | **FAIL** (error mío: `//` se resolvió a `C:\`; no se escribió nada) — iteración 1 de 3 |
| Cycles CPU, ruta absoluta | **PASS**: 2,44 s, PNG 192×108, 12 260 bytes, sha256 `ce7daa10f9516e15…`, exit 0; imagen no vacía (cara superior verde del cubo; encuadre mejorable) — iteración 2 de 3 |
El PNG queda **solo local** en el scratchpad de la sesión; no está en el repositorio.

### 10.5 ALT-TRIAD-001: correcciones y QA independiente
- `ALT-TRIAD-001-ui.md` corregido: 9 de 11 ratios eran inexactos (siempre por debajo del real; el veredicto AA no cambia). Botón deshabilitado: 3.01:1 (exento de AA). Nota de revisión añadida; original en `e1d774f`.
- QA independiente **preparado, no ejecutado** (`tests/triad/ALT-TRIAD-001-qa-request.md`). **La triada NO está aprobada.** Quien corrigió los ratios (Claude, autor del brief) no puede revisarlos.

## 11. Controles: resumen final
| Estado | Controles |
|---|---|
| **PASS** | `npm run check`; OmniRoute solo en loopback y con autenticación; LAN inaccesible; sin otro proceso expuesto; respaldos con hash; Blender render Cycles CPU; Playwright MCP; routing 17/17; skills:audit sin regresión |
| **FAIL / corregido** | Preflight OmniRoute (falso negativo) → corregido; sondeo de Blender (timeout) → corregido; ratios de contraste inexactos → corregidos; `omniroute stop` inefectivo → mitigado a mano |
| **FAIL abierto** | EEVEE headless en esta GPU; `visual:preflight` vía npm informa `npm: NOT_FOUND`/`Python 3: ERROR` (falso negativo no corregido) |
| **BLOCKED** | Codex (sin créditos): QA independiente; Supermetrics/Klaviyo/Windsor (auth); plugin marketing duplicado |
| **PENDIENTE** | Aprobar MCP playwright/chrome-devtools; proveedor aprobado para inferencia en OmniRoute; identidad de Palacio Mental y Claude Red; Headroom; firewall Public; `altiora-shared` apunta a carpeta antigua; ciclo con cliente real |
