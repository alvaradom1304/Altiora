# Altiora — deduplicación segura y coordinación multi-IA
Fecha: 2026-11-03

## Resultado observado en GitHub (rama main, commit f7e3f0e)
Comparación de rutas `*/SKILL.md` y SHA de blobs, sin ejecutar los agentes:
- 355 skills canónicas con entrada `skills/*/SKILL.md`.
- 85 grupos de archivos `SKILL.md` idénticos, cada uno con dos rutas: **80** copias en `temp_skills/Agency_OS_208_Skills/`, **3** de archivo retirado y **2** adaptadores de clientes.
- No se encontró duplicación exacta entre dos skills canónicas distintas. **Las 80 copias temporales son candidatas a retirar del árbol operativo, no 80 skills redundantes distintas.**
- Coincidencia por SHA demuestra identidad de archivo; no demuestra si el paquete temporal requiere esos archivos para restauración o reproducibilidad. Conservar hasta revisar dependencias, permisos y procedencia.

## Optimización aplicada / propuesta
1. Fuente de verdad de ejecución: `skills/`; no indexar `temp_skills/` como skills activas.
2. Script de auditoría **solo lectura**: `node scripts/skill-duplicates-report.mjs`; genera grupos exactos para revisión.
3. Mantener archivos bajo `.agents/` y `.claude/` si funcionan como adaptadores de clientes.
4. Antes de retirar `temp_skills/`, buscar referencias con `git grep -n 'temp_skills/Agency_OS_208_Skills'`, ejecutar `npm run check` y `npm run skills:audit`, y verificar que la copia temporal no sea el único respaldo. Eliminar solo en PR separado con pruebas verdes y copia recuperable.

## Prueba real de coordinación, identificador ALT-TRIAD-001
**Autoridad**: CEO humano aprueba acciones externas; Claude Code dirige el ejercicio. Ejecutar solo con los tres clientes instalados y autorizados en el equipo; GitHub Actions remoto **no abre aplicaciones locales** por sí mismo.

- Claude Code: leer `team/ROUTING.md`, elaborar en una rama `tests/triad/ALT-TRIAD-001-brief.md` un brief ficticio de una landing para venta de plantas, con definición de éxito y riesgos. Registrar cliente, sesión, commit.
- Antigravity: leer el brief, crear **en ruta distinta** `tests/triad/ALT-TRIAD-001-ui.md` un esquema visual verificable (no publicar ni instalar software). Registrar sesión y commit.
- Codex: verificar ambos entregables, comprobar claridad, cumplimiento del brief y no solapamiento de rutas; crear `tests/triad/ALT-TRIAD-001-qa.md` con hallazgos, estado PASS/FAIL y commit. Nunca autoaprobar.
- Claude: reunir un reporte final con enlaces a los tres commits, tiempos, versiones, cambios y evidencias de las tres sesiones. Solo entonces marcar **PASS** en [issue #65](https://github.com/alvaradom1304/Altiora/issues/65).

### Mensaje único para iniciar desde Claude Code en la computadora
> Actúa como director operativo de Altiora. Lee team/ROUTING.md y docs/operations/SKILLS-DEDUP-TRIAD-2026-11-03.md. Inicia ALT-TRIAD-001 en modo seguro y sin publicar, gastar ni instalar software. Comprueba la disponibilidad real de Orca, Antigravity y Codex. Presenta primero el estado de conexiones y prepara el handoff. Si no hay conexión real, marca BLOCKED y no simules su ejecución.

Este mensaje inicia la **comprobación local** cuando el usuario lo pega en Claude Code. No prueba que el equipo pueda recibir comandos remotos de este chat.

## Evidencia y estados
Usar `NOT_TESTED`, `BLOCKED`, `FAIL`, `PASS` por cada herramienta, con fecha, versión, resultado reproducible, ruta y commit. La existencia de scripts y roles no implica conexión en vivo.
