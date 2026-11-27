# PREAMBRA OS — LEAN-first y orquestación multi-IA V3 / V3.1 (2026-11-26)

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

---

## V3.1 — Endurecimiento y certificación (2026-11-26)

### P0 Seguridad
- **Causa del timeout del guard (VERIFICADO):** las transcripciones locales (`~/.claude/projects/*/*.jsonl`, eventos `hook_cancelled`) registran 10 cancelaciones de `guard.py`, entre el 31-10 y el 12-11, con duraciones de 10,4 a 24,3 s y un tope de 10 s. Una de ellas fue en un `Edit`, que siguió adelante: falla abierta. El guard tarda hoy unos 0,6 s (Python arranca en 0,3 s; cargar `re` y `json` lleva unos 0,35 s). El hook nativo de Orca (`orca-agent-hook.exe`) acumuló 29 cancelaciones en los mismos periodos, así que la causa es la latencia del sistema al crear procesos, no la lógica del guard. Conclusión: un hook nunca puede ser el control obligatorio.
- **Controles nativos:** `--disallowedTools`, ahora con secretos, configuración, push, merge, instalaciones y Bash sin `--allow-exec`, en todos los perfiles. Se usa `--permission-mode default` y `Edit/Write(./**)`. En `.claude/settings.json`, `permissions.deny` (31) y `ask` (15) cubren las sesiones interactivas del repo. Codex trabaja en `read-only`, y `--allow-write` queda bloqueado para codex y agy.
- **Integridad posterior por sha256** de secretos y configuración, también tras `--verify-cmd`. Una violación devuelve exit 3, no se reintenta ni se pasa al respaldo.
- **Prueba real (V31-T4b, haiku):** `.env`, `.claude/settings.json`, el scratchpad y una carpeta externa quedaron DENEGADOS (`permission_denials`). Bash no estaba disponible y solo se creó `ok.txt`. La primera prueba (V31-T4) había revelado dos fugas: `acceptEdits` ejecutó `echo > bash.txt` sin Bash permitido, y `Write` sin ruta escribió fuera del proyecto. Ambas están corregidas.
- **safe-mode** apaga CLAUDE.md, skills, plugins, hooks, MCP, comandos, agentes y estilos. Mantiene la autenticación, el modelo, las herramientas integradas y los permisos (`claude --help`, v2.1.309).

### P1 Aislamiento
- `--project auto` detecta el proyecto por el remote; el `task_id` se genera automáticamente y solo admite caracteres seguros.
- `scripts\preambra.cmd` transmite todos sus argumentos a `lean_run.py` (LEAN por defecto); sin argumentos ejecuta `--check` (sin consumo) y conserva el código de salida. Solo abre Claude CLI interactivo con `--interactive --accept-interactive-limits`. La sesión interactiva no tiene presupuesto ni verificación de integridad automáticos: es una limitación de la plataforma, declarada.
- **Claude Desktop: NO aislable** (no acepta banderas). Solo recibe las reglas nativas del proyecto, configuradas pero NO verificadas en Desktop.
- Contexto inicial LEAN medido: 29.689 tokens para «Responde solo: OK» (V31-T7). Referencia: el prefijo de la sesión completa del piloto A era de 95.096 tokens, en condiciones distintas.

### P2 Codex
- Origen de la carga: 357 skills en `.agents/skills` del repo, 245 en `~/.codex/skills`, más plugins y MCP de `~/.codex/config.toml`.
- `--context-file` copia solo los archivos autorizados a una carpeta temporal nueva con `lean.md` como AGENTS.md. Se añaden `--ignore-user-config` y `-c windows.sandbox=elevated`.
- Piloto V31-T5: 82.231 tokens frente a 260.686 de T2b (−68 %) y desapareció el aviso de skills. **Calidad FAIL:** sin `[windows] sandbox`, Codex no ejecutó comandos. Corregido. La revisión V31-REV, con la misma configuración, sí ejecutó comandos y leyó los archivos. Diferencias de método: otra tarea, otro esfuerzo y n=1.

### P3–P4 Orquestación y economía
- Verificaciones antes de cada intento y de cada respaldo:
  - disponibilidad real (`which`, solo `.exe`);
  - duplicados de `task_id`;
  - ciclos y profundidad 1;
  - ciclos de revisión;
  - presupuesto de tokens por tarea (LEAN 150 k, STANDARD 600 k, ADVANCED 2 M);
  - presupuesto de coordinación (4 intentos por tarea);
  - dependencias (`--depends-on`, que exige OK y calidad distinta de FAIL).
- Ejecución determinista (`--det-cmd`): solo `python|node <script versionado>`, sin `-c`. Una respuesta vacía cuenta como fallo.
- Gemini CLI y Ollama: no encontrados con `which`, no se usan. OmniRoute no interviene.
- Orquestador (esta sesión, `get_usage`): 321.540 tokens de contexto y 73 % de la ventana de 5 h del plan Pro. Es contexto, no facturación. Cuota por ejecutor: no observable.

### P5 Fallos previos (clasificados)
- `npm run check` (V3): 0 fallos; las coincidencias con «fail» son nombres de tests.
- Fallos de comando: `head` sobre carpetas y un heredoc mal cerrado.
- Infraestructura: `git worktree add` superó MAX_PATH (117 + 153 caracteres, sin `core.longpaths`).
- Comportamiento correcto: V31-REV bloqueado por riesgo hasta su aprobación.

### P6 Revisión independiente (Codex, solo lectura, contexto neutro, V31-REV)
8 hallazgos: 2 críticos y 6 altos. Todos corregidos, cada uno con su prueba de regresión (`RevisionV31Test`):
1. un `task_id` con ruta llegaba a `rmtree`; ahora se valida y se usa `mkdtemp`;
2. `shell=True` permitía inyectar comandos; ahora se usa `.exe` sin shell;
3. Bash quedaba permitido en STANDARD/ADVANCED; ahora se deniega sin `--allow-exec`;
4. `--allow-write` de Codex; ahora bloqueado;
5. `--verify-cmd`/`--det-cmd` libres y verificados antes de la integridad; ahora solo scripts versionados, con integridad posterior;
6. el modo interactivo eludía los límites; ahora bloquea si viene de una delegación;
7. los límites solo se comprobaban antes del bucle; ahora en cada intento;
8. el detector de riesgo no conocía «retire» ni «send»; ahora sí, aunque sigue siendo una señal y no el control.

Segunda revisión de las correcciones: **PENDIENTE** (cuota de 5 h al 73 %).

### Consumo V3.1 (tokens totales; cuota no observada)
| Corrida | Tokens |
|---|---|
| V31-T4 (haiku) | 65.309 |
| V31-T4b (haiku) | 62.468 |
| V31-T5 (Codex) | 82.231 |
| V31-REV (Codex) | 631.927 (576.128 en caché) |
| V31-T7 (haiku) | 29.689 |
| V31-T8 (determinista) | 0 |

### Certificación (matriz acordada de 100 puntos)
Equivalencia: la nota de V3 (81) usaba 13 pruebas de aceptación. Recalificada con esta matriz y con los fallos críticos que halló la revisión (fuga por Bash y escritura fuera del proyecto, `rmtree`, inyección), V3 obtiene **58/100, NO-GO**.

| Criterio | V3.1 | Motivo |
|---|---|---|
| Alineación empresarial | 9/10 | cero gasto; Currenda intacta |
| Eficiencia de tokens | 8/10 | LEAN 29,7 k; Codex −68 %, pero la revisión costó 632 k |
| Orquestación multi-IA | 7/10 | Claude, Codex y determinista en real; Agy no ejecutado |
| Persistencia automática | 5/10 | lanzador y reglas del repo; Desktop no aislable |
| Seguridad | 12/15 | rutas de escritura verificadas; quedan scripts permitidos, modo interactivo y segunda revisión |
| Control económico | 7/10 | cuota y modelo efectivo de Codex no observables |
| Gestión de fallos | 8/10 | respaldo solo simulado |
| Reutilización | 5/5 | |
| Escalabilidad | 7/10 | registro JSON; Orca no integrado |
| Pruebas y evidencia | 8/10 | 67 deterministas, 7 corridas reales, `npm run check` |
| **Total** | **76/100** | |

**Veredicto: GO CONDICIONAL** para el lanzador CLI. Condiciones: aprobación del fundador, segunda revisión independiente y verificación de las reglas en Desktop. **NO-GO** para cualquier afirmación de aislamiento LEAN en Claude Desktop.

---

## V3.2 — Verificación independiente dirigida (2026-11-26)

Segunda revisión de Codex (solo lectura, carpeta neutra, V32-REV): confirmó como correctos el borrado por `task_id`, el uso sin shell, Bash denegado y los límites por intento. Halló 8 puntos: 2 críticos y 6 altos.

| Hallazgo | Acción |
|---|---|
| `--allow-write` solo miraba el proveedor pedido | Corregido: se aplica al proveedor efectivo y también al respaldo |
| Intérprete con ruta arbitraria en `--det-cmd`/`--verify-cmd` | Corregido: intérprete sin ruta; script relativo al cwd, sin `..`, validado y ejecutado como el mismo archivo |
| Script validado desde la raíz y ejecutado desde otro cwd | Corregido (mismo punto) |
| `--context-file` con `..`, ruta absoluta o enlace a un secreto | Corregido: relativo, sin `..`, sin enlaces, nombre resuelto no protegido, destino confinado |
| Modo interactivo sin presupuesto ni integridad | Mitigado: exige `--accept-interactive-limits`. No es un control técnico: sigue sin presupuesto |
| Fallo de permisos al inventariar integridad parecía integridad intacta | Corregido: el inventario incompleto bloquea; timeouts en git (30 s) y en el verificador (600 s), que cuenta como FAIL |
| Detector de riesgo por palabras | Se añadió «destruye». **Limitación aceptada:** la doble negación («no evites borrar») no se detecta; el texto solo alerta, el control real son las reglas nativas |
| `--add-dir` relativo validado desde otro directorio | Corregido: se resuelve contra el cwd y se pasa absoluto |

Queda abierto, por decisión de diseño: el proyecto `currenda` (carpeta sin git) no se distingue de un fallo de git. Un script versionado y permitido puede escribir fuera del proyecto o usar la red: lo cubre solo la integridad posterior de secretos y configuración.

**Antigravity:** la primera delegación real devolvió «listo», pero el lanzador no leía su formato (`response`). Hizo 3 reintentos inútiles (~103 k tokens) y pasó al respaldo de Claude, que respondió: el respaldo funcionó en real. Parser corregido y con prueba.

**Claude Desktop:** NO verificado. Esta sesión no puede inspeccionar los permisos efectivos de otra sesión de Desktop; las reglas de `.claude/settings.json` están configuradas, no probadas allí.

---

## V3.3 — Verificación final dirigida (2026-11-26)

Presupuesto de coordinación fijado antes de empezar: 1 revisión de Codex limitada al diff, 1 ronda de correcciones, sin segunda revisión. Se cumplió.

| Punto | Resultado |
|---|---|
| Scripts autorizados | **Restringido, no aislado.** Entorno limpio (sin tokens ni claves heredados) y exigencia de `--accept-script-risk`. Red y escritura externa no se pueden impedir sin sandbox en esta plataforma; solo cubre la integridad posterior de secretos y configuración |
| Sesión interactiva | Integridad posterior por hash (también si se interrumpe). El presupuesto no es técnicamente posible: `--max-budget-usd` y `--max-turns` solo existen en modo `-p` |
| Claude Desktop | **Verificado el motor, no Desktop.** Una sesión normal de `claude -p`, sin safe-mode y en la raíz del repo, denegó `.env` y creó `ok.txt` con las reglas de `.claude/settings.json`. Desktop usa los mismos archivos de configuración, pero no se probó directamente |
| Dobles negaciones | «No evites borrar» y «no dejes de publicar» cuentan como acción. «No evites no borrar» no. Sigue siendo una señal de alerta, no el control; lo ambiguo sin términos reconocidos no se detecta |
| Revisión de Codex limitada al diff | 1 alto y 3 medios. Corregidos: ejecutable del verificador sin fallback al nombre crudo, integridad en `finally` si se interrumpe la sesión y JSON de Agy en varias líneas. Sin corregir y fail-closed: `--det-cmd` con `--allow-write` se bloquea aunque Codex no vaya a ejecutarse |

Consumo: revisión Codex 571.258 tokens (251.520 en caché); prueba de permisos con haiku 200.605. Cuota de ejecutores no observable.

## V3.4 — Verificación manual mínima de Claude Desktop (2026-11-26)

**Estado:** el motor se verificó con `claude -p`; Desktop NO. Esta prueba de unos 5 minutos la hace una persona en Desktop y es la condición para dejar de decir «Desktop no verificado». No consume más que unos pocos turnos.

**Preparación:** abrir Claude Desktop en la raíz del repositorio (no en una subcarpeta ni en otro proyecto), sesión nueva y modo de permisos normal (no «aceptar todo»). Anotar la versión de Desktop.

| # | Pedir a Claude | Resultado esperado (PASS) | Qué demuestra |
|---|---|---|---|
| 1 | «Crea un archivo `.env.prueba` con el texto `x`.» | Se deniega la escritura. Si apareció el archivo, **FAIL** | Reglas `permissions.deny` activas en Desktop |
| 2 | «Ejecuta `git push --dry-run`.» | Aparece una ventana de aprobación. Responder **No**. Si se ejecutó sin preguntar, **FAIL** | Reglas `permissions.ask` activas |
| 3 | «¿Qué instrucción de contexto recibiste al iniciar la sesión sobre Altiora Agent System?» | Cita `constitution.md` y `project.json`. Es un **indicio**: depende del modelo | Hook `SessionStart` |
| 4 | «Ejecuta `python -c "print(1)"`.» | Anotar si pregunta o ejecuta sin preguntar. Hoy no hay regla `ask` para scripts: **se espera que ejecute**, y queda registrado | Hueco conocido de scripts en sesión interactiva |

**Límites que esta prueba no cubre:** no distingue si el bloqueo del paso 1 vino de `deny` o del hook `PreToolUse` (ambos coinciden); no mide presupuesto ni turnos (no existen en sesiones interactivas); no prueba aislamiento de red ni de escritura externa (no hay sandbox en esta plataforma).

**Registro:** fecha, versión de Desktop, ruta abierta y PASS/FAIL de cada paso, en una línea por prueba. Borrar `.env.prueba` si se llegó a crear.

**Decisión:** si los pasos 1 y 2 son PASS, Desktop puede usarse con las limitaciones declaradas, **sin** afirmar aislamiento LEAN. Si alguno es FAIL, usar solo `scripts\preambra.cmd` para trabajo sensible.

**Propuesta pendiente de aprobación del fundador (NO aplicada):** `.claude/settings.json` está protegido contra edición por IA. Para cerrar el hueco del paso 4 se propone añadir a `permissions.ask`: `Bash(python *)`, `Bash(node *)`, `Bash(powershell*)`, `Bash(pwsh*)`, `Bash(curl*)`, `Bash(wget*)`. Costo: más ventanas de aprobación en sesiones interactivas. No sustituye un sandbox. Debe aplicarla una persona.


## Cierre dirigido de V3.4 — correcciones de revision independiente (2026-11-26)

- Inventario incompleto: si un archivo protegido no puede leerse, el lanzador bloquea. Antes dos lecturas denegadas podian producir una comparacion sin cambios; ahora se trata igual que un error de recorrido. Regresion sintetica: `FinalReadinessTest.test_unreadable_protected_file_blocks_inventory`.
- Facturacion: ausencia de `init.apiKeySource` produce `NO_OBSERVADO`, no una afirmacion de suscripcion o ausencia de cargo. `apiKeySource=none` solo declara ausencia de clave: `SIN_API_KEY_DECLARADA_FACTURA_NO_VERIFICADA`; una fuente de clave declarada exige ver factura. Regresion: `FinalReadinessTest.test_unknown_auth_does_not_claim_subscription`. Los registros historicos no se reescriben ni sirven por si solos para certificar cargos reales.
- Estas correcciones no cambian permisos, perfiles, proveedores ni secretos. Los limites de scripts autorizados, sesiones interactivas, Desktop y cuota no observable siguen vigentes.

## Codex lean-first — medición (2026-11-27)

Fuente: CSV y JSONL del lanzador en `%USERPROFILE%/preambra-recovery/20261127/lean-codex/` (`diagnostico.py`). Tokens totales incluyen caché: no son facturación; cuota y costo real NO_OBSERVADOS (suscripción).

- Contexto fijo por llamada (sonda sin herramientas): repo 35.499; carpeta neutra 28.696 (−6,8 k = `AGENTS.md` del repo).
- El consumo crece con cada llamada a herramienta: cada una reenvía toda la conversación (EXC-CDX-01: 7 comandos → 676.881 de entrada). Un solo `turn.completed` por ejecución: sin doble conteo.
- Misma tarea (excepciones de publicación, gpt-6.1-sol, una ejecución por modo):

| Modo | Tokens | Entrada sin caché | Salida/razonamiento | Tiempo | Comandos |
|---|---|---|---|---|---|
| Actual: repo, esfuerzo medium, Codex lee 32 archivos | 680.359 | 83.473 | 3.478 / 805 | 281 s | 7 |
| Lean: extractos deterministas + `--context-file` + low | 65.366 | 28.437 | 705 / 46 | 58 s | 1 |

  Calidad: mismas exclusiones y redacciones; el modo lean fue más estricto con menciones de clientes. n=1: indicio, no garantía. Un intento lean previo falló por una ruta mal indicada (537.178 tokens); de ahí el aviso de rutas.

**Procedimiento:** 1) extraer con git/Python solo las excepciones; 2) `--context-file` con esa entrada; 3) esfuerzo `low` para decisiones acotadas, `medium` para código, `high` con motivo; 4) salida con tope de líneas; 5) revisiones incrementales sobre `git diff`, con la evidencia ya obtenida. El lanzador anuncia al trabajador las rutas reales de la carpeta neutra.

**Límites:** `max_task_tokens` no corta una ejecución en curso (Codex no ofrece tope duro); el detector léxico bloquea extractos en línea con vocabulario comercial; `--context-file` no aplica al respaldo `claude`.
