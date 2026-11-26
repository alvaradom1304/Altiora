# PREAMBRA OS — LEAN-first y orquestación multi-IA V3 (2026-11-26)

Estado: **IMPLEMENTADO en la rama `feat/preambra-lean-v3`, PROBADO localmente, sin fusionar ni publicar.** Parte de `feat/lean-profile-router` (`99319cf`).
Fuentes únicas: perfiles y seguridad en `team/profiles/profiles.json`; reglas de redacción LEAN en `team/profiles/lean.md`; lanzador `scripts/lean_run.py`; riesgo en `scripts/preambra_v2_routing.py`.

## Qué cambia
- **Lanzador con preflight obligatorio** (`--check` / `--dry-run` sin consumo). Bloquea (exit 2) si: el proyecto no coincide con el remote o se añade una carpeta de otro proyecto; el esfuerzo está fuera de perfil; se pide ADVANCED sin `--reason`; la tarea tiene riesgo crítico sin `--approved-risk`; faltan reglas de denegación o presupuesto; hay una bandera prohibida; se detecta un ciclo o una re-delegación (`PREAMBRA_DELEGATION_CHAIN`, profundidad 1); se intenta una tercera revisión del mismo `--task-id`.
- **Seguridad en LEAN:** `--safe-mode` apaga todos los hooks, incluido el guard `PreToolUse`. Las denegaciones de `security.deny_tools` se pasan siempre con `--disallowedTools`, y LEAN suma red.
- **Multi-IA:** orden de proveedores por perfil, respaldo si uno no está instalado, hasta 2 reintentos. Codex corre en `read-only` y Agy en `plan` salvo `--allow-write`.
- **Riesgo:** detecta imperativos y subjuntivos (borra, elimina, publica, paga), además de push, merge, instalar y secretos. Una negación solo anula el término si lo precede de inmediato (admite cliticos y auxiliares). «sin revisar publicar» y «no borres nada pero publica» siguen siendo críticos.
- **Registro económico** (CSV): proveedor, modelo efectivo (evento `init`) o planeado, esfuerzo, tokens, caché, turnos, tiempo, costo nocional, costo real (`SUSCRIPCION_SIN_CARGO_API`), cuota (`NO_OBSERVADA`), coordinación y calidad (`--verify-cmd`). `--raw-dir` guarda la salida bruta.

## Pruebas de aceptación
Deterministas: `npm run routing:v2:test` → 11 + 12 + 21 OK; `test_orca_dispatch` 5 OK; `preambra-orca-smoke.py` OK.

| Prueba | Resultado | Evidencia |
|---|---|---|
| Arranque LEAN | PASS real | `init`: 26 herramientas, 0 MCP, 0 skills, modelo claude-haiku-5-5 |
| Persistencia | PARCIAL | Lanzador: lee el archivo en cada proceso. Claude Desktop interactivo: **no** se aísla automáticamente |
| Proyecto correcto | PASS real | cwd del repo cliente con `--project altiora` → BLOCKED |
| Modelo proporcional | PASS (Claude) | low→haiku, medium→sonnet, high→bloqueado en LEAN. Codex: modelo efectivo NO_OBSERVADO |
| Tarea sencilla sin delegación | PASS | proveedor claude, cadena vacía |
| Escalamiento justificado | PASS | ADVANCED sin motivo → BLOCKED; con motivo → opus/high |
| Delegación real | PASS real | Codex en solo lectura respondió «18»; `grep -c '^def '` = 18. Agy no se ejecutó |
| Proveedor no disponible | PASS simulado | claude fuera del PATH → respaldo codex `read-only` |
| Ciclos | PASS | cadena `claude` → ciclo y profundidad bloqueados |
| Negaciones mixtas | PASS | 13 casos nuevos en `test_client_routing.py` |
| Seguridad | PASS real | LEAN: `.env` denegado y `ok.txt` creado. Preflight: la tarea con `.env` quedó bloqueada sin aprobación |
| Medición | PASS con límites | cuota no observable; Codex no expone turnos |
| Reversión | PASS | los tests del commit base `99319cf` pasan; basta con no fusionar o revertir el commit |

## Consumo observado (n=1, cuota OAuth no observada)
| Corrida | Proveedor | Tokens totales | Nocional |
|---|---|---|---|
| T1 deny LEAN | claude-haiku-5-5 low | 64.041 | 0,007 USD |
| T2 Codex | gpt-6.1-sol low | 74.101 (corregido) | n/d |
| T2b Codex (repetición con captura) | gpt-6.1-sol low | 260.686 (corregido) | n/d |

**Hallazgo:** Codex carga más de 139 skills del repo y avisa «Exceeded skills context budget». En Codex el perfil LEAN no aísla. Piloto propuesto, sin probar: `--ignore-user-config` y un cwd neutro.

## Límites y riesgos abiertos
- El guard `PreToolUse` tardó unos 0,6 s por llamada (3 mediciones) frente a un tope de 10 s. Si agota el tiempo, Claude Code sigue adelante, es decir, falla abierto. Además no cubre escrituras por Bash ni las lecturas. LEAN no depende de él.
- Graphify: el MCP responde (21.908 nodos, grafo de `347f874`). OmniRoute: hay un servicio HTTP en el puerto, pero `/v1/models` exige autenticación, así que queda `NOT_VERIFIED` y sin activar.
- Notion: según la Agent Operating Guide (17-11-2026), GitHub es la fuente técnica y la guía no se modifica sin aprobación. No se escribió nada en Notion.
- `--max-budget-usd` con OAuth: no se verificó que corte la ejecución.
