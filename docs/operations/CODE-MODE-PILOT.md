# Piloto experimental: Claude Code Mode (lectura MCP)

**Estado (2026-11-28): PREPARADO, BLOQUEADO POR VERSIÓN.** La CLI instalada es `2.1.309 (Claude Code)` y Code Mode exige como mínimo **v2.1.323**. La actualización la autoriza el fundador; ninguna IA actualiza Claude Code ni cambia la configuración global.

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
