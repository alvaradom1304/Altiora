# Organización de Altiora · 2026-11-10

Responsable: claude (coordinador/implementador, único escritor empresa). Raíz y remoto: `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado`, `alvaradom1304/Altiora`, rama `main` (verificado con `git rev-parse --show-toplevel` y `git remote -v`). `modelo_planeado`: sonnet · `modelo_efectivo`: null/no_observado (sin recibo del proceso exacto). Continúa [CIERRE-OPERATIVO-20261110](CIERRE-OPERATIVO-20261110.md); no repite sus auditorías. Cuatro resultados por separado:

| Resultado | Veredicto |
| --- | --- |
| Cierre operativo (informe anterior) | **FAIL limitado**, sin cambio: falta QA independiente |
| Organización (este informe) | **PASS** con QA independiente de Antigravity (6/6), alcance limitado |
| Graphify MCP nativo | **Consultado con éxito tras `/mcp` Reconnected**; luego volvió a aparecer `CONNECT_TIMEOUT` al reabrir la sesión (ver abajo) |
| QA independiente (AGY) | **PASS 6/6** ([informe del revisor](ORGANIZACION-ALTIORA-QA-20261110.md)) |

## Cambios propios

- Creado [MAPA-ALTIORA.md](MAPA-ALTIORA.md): tres raíces con remoto, cuatro áreas (Dirección · Análisis · Producción · Operación) enlazadas a fuentes existentes, empresa/clientes/laboratorio con estado, guía de encargo y traspaso, cobertura del grafo. No mueve ni duplica documentos, no crea repos, orquestadores ni carpetas.
- Enlaces añadidos (una línea cada uno): `AGENTS.md` (primera línea; archivo con cambios previos ajenos sin commit, conservados), `README.md`, `docs/altiora-business/INICIO.md`, sección «Organización» en `ESTADO-ACTUAL.md`.
- Enlaces del mapa comprobados: 0 rutas faltantes.
- Respaldo: no hubo movimientos ni borrados; los cambios son aditivos y reversibles con `git diff`. `.mcp.json` ya contenía el servidor `graphify` (cambio previo sin commit): no lo toqué.

Cambios ajenos conservados, sin tocar: `.claude/settings.json` (`enabledPlugins codex`), `.mcp.json`, `.graphifyignore`, `package.json`, scripts nuevos, `projects/tilicheros/*` sin versionar, `out/`, `.references/`, `reparar-antigravity.bat`, borrados de `.pyc` en el índice.

## Comprobaciones

| Comprobación | Resultado |
| --- | --- |
| `npm run check` (log en archivo, código leído de `check2.exit` escrito tras npm) | **exit 0**; `check:handoff` PASSED. Un intento anterior quedó interrumpido por cierre de terminal en `routing:eval` y no cuenta |
| `npm run altiora:ready` | LISTO; elegibles claude y antigravity; HTTP 200 en 20128 y 20129; Codex `paused-user-quota` |
| `orca-coordinator preflight` | `launchReady/returnReady/executeReady` true; terminal propio conectado y escribible |
| Router con Codex pausado (`route`, tres dominios, `files` indicados) | `ux-copy-frontend`→claude; `engineering-security-qa`→claude (`fallbackUsed`, Codex omitido por pausa); `immersive-3d-motion`→antigravity. Sin `files` el router rechaza («sin propiedad de archivos») |
| Contexto/identidad | raíz empresa, remoto `alvaradom1304/Altiora`; Desktop/altiora y `client-central-del-queso` → `la-central-del-queso` |

**Divergencia de dominios corregida de forma mínima:** `.altiora/coordinator.json` usa `ux-copy-frontend`, `engineering-security-qa`, `immersive-3d-motion`; `team/ROUTING.md` usa otros nombres. Autoridad: ROUTING primero. Se añadió `domainAliases` (config) y su lectura en `route()` (`scripts/orca-coordinator.mjs`, solo si el dominio pedido no existe): `brand-copy-frontend`→`ux-copy-frontend` e `immersive-3d-qa`→`immersive-3d-motion`, únicos equivalentes con la misma cadena de IAs. El resultado incluye `requestedDomain`. `strategy-finance-backend` (ROUTING: codex primero) y `cloud-data-engineering` **no** tienen equivalente: siguen devolviendo `abstain` «dominio desconocido» en el coordinador, y los cubre `team/ROUTING.md`. Tradeoff: no se forzó una correspondencia con roles distintos ni se cambió ninguna cadena o política. Prueba nueva en `orca-coordinator.test.mjs`; `npm run coordinator:test` **exit 0, 52/52** (antes 51). Respaldo de los tres archivos en `.altiora/backups/*.20261110-pre-aliases`. `altiora:ready` LISTO tras el cambio. No se repitió `npm run check` completo (los cambios no tocan catálogo ni documentos que valida).

## Graphify MCP

- **Antes del reinicio de esta sesión (VERIFICADO):** herramientas nativas `mcp__graphify__graph_stats` y `query_graph` devolvieron 21.510 nodos / 24.557 aristas, commit `e438b3a`, y nodos de `scripts/orca-coordinator.mjs`, `altiora-ready.mjs`. Configuración: `.mcp.json` → `graphify-mcp.exe` (v0.9.100, instalado el 2026-11-01), grafo `…/graphs/altiora-20261110b/graphify-out/graph.json`, `GRAPHIFY_BACKEND=none`. Sin dependencias nuevas. *Nota 2026-11-11: registro histórico; `.mcp.json` apunta ahora al grafo único `graphs/altiora` (ver [MAPA-ALTIORA](MAPA-ALTIORA.md)).*
- **Conexión actual (VERIFICADO):** el arranque inicial dio `CONNECT_TIMEOUT` (30 s, con `npm run check` cargando la CPU; `initialize` manual tardó 16,8 s). Tras `/mcp` → «Reconnected to graphify» (acción del usuario, sin reiniciar), la herramienta nativa `mcp__graphify__graph_stats` devolvió 21.510 nodos / 24.557 aristas / 792 comunidades, commit `e438b3a`. Una sola consulta; sin cambios de configuración por mi parte. Después, al retomar la sesión, el cliente volvió a reportar `CONNECT_TIMEOUT`: la conexión es intermitente (arranque lento del grafo de 14 MB) y debe reconectarse con `/mcp` cuando falle; no se acredita conexión permanente ni de otras IAs.
- **Cobertura REAL:** solo código y datos (`--code-only`). Incluye scripts nuevos; **no** incluye Markdown operativo (`ESTADO-ACTUAL`, `ROUTING`, `INICIO`: 0 nodos) ni `projects/`. El índice documental es [MAPA-ALTIORA](MAPA-ALTIORA.md) más los enlaces; no se prometen todos los documentos. Otras IAs: no verificado.

## QA independiente (Antigravity)

**PASS en los 6 criterios, alcance limitado.** Informe propio del revisor: [ORGANIZACION-ALTIORA-QA-20261110](ORGANIZACION-ALTIORA-QA-20261110.md). Revisor nuevo, solo lectura salvo su informe, sin reaprovechar identidades anteriores: run `run_6cf90154847a`, task `task_5d90ad56aeb4`, dispatch `ctx_774871cc073a`, terminal `term_09a5e197-4615-4d8e-b414-339f7b105a9c`; `worker-show` confirma `succeeded/settled` (comprobado por mí). Modelo efectivo del revisor: null/no_observado (sin recibo; el informe cita «Gemini 3.8 Flash» solo como planeado).

- Los dispatches anteriores `ctx_6deaec87546a` y `ctx_0bec7f3905ed` (login) siguen `failed` y quedan como historial; no se reutilizaron.
- Pruebas que reportó el revisor: `node --test scripts/orca-coordinator.test.mjs` exit 0 (47 pass) y `npm run coordinator:test` exit 0 (52 pass; combina coordinador y `altiora-ready`). Mi frase previa «52/52 (antes 51)» se refiere a esta cifra combinada.
- Un auxiliar `check_secrets.js` del revisor estaba en su scratch fuera del repo (indicado por el usuario); no se borró y no hay copia en el repo.
- Límites: el PASS cubre solo los archivos y cambios de este encargo, no el cierre operativo previo, ni la web/clientes, ni la cuota o autenticación futuras. El revisor leyó el informe antes de este cierre; la sección de QA se actualizó después con su resultado, sin cambiar el resto.

## Acciones humanas concretas

1. Si Graphify vuelve a dar timeout: `/mcp` → reconectar solo `graphify` (o subir el tiempo de arranque en tu configuración de usuario, no tocada).
2. Decisiones pendientes: commit del trabajo local (todo sigue **sin commit**), si `enabledPlugins codex` en `.claude/settings.json` es intencional, y cuándo reactivar Codex (pausado por cuota).
3. Cobertura del grafo: parcial (solo código); los documentos se navegan desde el [mapa](MAPA-ALTIORA.md).
