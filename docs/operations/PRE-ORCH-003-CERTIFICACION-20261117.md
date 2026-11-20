# PRE-ORCH-003 · Certificación del runtime real · 2026-11-17

Responsable: Claude Code (coordinador). Rama: `feature/pre-orch-003-preflight-2026-11-17` desde `origin/main` `347f874`, en un worktree limpio (`C:/Users/Usuario/wt-preorch003`) para no tocar la copia canónica, que tiene 79 cambios locales sin commit y diverge de `origin/main` (1 commit local ECC `afaef46` y 7 commits remotos). `modelo_efectivo` del coordinador: null/no_observado.

Escala: **DISEÑADO → IMPLEMENTADO → PROBADO → OPERATIVO**. Nada sube de estado sin evidencia.

## 1. Preflight (VERIFICADO con comandos en la PC)

| Herramienta | Resultado |
| --- | --- |
| Git | 2.55.0.windows.5 |
| Node / npm | v24.21.0 / 11.19.0 |
| Python | 3.12.10 |
| Claude Code | 2.1.309 |
| Codex CLI | 0.167.0-alpha.3.2; `orca account list`: autenticación OAuth del sistema presente. **No se lanzó**: pausado por la persona fundadora por consumo |
| Antigravity (`agy`) | responde a `--help`; `agy models` lista 18 ids (Gemini 4 Argon/Hydrogen, Orchestrator, Gemini 3.8 Flash low/medium/high, Claude Opus/Sonnet 5.5, GPT-OSS 120B) |
| Orca | 1.4.261; `orca status --json`: app en ejecución, runtime `ready`, `connected` |
| Orca orquestación | `run-create`, `task-create`, `worker-start`, `worker-show`, `worker-read`, `check`, `gate-*` disponibles |

## 2. Router V2 (PROBADO, en el checkout `347f874`)

- `npm run routing:v2:test`: 11 OK. `npm run orca:test`: 5 OK. `npm run orca:smoke`: 4/4 PASS (`executed_agents=0`).
- Planes de los cuatro ejemplos del runbook: A, B, C (paralelo) y D (riesgo `elevated`), todos con contratos `PLANNED` y `model_observed: UNKNOWN`.

## 3. Etapa B · primera tarea real de Orca (PROBADO)

Requisito de Orca descubierto: toda orden de orquestación necesita la identidad de un terminal coordinador (`no_active_sender_terminal` sin ella). Se creó un terminal dedicado en el worktree limpio (`orca terminal create`, conectado y escribible) y se usó como `--from`. No se usó `ALTIORA_DISPATCH_EXECUTE` ni se saltó ninguna guarda.

| Campo | Valor |
| --- | --- |
| Run | `run_534259da3356` |
| Task / Dispatch | `task_569cc182ac40` / `ctx_1237a82432a8` |
| Agente / modelo / esfuerzo | claude / `claude-haiku-5-5` (recibo de Orca y autorreporte del worker) / low |
| Estado | `succeeded`, `exited` |
| Herramientas usadas | Read (runbook), Grep, Read (`preambra_v2_routing.py`), Bash solo para `orca orchestration send --type worker_done` |
| Salida recuperada | `worker-read --source transcript`; `worker_done` en el buzón del coordinador (`check --all`) |
| Archivos modificados | 0 (`git status --porcelain` vacío antes y después) |
| Verificación del coordinador | la cita `scripts/preambra_v2_routing.py:99-100` para el modo C es exacta |

## 4. Etapa C · traspaso a un revisor independiente (PROBADO, con 1 corrección)

| Campo | Valor |
| --- | --- |
| Run / Task / Dispatch | `run_534259da3356` / `task_5340340cea2f` / `ctx_32d32d74db54` |
| Agente / modelo pedido / esfuerzo | antigravity / `gemini-3.8-flash-low` (recibo de Orca); `model_observed` autorreportado: UNKNOWN / modo terminal |
| Contrato | solo el resultado del worker 1 y las rutas a revisar; sin la conversación del coordinador ni del worker 1 |
| Intento 1 | **falló**: la especificación multilínea llegó partida al TUI y el revisor pidió instrucciones. Orca escaló al coordinador: «Worker stopped without reporting» |
| Corrección 1 (de 2 permitidas) | instrucción de una sola línea (648 caracteres) enviada con `orchestration send --to dispatch:ctx_32d32d74db54` |
| Veredicto | `worker_done` «PRE-ORCH-003-QA PASSED»: confirma `preambra_v2_routing.py:93`, `:97-98` y `:99-100`; `files_modified: []` |
| Cierre | el proceso del revisor siguió vivo tras `succeeded`; se cerró su terminal con `orca terminal close` |

## 5. Etapa D · paralelismo aislado (NO EJECUTADA)

Requiere dos workers en worktrees nuevos (`--worktree new-child`) y un segundo ejecutor con cuota. Codex está pausado por consumo y no hubo autorización de gasto adicional. El router ya bloquea `--launch-workers` sin worktrees reales (`orca-dispatch.py`, prueba en `test_orca_dispatch.py`). Estado: DISEÑADO/IMPLEMENTADO en el plan, **no PROBADO** en runtime.

## 6. Etapa E · recuperación (PARCIAL)

| Fallo | Resultado | Estado |
| --- | --- | --- |
| Worker que termina sin `worker_done` | Orca envía `escalation` al coordinador con el último output; el coordinador corrigió con `send` | PROBADO |
| Modelo inexistente (`modelo-inexistente-preambra`, dispatch `ctx_12ee1d1ccab5`) | Orca **acepta el id y reporta `ready`**; Claude rechaza el modelo; Orca escala «Agent hit an error»; sin fallback silencioso; `worker-stop` → `stopped/exited` | PROBADO |
| Coordinador cerrado y reanudado | un terminal nuevo recibe `consumer_fenced` hasta `run-use --id <run>` | PROBADO |
| Cuota agotada, timeout, worker bloqueado en permiso, dependencias incompatibles | no provocados (coste o riesgo); el router rechaza paralelo con dependencias o colisiones en pruebas offline | NO PROBADO en runtime |

## 7. Hallazgos

1. **Identidad del coordinador:** una sesión de Claude Code fuera de Orca no puede orquestar sin `--from`; el terminal coordinador dedicado lo resuelve sin saltar protecciones.
2. **`worker-read` recorta bloques largos (~1.200 caracteres), también con `--full`.** Un contrato JSON largo llega cortado y no se puede parsear. Contratos de traspaso: cortos (<1.000 caracteres) o escritos en un archivo de artefacto.
3. **Codificación en terminal de Antigravity:** los acentos se ven como `Ã³` en la salida de terminal (UTF-8 leído como Latin-1). Afecta la legibilidad del registro; no se comprobó si afecta al razonamiento.
4. **Router (CORREGIDO en esta rama):** `decide_mode` proponía `codex` como revisor siempre que el líder no fuera Codex, sin consultar disponibilidad. Ahora acepta `unavailable` (`--unavailable` o `PREAMBRA_UNAVAILABLE_AIS`), elige el revisor en orden codex → claude → antigravity saltando al líder y a las no disponibles, y exige revisión humana si no queda ninguno. Sin lista, el comportamiento es el anterior. 7 pruebas nuevas en `test_preambra_v2_routing.py` (18/18 OK).
5. **Clasificación heurística:** «Formatear un resumen» se asigna al stream `codex`/`strategy-finance-backend`, aunque el modo A corrige el líder a la IA de entrada (`:117-118`).
6. **Orca no valida el id de modelo antes de lanzar.** El router debe pasar solo ids comprobados (`agy models` para Antigravity; ids aceptados por Claude Code) y el coordinador debe vigilar escalaciones: el estado `ready` no prueba que el worker esté trabajando.
7. **Workers en modo terminal (Antigravity):** las instrucciones deben ir en una línea; el JSON devuelto perdió las comillas al pasar por la terminal. Para contratos estructurados conviene el modo estructurado (Claude) o un archivo.
8. **Terminales vivos tras terminar:** cerrar explícitamente terminales de coordinador y de workers en modo terminal para no dejar procesos ociosos.

## 8. Estado por componente

| Componente | Estado | Evidencia | Pendiente |
| --- | --- | --- | --- |
| Router V2 | PROBADO (plan) | 18 + 5 pruebas, smoke 4/4; revisor según disponibilidad declarada | la disponibilidad la declara el operador; no se detecta sola |
| Claude Code | PROBADO como worker | `ctx_1237a82432a8` succeeded, `claude-haiku-5-5` | probar sonnet/opus solo cuando una tarea lo justifique |
| Codex | IMPLEMENTADO, no lanzado | CLI 0.167.0-alpha.3.2, OAuth presente | reactivar solo si la persona fundadora lo autoriza |
| Antigravity | PROBADO como revisor | `ctx_32d32d74db54` PASS tras 1 corrección | modo estructurado o instrucciones de una línea |
| Orca | PROBADO (Run/Task/worker/inbox/escalación) | `run_534259da3356`, 3 dispatches | validación de modelo; liveness de terminales |
| Delegación multi-IA | PROBADO (B: constructor + revisor) | Etapas B y C | no es OPERATIVO hasta repetirlo en una tarea de cliente |
| Worktrees | IMPLEMENTADO | worktree limpio registrado en Orca | Etapa D no ejecutada |
| QA independiente | PROBADO en una entrega | veredicto del revisor contrastado por el coordinador | QA empresarial no aplica a esta prueba |
| Seguridad | PROBADO en lo ensayado | 0 archivos modificados; sin `ALTIORA_DISPATCH_EXECUTE`; sin fallback silencioso | permisos de worker ante escrituras no ensayados |
| Continuidad | IMPLEMENTADO | este documento y `continuity/checkpoint.json` | sincronizar la copia canónica (diverge de origin) |
| Costos | NO MEDIDO | 3 workers baratos (Haiku low, Flash low; uno falló sin trabajo) | Orca y los CLI no expusieron tokens ni costo en esta prueba |

**Preparación operativa (escala 0–10 de PREAMBRA-MULTI-AI-ORCHESTRATION):** Claude 10/10 (instrucciones, documentación, test de routing, invocación real, prueba con handoff/QA); Antigravity 10/10 con la reserva del modo terminal; Codex 6/10 (sin invocación real ni handoff en esta prueba). Puntuación de preparación, no de calidad de modelo.

**DoD de la directiva:** cumplidos 1, 2, 4, 5, 6 y 9 (parcial); parciales 3, 7, 8 y 11; pendientes 10 (piloto de 12 tareas) y 12 (procedimiento de cliente nuevo). El sistema **no** se declara OPERATIVO.
