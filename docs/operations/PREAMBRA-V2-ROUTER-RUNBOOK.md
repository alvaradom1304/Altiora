# PREAMBRA V2 — Runbook de router adaptativo (primer hito técnico)

**Estado:** implementado para planificación en el router; NO certifica coordinación multi-IA viva.
**Marca:** PREAMBRA | **Núcleo técnico:** Altiora.
**Arquitectura completa:** documento maestro PREAMBRA-OS-V2-MASTER-HANDOFF.md (PR #93, propuesta).

## Alcance

Se incorporó una política dentro del dispatcher existente, sin un framework duplicado.
La salida JSON incluye policy_v2 y handoffs adicionales a los campos históricos.

- **Modo A:** resolver desde la IA actual sin transferencias.
- **Modo B:** constructor y revisor independiente.
- **Modo C:** paralelismo solo si se indica independencia, no hay dependencias y no se solapan rutas de escritura.
- **Modo D:** proyecto integral, por fases y con aprobación de negocio.
- **Riesgo crítico:** requiere aprobación humana.
- **Modelo:** UNKNOWN hasta que el ejecutor demuestre acceso.
- **Estado:** contratos inician PLANNED; DONE exige checks y evidencia.

Límites: la clasificación por palabras clave puede equivocarse. La sugerencia de revisor no demuestra una sesión activa. La comprobación de rutas no sustituye revisión de diffs.

## Pruebas desde el checkout actualizado

~~~bash
npm run routing:v2:test
npm run orca:test
npm run orca:smoke
npm run check

# Planes gratuitos, sin usar Orca ni IA externa
npm run orca:dispatch -- --json --entrypoint claude "Formatear un resumen"
npm run orca:dispatch -- --json --entrypoint codex "Implementar una API con pruebas"
npm run orca:dispatch -- --json --entrypoint antigravity "Crear estrategia y escena WebGL en paralelo"
npm run orca:dispatch -- --json --entrypoint claude "Proyecto integral de cliente de principio a fin"
~~~

**IAs no disponibles:** el router no observa cuotas ni logins. Si una IA está pausada o sin cuota, indícalo con `--unavailable codex` (repetible o separado por comas) o con `PREAMBRA_UNAVAILABLE_AIS=codex`. El revisor se elige en orden codex → claude → antigravity, sin repetir al líder y saltando las no disponibles. Si no queda ninguno, `reviewer_candidate` es `null`, se añade una advertencia y `requires_human_approval` pasa a `true`.

~~~bash
npm run orca:dispatch -- --json --entrypoint claude --unavailable codex "Implementar una API con pruebas"
~~~

La salida incluye modo, riesgo, motivo, colisiones, advertencias, `unavailable_ais` y contratos de traspaso. Sin --execute **no** se crean Task, Run, sesión de worker ni worktree.

El router por defecto es heurístico (sin consumo de LLM). Usar --router model únicamente si se desea una invocación Claude CLI y se verificó cuota/cuenta.

## Seguridad y ejecución real

- Se conserva el gate ALTIORA_DISPATCH_EXECUTE=1 para --execute y --launch-workers.
- V2 bloquea --launch-workers para A, D y para flujos que necesitarían worktrees todavía no creados. No saltarse esta restricción sin aislamiento real.
- --execute puede registrar tareas si hay autorización, runtime y permisos comprobados. No usar durante el piloto de lectura.
- Los modos C/D se consideran **planes** hasta que Orca demuestre Runs, Tasks, worktrees y QA en la PC.
- Ninguna habilidad/Markdown concede permiso para gastar, publicar, modificar producción o usar cuentas.

## Certificación de Orca en PC

1. Verificar versión del binario Orca, comandos y estado. Registrar evidencia sin credenciales.
2. Verificar modelos/efuerzos disponibles de Claude Code, Codex y Antigravity en las cuentas reales.
3. Ejecutar una única tarea de lectura; confirmar su ID real, output, estado y revisión.
4. Comparar el resultado con el contrato de traspaso; registrar errores y recuperación.
5. Solo después ensayar constructor+revisor y paralelismo en worktrees reales con permiso expreso.
6. Si el runtime falla, BLOCKED_RUNTIME; usar handoffs por GitHub en su lugar.

**Identidad en Orca (corregido 2026-11-22).** Orca atesta la terminal que llama y rechaza con `consumer_fenced` cualquier `--from` con otra identidad. El despachador solo reutiliza un Run coordinado por su propia terminal (`ORCA_TERMINAL_HANDLE`) y, si no, crea uno sin `--from`. El piloto debe lanzarse **desde una terminal de Orca**; un Run de otra terminal no se reutiliza. Orchestration es experimental: activarla en Settings → Experimental. Usar `worker-start` (supervisado, con `worker_done`) en vez de `agent launch` para el piloto. Diagnóstico completo: [certificación 2026-11-22](PREAMBRA-OS-CERTIFICACION-20261122.md).

## Arranque diario (Claude como orquestador)

1. `git fetch` y trabajar en un worktree propio desde `origin/main`; no editar el checkout canónico si tiene cambios ajenos.
2. `npm run resume` y `gh pr list`: el estado vivo lo da GitHub, no el checkpoint.
3. Clasificar el encargo: `python scripts/orca-dispatch.py --json --entrypoint claude "<encargo>"` (heurístico, sin coste). Modo A: hacerlo en la sesión. B: constructor + revisor distinto. C/D: plan hasta que Orca esté certificado.
4. Delegar en subagentes de `.claude/agents/` (descubrimiento e invocación comprobados el 2026-11-22). Codex por terminal: `codex exec -s read-only --skip-git-repo-check -C <worktree> -m <modelo> -c model_reasoning_effort=<nivel> -`. Antigravity: `agy -p "..." --mode accept-edits` solo para 3D/visual.
5. Cerrar con `npm run check`, revisión independiente y PR; nunca push a `main`.

**Autoridad de continuidad.** Estado vivo: GitHub (PR, CI, ramas) y, durante una ejecución, la Run de Orca con sus IDs reales. Histórico: `continuity/checkpoint.json` (instantánea fechada) y `team/chat/` (registro de reparto y cierres). `.altiora/orchestration.json` es registro local, no prueba de runtime: su `VERIFIED_READY` de 2026-11-01 no vale como estado actual.

## Próximos hitos

- PRE-ORCH-002: integración de política A/B/C/D, contratos y pruebas en router existente; solo planificación.
- PRE-ORCH-003: Orca real autenticado + primer handoff de lectura.
- PRE-ORCH-004: QA independiente y piloto constructor/revisor.
- PRE-ORCH-005: 12 tareas comparables y métricas de calidad, tiempo, costo, correcciones y valor de negocio.

**No declarar PRE-ORCH-002 como orquestación multiagente de extremo a extremo.**
