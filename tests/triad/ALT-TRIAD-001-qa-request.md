# ALT-TRIAD-001 · Solicitud de revisión independiente (para Codex)

Estado: **PENDIENTE** (Codex sin créditos el 2026-11-03). Este paquete lo puede ejecutar Codex u otro revisor que **no** haya escrito el brief ni el esquema. Claude escribió `ALT-TRIAD-001-brief.md`; Antigravity escribió `ALT-TRIAD-001-ui.md`. La revisión previa de Claude (`ALT-TRIAD-001-report.md`) NO cuenta como independiente.

## Entradas
- `tests/triad/ALT-TRIAD-001-brief.md` (Claude Code, commit `3c8efc2`)
- `tests/triad/ALT-TRIAD-001-ui.md` (Antigravity 1.4.12, commit `e1d774f`)

## Qué verificar (marcar PASS / FAIL / NOT_RUN con comando y salida)
1. **Cumplimiento del brief:** los 4 criterios de éxito y las 5 secciones están presentes en `ui.md`, sin 3D ni datos reales.
2. **Contraste:** `python tests/triad/contrast-check.py` — confirma que cada par cumple AA y anota los valores declarados inexactos (Claude detectó 9 de 11).
3. **Medida de «sin scroll en 360×640»:** `ui.md` afirma ~304 px; es una suma estimada, no una medición. Marcar NOT_RUN salvo que se maqueta y se mide en navegador.
4. **Solape de rutas:** `git log --name-only --format=%h -- tests/triad` — un único escritor por archivo.
5. **Claridad:** ¿un desarrollador podría construir la landing solo con `ui.md`? Listar ambigüedades.

## Entrega del revisor
Crear **solo** `tests/triad/ALT-TRIAD-001-qa.md` con: cliente, versión, sesión, comandos, hallazgos reproducibles, estado PASS/FAIL, commit. No editar brief ni ui. Con ese archivo, y solo entonces, puede marcarse PASS en el issue #65.

## Comando para lanzarlo (requiere autorización y créditos)
`orca worktree create --name triad-qa --repo id:<repo> --base-branch <rama-con-tests/triad> --agent codex --setup skip --prompt "Ejecuta tests/triad/ALT-TRIAD-001-qa-request.md"`
