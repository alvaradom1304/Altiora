# PREAMBRA OS — Auditoría y certificación de Claude Code como orquestador (2026-11-22)

**Veredicto:** NIVEL 3 (multi-IA, mínimo: Claude coordina y Codex trabaja vía Orca) · ESTADO **PARTIAL**. Escala: 1 configurado · 2 operativo · 3 multi-IA · 4 comercial.

El piloto `Run → Task → Worker → Resultado → Revisión → Cierre` se completó con IDs reales tras la autorización del fundador (ver «Piloto Orca» más abajo). El estado sigue siendo PARTIAL porque:
- fue una sola tarea de lectura;
- Antigravity no se probó;
- el piloto constructor + revisor con escritura sigue pendiente.

## Piloto Orca (2026-11-22, autorizado por el fundador)

| Paso | ID real / evidencia | Resultado |
|---|---|---|
| Coordinador | Terminal `term_62a30b5d-4305-48c3-9be5-dcadbf157ccc`, creada en este worktree; su `ORCA_TERMINAL_HANDLE` coincide | PASS |
| Run | `run_9b4ceb61a534` (`run-create` sin `--from`) | PASS |
| Task | `task_2642ce03f9f9`, sintética, solo lectura, estado `ready` | PASS |
| Worker | `worker-start --agent codex --model gpt-6.1-sol --effort low` → dispatch `ctx_36da41c4331a`. El recibo de Orca confirma `effective`: codex / gpt-6.1-sol / low | PASS |
| Resultado | `worker_done` `msg_2433c2185144`, outcome `succeeded` | PASS |
| Revisión (Claude) | Las tres respuestas coinciden con la fuente. El texto del error solo existe en esta rama, así que el worker leyó este worktree. `git status` limpio: no modificó nada | PASS |
| Cierre | Dispatch `completed`; `worker-release` → `released`, transcripción archivada, terminal del agente cerrada; terminal coordinadora cerrada | PASS |

Hallazgo: fuera de una terminal de Orca, Orchestration responde `no_active_sender_terminal`. El coordinador debe ser una terminal de Orca, y su handle es la única identidad válida para `--from`. Esto confirma la corrección P0.

Rama: `claude/preambra-os-certificacion`, creada desde `origin/main` `256bdfc` en un worktree aislado (`C:/Users/Usuario/wt-preambra-cert`). El checkout canónico tenía cambios ajenos sin confirmar y no se modificó.

Estados: PASS · FAIL · UNKNOWN · NOT_RUN · NOT_APPLICABLE · NOT_VERIFIED.

## A. Auditoría (fase 0, preflight de solo lectura)

| Componente | Configurado | Detectado | Autenticado | Probado | Riesgo | Acción |
|---|---|---|---|---|---|---|
| Git / worktree | PASS (`origin` HTTPS) | PASS: 40 worktrees; `main` local 4 commits detrás de `origin/main` | NOT_APPLICABLE | PASS | Medio: muchos worktrees y el canónico está sucio | Trabajar siempre en un worktree desde `origin/main` |
| Node / npm / Python | PASS | v24.21.0 / 11.19.0 / 3.12.10 | NOT_APPLICABLE | PASS (`npm run check`) | Bajo | — |
| Claude Code | PASS | 2.1.309 | PASS (`claude auth status`: claude.ai) | PASS (invocó el subagente `qa-reviewer`) | Bajo | — |
| Codex CLI | PASS | 0.167.0-alpha.3.2 (alpha) | PASS («Logged in using ChatGPT») | PASS (revisión QA de este diff, solo lectura) | Medio: versión alpha | Fijar `-m`/esfuerzo en cada delegación |
| Antigravity (`agy`) | PASS | 1.4.12 | UNKNOWN (el CLI no expone estado de login) | NOT_RUN en esta sesión | Medio | Probar con una tarea 3D sintética cuando haga falta |
| Orca CLI | PASS | 1.4.261 | NOT_APPLICABLE | PASS tras abrir la app (`runtime ready`). Antes había dado `runtime_unavailable` con la app cerrada | Medio | Coordinar siempre desde una terminal de Orca |
| `gh` | PASS | 2.103.3 | PASS (scopes repo, workflow, read:org, gist) | PASS | Bajo | — |
| Hook `SessionStart` | PASS | PASS | NOT_APPLICABLE | PASS (payload sintético → contexto inyectado) | Bajo | — |
| Hook `PreToolUse` | PASS | PASS | NOT_APPLICABLE | PASS (`.env` → `deny`; `README.md` → permitido) | Bajo: la ruta apunta al canónico, pero el guard compara nombres base, así que protege también los worktrees | Ninguna |
| MCP `altiora-after-effects` | PASS (`.mcp.json`) | PASS | NOT_APPLICABLE | FAIL: `npm run adobe:check` → `aerender.exe` ENOENT | Medio | Fallback sin AE; marcar `NOT_VERIFIED` |
| MCP `chrome-devtools` | PASS | PASS (1.12.0 en `.altiora-tools`) | NOT_APPLICABLE | NOT_RUN (pendiente de aprobar en el worktree nuevo) | Bajo | Aprobar solo cuando se use |
| MCP `metricool` | PASS (HTTP) | PASS | UNKNOWN (pendiente de aprobación; no se conectó la cuenta) | NOT_RUN | Bajo | No conectar sin autorización |
| Notion (Plan maestro) | PASS (conector) | PASS: página «Plan maestro» localizada | PASS | PARCIAL: solo búsqueda; «Guía v0.0.6» no encontrada por título; «Metodología» no leída | Bajo | Leer bajo demanda |
| `.altiora/orchestration.json` | PASS | PASS | NOT_APPLICABLE | FAIL histórico: `consumer_fenced` (2026-11-01) | Alto: `VERIFIED_READY` es de hace tres semanas | No tratarlo como estado vivo (ver C) |

## B. Matriz de capacidades

| Capacidad | Diseñado | Implementado | Probado aquí | Evidencia |
|---|---|---|---|---|
| Claude descubre agentes de `.claude/agents` | Sí | Sí | **PASS** | `claude -p` en el worktree invocó `qa-reviewer` → `QA-PING-OK` (sesión `c13934d4…`, agente `a417fd8b5e69021ca`) |
| Router V2 A/B/C/D | Sí | Sí | **PASS** con un defecto corregido | A: errata; B: formulario + seguridad (riesgo crítico); C rechazado por colisión de rutas (`components` frente a `components/3d`), comportamiento correcto; D: proyecto integral |
| Revisor independiente por traspaso | Sí | Defectuoso | **FAIL → PASS** | En D, el flujo de Codex salía con `reviewer=None` sin aviso; corregido |
| Delegación Claude → Codex por terminal | Sí | Sí | **PASS** | `codex exec -s read-only` revisó el diff (veredicto abajo) |
| Delegación a Antigravity | Sí | Sí | NOT_RUN | Funcionó en la sesión de origen (sin recibo propio aquí) |
| Orca supervisado (Run/Task/Worker) | Sí | Sí (defecto `--from` corregido) | **PASS** (una tarea de lectura) | `run_9b4ceb61a534` / `task_2642ce03f9f9` / `ctx_36da41c4331a` |
| Equipos experimentales de Claude | — | — | NOT_APPLICABLE | No se habilitaron (prohibido por el encargo) |
| After Effects | Sí | Puente | FAIL | `aerender` ausente |

**Agentes (32 en `.claude/agents/`).**
- 22 se generan desde `team/` con `npm run agents:build`: la comprobación pasa.
- Los otros 10 (`altiora-os-*` y `altiora-creative-analyst`) se copian a mano desde `altiora-os/agents/`. Una heurística de palabras clave (SUPUESTO, no revisión humana) les detecta huecos de **entradas, datos ausentes y cierre**.
- Ninguno declara `model`: todos heredan el modelo de la sesión. La regla de «modelo grande solo en high» no se aplica a nivel de agente.
- Solapamientos que confunden la selección automática:
  - `qa-reviewer` / `altiora-review` / `altiora-os-qa`;
  - `market-intelligence-director` / `altiora-research` / `altiora-os-research`;
  - `business-strategist` / `altiora-os-strategy`.

  No se consolidan sin decisión del fundador (G).

**PR #100 (seis agentes) — dictamen: INTEGRABLE.**
- CI en verde en Ubuntu y Windows (commit `7b4677c`).
- En local pasan `build-agents --check` y `build-antigravity --check` (22 agentes, 355 skills) y `verify-catalog`.
- Las 72 skills referenciadas por los seis agentes existen en `skills/`.
- `git merge-tree` contra el #101 no da conflictos.
- Edita fuentes (`team/agents.json`, `team/roles/`) y adaptadores regenerados.
- Pendiente: invocación real de cada uno de los seis agentes (solo se probó `qa-reviewer`).
- No se fusionó.

## C. Informe de correcciones (P0/P1)

1. **P0 — `consumer_fenced` (Orca)** en `scripts/orca-dispatch.py`.
   - **Causa:** `ensure_orca_run` reutilizaba el Run guardado o el de la primera terminal viva y pasaba su handle como `--from`. Orca atesta la terminal que llama y solo la deja actuar como sí misma. El registro lo confirma: la llamada estaba atestada como `term_ce98…` y pidió actuar como `term_d096…`. Además, el run guardado (`run_b9a2…`) no coincide con el usado (`run_c4e4…`).
   - **Corrección:** se reutiliza solo un Run cuyo coordinador sea `ORCA_TERMINAL_HANDLE`. Si no hay, se crea sin `--from`, y `task-create` solo envía `--from` con el handle propio.
   - **Prueba de regresión:** `OrcaIdentityFencingTest`.
   - **Límite:** el mock comprueba argumentos, no el rechazo real de Orca. Falta repetirlo con Orca vivo.
2. **P1 — revisor ausente por traspaso** en `scripts/preambra_v2_routing.py`.
   - **Corrección:** cada traspaso B/C/D recibe un revisor distinto de su dueño. Si no queda ninguno, se añade un riesgo explícito, y `validate_contract` impide `DONE` sin `reviewer` ni `human_review` registrado.
   - **Pruebas:** dos nuevas.
3. La prueba nueva escribió por error en `.altiora/orchestration.json`. Se restauró desde HEAD y ahora la prueba usa una ruta temporal. El archivo queda intacto en el PR.
4. Runbook: identidad en Orca, arranque diario y autoridad de continuidad (sección E).

QA independiente (Codex `gpt-6.1-sol`, esfuerzo low, solo lectura): «ACEPTAR CON CORRECCIONES».
- ALTA y MEDIA (DONE sin revisor): corregidas.
- BAJA (el mock no reproduce el rechazo): aceptada como límite.
- Compatibilidad en modo A: no aplica, porque `reviewer_candidate` ya era `None` en A.

## D. Certificación

| Grupo | Alcance (SUPUESTO: sin el texto literal del prompt) | Resultado |
|---|---|---|
| A — Entorno | Preflight, versiones, auth, hooks, MCP | PASS con FAIL en Orca runtime y AE |
| B — Calidad del repo | `npm run check` en `origin/main` (4 min 32 s) | PASS (código 0) |
| C — Router y despachador | Suites `routing:v2:test` (20) y `orca:test` (7), `orca:smoke` | PASS tras corregir |
| D — Orquestación real | Claude → subagente: PASS. Claude → Codex por terminal: PASS. Piloto Orca con worker Codex: PASS. Antigravity y piloto con escritura: NOT_RUN | PARCIAL |
| E — QA independiente | Revisión de Codex sobre el diff | PASS (correcciones aplicadas) |

## F. Guía de primer uso — ejemplo: estudio de mercado de Currenda (revisado)

Datos sintéticos. No tocar `C:/Users/Usuario/Currenda` sin el encargo del sprint.

1. Clasificar el encargo: `python scripts/orca-dispatch.py --json --entrypoint claude "Estudio de mercado de Currenda: demanda, competencia y precios en Costa Rica"`. Se espera el modo B: constructor y revisor.
2. Constructor: subagente `market-intelligence-director`, con las skills que le asigna el PR #100, una vez fusionado. Entrada: brief de Currenda y preguntas cerradas. Salida: fuentes fechadas, VERIFICADO / SUPUESTO / NO SÉ y un top de oportunidades con su método.
3. Revisor distinto: `qa-reviewer`, o Codex en solo lectura con `-m` y esfuerzo explícitos. Bloquea toda cifra sin fuente.
4. Cierre: entregable en `projects/<cliente>/`, `npm run check`, PR. El checkpoint no se actualiza hasta la fusión.
5. Límites: no contactar personas, no gastar, no publicar. Lo que el estudio no pueda verificar se queda en NO SÉ.

## G. Pendientes y aprobaciones (decide el fundador)

1. Fusionar el PR #100 (dictamen favorable) y el #101 (gobierno). No se fusionó nada.
2. Revisar y fusionar el PR de esta rama (correcciones P0/P1 y runbook).
3. ~~Piloto Orca de lectura~~: hecho y con IDs registrados. Siguiente paso, que requiere autorización: piloto constructor + revisor con escritura en un worktree aislado y, si aporta valor, un worker de Antigravity para una tarea 3D.
4. Decidir si se consolidan los agentes duplicados (lista en B) y si se fija `model` por agente.
5. `.altiora/orchestration.json`: decidir si se marca su `runtime` como histórico. No se modificó.
6. PR #81: el CI del arreglo de Windows `d49dc37` ya está en verde y es fusionable (antes constaba como no verificado). Revisar #86 y el resto de PR abiertos (16 en total).
7. After Effects: instalar o apuntar `ALTIORA_AERENDER` solo si un cliente lo pide.

Costos observados:
- `claude -p` con Haiku: US$0,0199, según el propio CLI. Es un equivalente estimado, porque la cuenta es claude.ai.
- Codex: dentro de la cuota de ChatGPT; el CLI no informó el importe.
- Tokens de esta sesión orquestadora: sin medir.
- No hubo gastos de servicios ni de facturación.
