# Piloto experimental: Claude Code Mode (lectura MCP)

**Estado (2026-11-28): COMPARACIÓN INICIAL EJECUTADA. NO SE ADOPTA** (resultados al final). En el PATH aparece primero la CLI de npm, `2.1.309`; la compilación nativa `~/.local/bin/claude.exe` ya estaba en 2.1.323 y se autoactualizó durante el piloto a 2.1.332. Configuraciones sin cambios, verificado por hash.

Fuente oficial: <https://code.claude.com/docs/en/code-mode>, leída el 2026-11-28. Code Mode es experimental y está apagado por defecto. Claude escribe JavaScript que hace varias llamadas a herramientas en un paso, mediante la herramienta `REPL`.

## Requisitos oficiales y estado en esta PC

| Requisito | Estado |
|---|---|
| Claude Code ≥ 2.1.323, compilación nativa | **NO**: 2.1.309. Pendiente de autorizar la actualización |
| Sesión interactiva de terminal (no Desktop, no panel de VS Code, no nube, no `-p`) | Se usa una ventana de PowerShell independiente |
| Windows: Git for Windows | OK: `git version 2.56.1.windows.1` |
| Modelo con nombre completo (Opus/Sonnet/Haiku 5.5, Fable 5.2) | `claude-sonnet-5-5` en las dos variantes. Opus 5.5 High sigue como orquestador y no ejecuta el piloto |
| Activación | `$env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "1"` solo en esa ventana. **No** en `~/.claude/settings.json`; el `settings.json` del proyecto ignora la variable |
| Sin pasarela, ayudante de API key ni org ZDR/HIPAA | NO VERIFICADO; aparecerá al confirmar «Yes, turn on Code Mode» en la primera sesión |

## Compatibilidad con PREAMBRA (sin infraestructura nueva)

- **Hooks:** las llamadas dentro del código disparan `PreToolUse` con su nombre habitual, y `REPL` lo dispara con `tool_input.code`. El guard del proyecto (`matcher: "*"`, `onFailure: block`) sigue viendo `Write`/`Edit` aunque se invoquen desde JavaScript; para `REPL` no extrae rutas y permite. Hay que comprobarlo en la sesión B (paso 4).
- **Permisos:** las reglas `deny`/`ask` se aplican a las llamadas dentro del código. Las reglas por texto de `Bash` pueden eludirse, por eso el piloto deniega `Bash` completo. El sandbox oficial solo cubre comandos de shell: JavaScript, archivos, web y MCP quedan fuera. Mitigación: `ask: ["REPL"]` en un `--settings` de sesión, de modo que **una persona aprueba cada bloque de código antes de que se ejecute**. No hay ejecución autónoma de código.
- **MCP:** `--strict-mcp-config` con un único servidor local, `altiora-graphify`, que consulta el grafo del repo, y 7 herramientas permitidas por nombre. Se excluyen `list_prs`, `triage_prs` y `get_pr_impact`. Los MCP de cuentas reales que la CLI tiene conectados (Gmail, Slack, HubSpot…) no se cargan.
- **Delegación multi-IA:** `lean_run.py` fuerza `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=0` en todos los trabajadores delegados (prueba `test_delegated_workers_force_code_mode_off`). Además, `-p` no admite Code Mode. Un subagente solo lo usa si declara `REPL` en sus `tools`, y ningún rol del repo lo hace.
- **Por qué no `lean_run --interactive`:** el perfil LEAN usa `--safe-mode`, que apaga los hooks y los MCP, y `team/profiles/profiles.json` está protegido. Se usa el comando directo de abajo. La integridad posterior se sustituye por `git status --porcelain` antes y después (lectura).
- **Medición:** `scripts/transcript_usage.py` lee el transcript JSONL de la sesión (usage por mensaje sin duplicados, modelo efectivo, tiempo, llamadas `REPL`/MCP y errores de herramienta) y escribe una fila en el mismo CSV del lanzador.

## Runbook (tras autorizar la actualización)

Archivos de sesión, fuera del repo, en `%USERPROFILE%\preambra-recovery\20261128\codemode\`: `mcp-graphify.json` (solo graphify, `GRAPHIFY_BACKEND=none`), `session-settings.json` (`ask: ["REPL"]`) y `tarea.txt` (prompt fijo).

En **una ventana nueva de PowerShell**, una sesión nueva por variante (A primero), sin reanudar:

```powershell
$P = "$env:USERPROFILE\preambra-recovery\20261128\codemode"
Set-Location C:\Users\Usuario\Altiora\.claude\worktrees\antigravity-code-mode-pilot-bb55cf
git status --porcelain > "$P\antes-A.txt"
$env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "0"   # variante B: "1" y añadir ,REPL a --allowedTools
$G = "mcp__altiora-graphify__"
claude --model claude-sonnet-5-5 --effort medium --permission-mode default --strict-mcp-config --mcp-config "$P\mcp-graphify.json" --settings "$P\session-settings.json" --allowedTools "${G}graph_stats,${G}god_nodes,${G}get_neighbors,${G}get_node,${G}query_graph,${G}shortest_path,${G}get_community" --disallowedTools "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch,${G}list_prs,${G}triage_prs,${G}get_pr_impact"
```

1. Pegar el contenido de `tarea.txt`. En B, revisar y aprobar cada bloque `REPL` (anotar cuántos). Salir con `/exit`.
2. `git status --porcelain > "$P\despues-A.txt"`; los dos archivos deben ser idénticos.
3. Medir: `python scripts/transcript_usage.py --transcript <último .jsonl de ~/.claude/projects/C--Users-Usuario-Altiora--claude-worktrees-antigravity-code-mode-pilot-bb55cf> --log "$P\consumo.csv" --task-id CM-A --label sin-code-mode --calidad PASS|FAIL`.
4. Solo en B: confirmar que el encabezado muestra «Code Mode (experimental) is on», que el transcript contiene `REPL` y que una llamada `mcp__…` hecha desde el código respetó la lista permitida.

## Calidad, decisión y límites

- **Referencia determinista** (`graph.json` de 2026-11-10): 21.510 nodos y 24.557 aristas, sin contar hiperaristas. `graph_stats`/`god_nodes` pueden contar distinto; la calidad es **PASS** si la respuesta coincide con la salida de las herramientas del propio transcript, sin datos inventados, y si A y B coinciden entre sí.
- **Se registra:** tokens (entrada, caché creada y leída, salida y total ponderado), tiempo de reloj (en B incluye las aprobaciones humanas), turnos, llamadas `REPL`/MCP, errores de herramienta y calidad. Costo real y cuota: NO_OBSERVADOS (suscripción).
- **Decisión:** proponer la adopción solo si B reduce el total ponderado ≥ 30 % con la misma calidad y sin más errores. Con n = 1 es un indicio, no una garantía; una segunda tarea solo se ejecuta si el resultado es dudoso.
- **Fuera del piloto:** escrituras, sesiones sin aprobación de `REPL`, Desktop, delegación con Code Mode y cualquier cambio en `~/.claude/settings.json`.

## Resultado de la comparación inicial (2026-11-28, n = 1)

Registro: `%USERPROFILE%\preambra-recovery61128\codemode\consumo.csv`, generado con `scripts/transcript_usage.py`. Git quedó sin cambios tras las dos sesiones, y `~/.claude/settings.json`, `.claude/settings.json`, `.mcp.json` y `.agents/hooks.json` tienen el mismo hash antes y después.

| Ejecución | CLI | Turnos | Tiempo | Total tokens | Ponderado | Calidad | Herramientas |
|---|---|---|---|---|---|---|---|
| A, sin Code Mode | 2.1.323 | 6 | 88 s | 477.032 | 154.988 | PASS | 11 llamadas MCP directas y 2 ToolSearch |
| B, con Code Mode | 2.1.332 | 5 | 341 s (incluye 4 aprobaciones humanas de REPL) | 339.640 | 123.740 | PASS | 4 REPL, con 20 llamadas MCP dentro del código |
| Fallo B1: cancelado al relanzar | 2.1.323 | 1 | 12 s | 63.872 | 80.293 | FAIL | 1 REPL |
| Fallo B0: cerrada antes del prompt | — | 0 | — | 0 | 0 | FAIL | — |
| Fallo A0: `--disallowedTools` se tragó el prompt | 2.1.323 | — | — | 0 | 0 | FAIL | — |

- **Reducción de B frente a A:** −28,8 % en total y −20,2 % en ponderado. Si se suma el fallo B1, B cuesta −15,4 % en total y **+31,6 %** en ponderado.
- **Calidad:** las dos dan los mismos totales (iguales a la referencia), nodos, grados y vecinos. A omite la autollamada de `I()`; B la incluye y añade una nota de validación algo incoherente (acepta un desfase de 1 en `check()`/`scripts` y no en `n()`). Ninguna inventó datos ni tuvo errores de herramienta.
- **Seguridad:** los 4 bloques de B solo llamaron a `searchTools` y a herramientas de `altiora-graphify`, todos con aprobación humana. Las reglas y los hooks funcionaron: 0 escrituras.
- **Decisión: NO ADOPTAR ni preparar la integración.** No llega al umbral de −30 % ponderado, y la diferencia de versión de la CLI, la caché previa desigual y n = 1 impiden atribuir la causa. Revisión independiente de Codex LEAN (`REV-CM-02`, 88.937 tokens): «REPETIR_CONTROLADO». Una repetición controlada exigiría la misma versión de CLI en A y B, alternar el orden y que el fundador la autorice.

**Hallazgos del piloto:**
- La CLI 2.1.323 avisa de que las 14 reglas `Write(...)` de `.claude/settings.json` «never match» y recomienda `Edit(...)`. Las `Edit(...)` equivalentes existen, así que la protección se mantiene. Limpiar el archivo, que está protegido, corresponde a una persona.
- `--disallowedTools` admite varios valores: el prompt debe ir antes de las banderas.
- Los hooks `PreToolUse` tardaron más de 30 s en el primer paso de A.
- La CLI nativa se autoactualiza: para comparar hay que fijar la versión.
- `lean_run.py` fallaba al imprimir respuestas no ASCII en una consola cp1252; está corregido.
