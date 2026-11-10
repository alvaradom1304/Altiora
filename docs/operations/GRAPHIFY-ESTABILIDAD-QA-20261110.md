# QA Independiente (Delta y Validación en Frío): Estabilidad de Sesiones Orca y Timeout Graphify MCP · 2026-11-10

- **Rol:** Antigravity (coordinador de sub-encargos supervisados y revisor QA independiente; no implementó cambios de configuración).
- **Workspace (raíz efectiva):** `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado` (`git rev-parse --show-toplevel`).
- **Repositorio saneado:** `github.com/alvaradom1304/Altiora` (`git remote -v`).
- **Run / Tasks / Dispatches propios:** `run_6cf90154847a` · `task_28f72b2c3bf8` (`ctx_fc374bd19044`) y `task_de959bb461ae` (`ctx_4b480ea5c356`) · coordinador raíz retomado en `term_dcb91772-3880-41e9-9cb8-f34149dd9404` (`consumer_generation: 2`).
- **Modelo planeado (este agente):** Gemini 4 Argon (High) · **Modelo efectivo:** `null` (`estado_modelo: no_observado`, `procedencia_modelo: null`; recibos Orca reportan `effective.model: null`).
- **QA previo intacto:** [`ORGANIZACION-ALTIORA-QA-20261110.md`](ORGANIZACION-ALTIORA-QA-20261110.md) conservado sin modificaciones (**PASS** intacto).
- **Veredicto QA final (delta + validación en frío):** **PASS** (implementación acotada en [`.claude/settings.json`](../../.claude/settings.json), opción/unidades `MCP_TIMEOUT` verificadas en binario local `claude.exe` 2.1.322, retención de sesión con `--keep-open` comprobada y arranque en frío de nueva sesión de Claude verificado en [`GRAPHIFY-ARRANQUE-FRIO-20261110.md`](GRAPHIFY-ARRANQUE-FRIO-20261110.md) con descubrimiento nativo y llamada real a `mcp__graphify__graph_stats`).

---

## 1. Diagnóstico con Recibos: Cierres Automáticos de Claude y Ciclo de Vida Orca

Se inspeccionaron en modo solo lectura `orca orchestration worker-list --json --full`, `worker-show --json --full`, `run-show --json --full` e `inbox --json --full` sin tocar registros ni procesos:

### A. Cierre automático por ciclo de vida de workers Orca (`resource_release`) — DEMOSTRADO CON RECIBOS
1. **Regla del runtime Orca (`orca orchestration worker-start --help`):**
   - *"Finished workers close on their own unless started with `--keep-open`"*.
   - Además, `buildWorkerStartArgs` en `scripts/orca-coordinator.mjs` (línea 403) invoca `worker-start` sin `--keep-open`.
2. **Recibo `ctx_8642b462f020` (`task_6dff4188f48b`, `run_78b0ec6e4cc8`, terminal `term_888d3401-2e33-4d0d-82dc-c2fd40c8941b`):**
   - Iniciado sin `--keep-open` (`retainedReason: null`).
   - Al emitir `worker_done` (`msg_9add3ee062a0`, `completedAt: "2026-11-10T15:03:05.837Z"`), Orca ejecutó inmediatamente la liberación automática del recurso `wtr_d3badab12251`:
     - `releaseState`: `"released"`, `ownershipState`: `"released"`
     - `releaseRequestedAt`: `"2026-11-10 15:03:05"`, `releaseCompletedAt`: `"2026-11-10 15:03:06"`
     - `projection.liveness`: `{"verdict": "exited", "source": "resource_release"}`
     - `terminal.exitCause`: `{"kind": "operator_close"}` (etiqueta interna del cierre de pestaña ejecutado por `resource_release`).
3. **Recibo `ctx_242e7b2d505a` (`task_9bf4d4d26fba`, `run_3345733992b6`, terminal `term_f9c77595-bb67-4fa8-a373-bf86e1308683`):**
   - Mismo comportamiento exacto: recurso `wtr_4f81f41d8655` con `retainedReason: null`, `releaseState: "released"`, `releaseRequestedAt` / `releaseCompletedAt`: `"2026-11-10 07:35:16"`, `projection.liveness`: `{"verdict": "exited", "source": "resource_release"}`.

### B. Follow-up automático bloqueado en prompt MCP (`ctx_12cd4c7ec6b4`) — DEMOSTRADO CON RECIBOS
- **Recibo `ctx_12cd4c7ec6b4` (`task_2bd3d79d25b8`, `run_78b0ec6e4cc8`, terminal `term_79068dd0afd99d8559c26120cc55c1bf`):**
  - Creado automáticamente a las `2026-11-10 15:03:06` (`followUpOf: "ctx_8642b462f020"`) porque existía un correo de recuperación en cola (`msg_2c5eb897b16f`) cuando `ctx_8642b462f020` terminó.
  - Su `terminal.preview` muestra que quedó detenido en el diálogo interactivo de Claude Code: `3 new MCP servers found in this project / Select any you wish to enable`, generando `turn_unobserved` (`msg_followup_cff4bdbf623ef5463ebd3c5e`).
  - Cerrado a las `2026-11-10T19:06:33.464Z` con `stage: "process_exited"`, `terminationReason: "operator_close"`, `liveness: {"verdict": "exited", "source": "execution_host"}`, `releaseState: "not_requested"`.

### C. Terminales coordinadores no-worker (`term_c7d6ebe6-731c-4866-a123-f4a2f653d366` y `term_875692eb-6b99-4599-bf83-108d4ed07855`) — CAUSA NO DEMOSTRADA
- Las sesiones abiertas como coordinador (no lanzadas como worker mediante `worker-start`) no generan recursos `wtr_*` en `worker-list` (`removedWork.terminals: 0` en `run-show`).
- En [`ORGANIZACION-ALTIORA-20261110.md`](ORGANIZACION-ALTIORA-20261110.md) (línea 25) consta que un intento previo se interrumpió por cierre de terminal durante `npm run check` (`routing:eval`). **Sin recibo de `terminalResource`, la causa de los cierres de terminales coordinadores no-worker se mantiene explícitamente como NO DEMOSTRADA y no se les atribuye `resource_release`.**

---

## 2. Fase 1: Delegación Supervisada (`ctx_08838f5c9f2a`) y Revisión del Delta de Configuración

- **Worker de implementación:** `dispatchId: "ctx_08838f5c9f2a"`, `taskId: "task_16b6bf7fe965"`, `runId: "run_6cf90154847a"`, `terminal: "term_d3263606-0f00-4757-b917-55be70cfe408"`, lanzado con `--keep-open` (`keptOpen: true`).
- **Retorno (`worker_done`):** `msg_e66c5d9d1e74` (`outcome: "succeeded"`, `completedAt: "2026-11-10T19:42:01.283Z"`), informe [`GRAPHIFY-ESTABILIDAD-20261110.md`](GRAPHIFY-ESTABILIDAD-20261110.md).
- **Modelo del worker (`ctx_08838f5c9f2a`):** `modelo_planeado`: `claude-sonnet-5-5` · `modelo_efectivo`: `null` (`no_observado` en recibo Orca).
- **Retención con `--keep-open` verificada:** Tras `worker_done`, `terminalResource` (`wtr_5aad6b3025fc`) permaneció en `ownershipState: "owned"`, `releaseState: "retained"`, `retainedReason: "user_requested"`, `autoReleaseAt: null`, con el terminal `connected: true`, `writable: true`, `liveness.verdict: "live"`.

| Criterio Delta (`ctx_08838f5c9f2a`) | Comprobación Independiente | Resultado | Veredicto |
| --- | --- | --- | --- |
| **1. Opción y unidades en fuente local** | Inspección de solo lectura de `C:/Users/Usuario/.local/bin/claude.exe` (v2.1.322): verificada la función literal `function sd(){let _=i.MCP_TIMEOUT;return _&&_>0?Math.min(_,2147483647):30000}` y el mensaje `connection timed out after ${sd()}ms`. Unidad real: **milisegundos** (defecto `30000`). | Exacto. | **PASS** |
| **2. Ajuste mínimo y reversible en proyecto** | `git diff --no-index .altiora/backups/claude-settings.json.20261110-pre-mcp-timeout .claude/settings.json` muestra solo la adición de `"MCP_TIMEOUT": "60000"` en `env`. `JSON.parse` válido (`true`). Intactos `SLASH_COMMAND_TOOL_CHAR_BUDGET`, `hooks`, `enabledPlugins`, `.mcp.json` y configuración global. | Respaldo verificado en `.altiora/backups/claude-settings.json.20261110-pre-mcp-timeout`. | **PASS** |
| **3. Propiedad y ausencia de secretos** | `git status --short` confirma que solo se tocaron los archivos autorizados; `0` coincidencias de patrones `sk-`, `AIza`, `api_key`. | Cumple. | **PASS** |

---

## 3. Fase 2: Validación en Frío en Nueva Sesión de Claude (`ctx_72f05aa613b1`)

Con autorización del usuario y manteniendo inactiva la sesión previa (`term_d3263606-0f00-4757-b917-55be70cfe408`), se inició una única sesión nueva de Claude supervisada con `--keep-open` en modo solo lectura (salvo su informe [`GRAPHIFY-ARRANQUE-FRIO-20261110.md`](GRAPHIFY-ARRANQUE-FRIO-20261110.md)):

- **Recibo de arranque:** `dispatchId: "ctx_72f05aa613b1"`, `taskId: "task_3605bc9c96ab"`, `runId: "run_6cf90154847a"`, `terminal: "term_02e57333-b7a0-42e7-9523-d8f98a76f5ea"`, `keptOpen: true`, `dispatchedAt: "2026-11-10 19:55:44"`.
- **Recibo de retorno (`worker_done`):** `msg_9d7f3ccd90e9` (`delivery_b4d90265359a`, `outcome: "succeeded"`, `completedAt: "2026-11-10T19:57:23.743Z"`).
- **Modelo del worker (`ctx_72f05aa613b1`):** `modelo_planeado`: `claude-sonnet-5-5` · `modelo_efectivo`: `null` (`no_observado`; `effective.model: null` en `worker-show`).
- **Retención tras `worker_done` (`worker-show --dispatch ctx_72f05aa613b1 --json --full`):** `terminalResource` (`wtr_9df071acd6d8`) en `releaseState: "retained"`, `retainedReason: "user_requested"`, `autoReleaseAt: null`, `terminal.connected: true`, `liveness.verdict: "live"`.

### Verificación independiente contra el transcript real (`orca orchestration worker-read --dispatch ctx_72f05aa613b1 --json`)

| Comprobación en frío | Evidencia en transcript (`sourceIdentity: CDMoafpVButHTOEZ5PASukbBTwE56lMD`) | Tiempos observados (epoch ms del transcript) | Veredicto |
| --- | --- | --- | --- |
| **1. Variable pública `MCP_TIMEOUT` en proceso hijo** | `callId: toolu_01Q193D546Arad2DsZtSSMeW` (`node -e "console.log('MCP_TIMEOUT=' + process.env.MCP_TIMEOUT)"; echo "exit=$?"`) → salida literal: `MCP_TIMEOUT=60000` y `exit=0`. Sin exponer otras variables. | Llamada: `1794340587943` · Respuesta: `1794340604545` | **PASS** |
| **2. Descubrimiento nativo de `graphify` sin `CONNECT_TIMEOUT`** | 1.º `ToolSearch` (`toolu_019YNR8m5PkG2FYsAB1q5du3`): `"Some MCP servers are still connecting: graphify"` (sin fallo de timeout).<br>2.º `ToolSearch` (`toolu_01Jwqv7LkGVRYyZ8sGaHhQqu`): descubrió y cargó el esquema diferido de `mcp__graphify__graph_stats` sin diálogo de autorización adicional. | 1.º `ToolSearch`: `1794340589576` → `1794340612050`<br>2.º `ToolSearch`: `1794340615043` → `1794340616395`<br>**Tiempo de conexión MCP: no medido** (no se deduce desde `dispatchedAt` porque este incluye creación de terminal, arranque del CLI y operaciones previas; no consta en el transcript el instante exacto de inicio de conexión del servidor MCP). | **PASS** |
| **3. Única llamada nativa a `mcp__graphify__graph_stats`** | `callId: toolu_01AnHHqs7S3zcUfuR6KCkGaC` (`mcp__graphify__graph_stats`, `{}`) → salida literal:<br>`Nodes: 21510`<br>`Edges: 24557`<br>`Communities: 792`<br>`EXTRACTED: 99%`, `INFERRED: 1%`, `AMBIGUOUS: 0%`<br>`Built at commit: e438b3a684fdb578307edd00bbaa39e67a52d62e` | Llamada: `1794340618699` → Respuesta: `1794340621050` (**2,351 s** entre invocación y respuesta de la herramienta en el transcript). | **PASS** |
| **4. Alcance y solo lectura** | Único archivo creado por `ctx_72f05aa613b1`: [`docs/operations/GRAPHIFY-ARRANQUE-FRIO-20261110.md`](GRAPHIFY-ARRANQUE-FRIO-20261110.md). Sin handshakes stdio aislados, sin tocar `.claude/settings.json` ni `.mcp.json`, `0` secretos. | Creado: `1794340636013` → `1794340638208` | **PASS** |

---

## 4. Actualización de Límite Pendiente y Cierre

- **Límite pendiente resuelto:** La validación en frío que había quedado pendiente en la Fase 1 queda **VERIFICADA Y CERRADA (PASS)** según lo realmente probado en [`docs/operations/GRAPHIFY-ARRANQUE-FRIO-20261110.md`](GRAPHIFY-ARRANQUE-FRIO-20261110.md) y el transcript de `ctx_72f05aa613b1`: herencia de `MCP_TIMEOUT=60000` (`exit=0`), descubrimiento nativo de `mcp__graphify__graph_stats` y consulta nativa exitosa (además de la verificación nativa previa en Antigravity `ctx_fc374bd19044`).
- **Límites materiales permanentes (sin prometer ausencia de todo error futuro):**
  1. **Tiempo de conexión no medido y ausencia de atribución causal:** En `ctx_72f05aa613b1` el tiempo exacto de conexión de `graphify` **no fue medido** (no se deduce desde `dispatchedAt`, pues este incluye el arranque del CLI y otras operaciones previas). Asimismo, se trata de una única observación en frío sin grupo de control, por lo que **no se atribuye causalidad al cambio de timeout** ni se promete ausencia de todo error futuro.
  2. **Cierres de terminales coordinadores no-worker:** La causa de los cierres de pestañas coordinadoras no iniciadas como workers (`term_c7d6ebe6-731c-4866-a123-f4a2f653d366` y `term_875692eb-6b99-4599-bf83-108d4ed07855`) permanece **NO DEMOSTRADA** (sin recibo de `terminalResource`), a diferencia del cierre automático por `resource_release` demostrado con recibos para workers lanzados sin `--keep-open`.
  3. **Estado de sesiones al cierre:** Permanecen abiertos y en reposo los terminales retenidos (`term_09a5e197-4615-4d8e-b414-339f7b105a9c`, `term_d3263606-0f00-4757-b917-55be70cfe408` y `term_02e57333-b7a0-42e7-9523-d8f98a76f5ea`), con [`ORGANIZACION-ALTIORA-QA-20261110.md`](ORGANIZACION-ALTIORA-QA-20261110.md) intacto.
