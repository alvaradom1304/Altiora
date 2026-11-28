# Claude Code Mode: piloto de lectura MCP

**Estado: HOLD (2026-11-28).** Se hizo una comparación inicial y no superó el criterio de adopción. Code Mode **no** se activa por defecto ni en la delegación, y el piloto **no** se repite sin una decisión expresa del fundador. Se conservan los resultados y el medidor (`scripts/transcript_usage.py`).

Fuente: <https://code.claude.com/docs/en/code-mode>, leída el 2026-11-28. Code Mode es experimental y está apagado por defecto. Claude escribe JavaScript que hace varias llamadas a herramientas en un paso, mediante la herramienta `REPL`.

## Requisitos oficiales (resumen)

- Claude Code ≥ 2.1.323, compilación nativa, en una sesión interactiva de terminal. No sirven Desktop, el panel de VS Code, la nube ni `-p`.
- Windows: Git for Windows.
- Modelo por nombre completo (`claude-sonnet-5-5`, `claude-opus-5-5`…).
- Se activa con `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1` solo en el shell de la sesión. El `settings.json` del proyecto ignora la variable, y `0` en cualquier capa la apaga.
- La primera vez pide confirmar «Yes, turn on Code Mode». Una sesión iniciada con Code Mode solo puede reanudarse con Code Mode.

## Controles vigentes en PREAMBRA

- **Delegación:** `lean_run.py` fuerza `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=0` en todos los trabajadores delegados (`test_delegated_workers_force_code_mode_off`). Ningún rol declara `REPL`.
- **Permisos:** las reglas `deny`/`ask` se aplican a las llamadas que hace el código, con su nombre habitual. Las reglas `Bash` por texto pueden eludirse, y el sandbox oficial no cubre JavaScript, archivos, web ni MCP. Si se usa Code Mode: denegar `Bash`, `ask: ["REPL"]` en un `--settings` de sesión (una persona aprueba cada bloque) y `--strict-mcp-config` con MCP de solo lectura.
- **Hooks:** las llamadas dentro del código disparan `PreToolUse` con su nombre habitual, y el guard del proyecto las sigue viendo.

## Resultado de la comparación inicial (n = 1)

Tarea: consultas de solo lectura a `altiora-graphify` (`graph_stats`, `god_nodes` y `get_neighbors` de 5 nodos), con `claude-sonnet-5-5` y esfuerzo medium. Registro local, no versionado: `%USERPROFILE%\preambra-recovery\20261128\codemode\consumo.csv`.

| Ejecución | CLI | Tiempo | Total tokens | Ponderado | Calidad |
|---|---|---|---|---|---|
| A, sin Code Mode | 2.1.323 | 88 s | 477.032 | 154.988 | PASS |
| B, con Code Mode (4 REPL aprobados, 20 llamadas MCP dentro) | 2.1.332 | 341 s, con aprobaciones humanas | 339.640 | 123.740 | PASS |
| Fallos: B cancelada al relanzar, y otros tres intentos sin consumo | 2.1.323 | — | 63.872 | 80.293 | FAIL |

- B frente a A: −28,8 % en total y −20,2 % en ponderado. Con el fallo de B: +31,6 % ponderado.
- Calidad equivalente: mismos totales (21.510 nodos y 24.557 aristas, iguales a la referencia), nodos, grados y vecinos. 0 escrituras; las configuraciones tienen el mismo hash antes y después.
- **Decisión: no adoptar.** No llega al umbral de −30 % ponderado. Además, la versión de la CLI fue distinta (autoactualización), la caché previa era desigual y n = 1. Revisión Codex LEAN `REV-CM-02`: «REPETIR_CONTROLADO»; queda en HOLD.

## Si el fundador reabre el piloto

- Fijar la misma versión de la CLI nativa en A y B (la autoactualización la cambió a mitad de prueba) y alternar el orden.
- El prompt va **antes** de las banderas: `--allowedTools`/`--disallowedTools` admiten varios valores y se tragan lo que venga después.
- `ask: ["REPL"]` solo tiene efecto en la variante con Code Mode; en la otra la CLI avisa de que no coincide con ninguna herramienta.
- Comando base, en una ventana de PowerShell nueva y desde la raíz del checkout. Las herramientas del grafo se listan por nombre y `list_prs`/`triage_prs`/`get_pr_impact` quedan denegadas:

  ```powershell
  $env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = '1'   # '0' en la variante sin Code Mode
  & "$env:USERPROFILE\.local\bin\claude.exe" '<prompt fijo>' --model claude-sonnet-5-5 --effort medium --permission-mode default --strict-mcp-config --mcp-config <mcp-solo-lectura.json> --settings <ajustes-de-sesion.json> --allowedTools 'REPL,<herramientas MCP de lectura>' --disallowedTools 'Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch'
  ```

- Medir cada sesión desde su transcript (`~/.claude/projects/<proyecto>/<sesion>.jsonl`):
  `python scripts/transcript_usage.py --transcript <sesion.jsonl> --log <consumo.csv> --task-id CM-X --label <etiqueta> --calidad PASS|FAIL`

## Hallazgos que siguen vigentes

- **Reglas `Write(...)` de `.claude/settings.json`: no tienen efecto.** Prueba directa (2026-11-28, CLI 2.1.309 y 2.1.332, `-p`, `acceptEdits`): `deny: ["Write(**/*.probe)"]` **no** impidió que la herramienta Write creara el archivo; `deny: ["Edit(**/*.probe)"]` sí lo impidió («File is in a directory that is denied by your permission settings»). Las 13 reglas `Write(...)` del proyecto, y las del perfil LEAN, tienen gemela `Edit(...)`, que es la que protege. Eliminar las `Write(...)`, en un archivo protegido, corresponde a una persona. NO VERIFICADO: si las reglas `Edit(...)` relativas sin `**/` (p. ej. `team/profiles/profiles.json`) coinciden cuando la sesión se abre en una subcarpeta.
- La CLI nativa se autoactualiza: fijar la versión antes de comparar.
