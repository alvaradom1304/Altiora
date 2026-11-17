# Validación ECC · 2026-11-17

## Alcance
Comparación de seis prácticas centrales de ECC contra Altiora/PREAMBRA; ver [matriz](../../references/ecc-adoption.json) y [uso](ECC-INTEGRACION.md). Upstream fijado, MIT conservada. No se instala el plugin completo ni se importan sus scripts, observadores o servicios.

## Evidencia actual
- npm run check en altiora-ecc: PASS, salida 0, handoff PASSED/errors vacíos.
- Pruebas de integración: 9 PASS, 1 SKIP POSIX en Windows. Incluyen Git real con secreto ficticio bloqueado y contenido limpio aceptado, worktree aislado, custom/no-op, directorio en ruta de hook y bare true/yes/1.
- Pruebas previas del guardián: 6 PASS, incluidas en toolkit:test.
- Regresiones de revisión: antes fallaban hook no-op/directorio y bare; después pasan. No se borraron fallos del informe.
- SkillSpector 2.12.0, sin LLM y fail-on-incomplete: altiora-quality-review SAFE 0/100; aem-learning-os SAFE 0/100. Sin hallazgos ni exclusiones.
- Primer escaneo de Learning OS: CAUTION por cobertura parcial de un expected_output anterior demasiado largo para el parser estático. Se compactaron los criterios conservándolos y se agregó una evaluación de aislamiento por cliente; el escaneo completo posterior pasó.
- Búsquedas de Unicode oculto, contenido escondido y red/permisos sobre ambas skills: sin coincidencias (rg salida 1 en las tres).

## Límites
Los tests usan fixtures, no credenciales reales. La comprobación POSIX no se ejecutó en Windows. Configuración del hook y prueba funcional se informan por separado. Sin ahorro o tokens medidos; modelo efectivo no observado. La revisión independiente y la validación de la copia canónica se registran al concluir. No acredita instalación nativa de ECC, disponibilidad de todos sus módulos ni despliegue.

## Revisión independiente
Revisor altiora-review: cumple lo comprobado, sin hallazgos pendientes en el alcance de código/documentos. Revalidó las regresiones del hook y booleanos bare; no se atribuyen a esa revisión los escaneos o check completo del implementador.

## Copia canónica
Archivos ECC aplicados con respaldo externo al repositorio y preservación de los demás scripts/locales. El doctor confirma integrated=true y hook configurado con alcance worktree; su functionalCheck permanece not_run porque el diagnóstico es solo de presencia/configuración. La prueba de commits usa repositorios temporales separados.

El primer control canónico tropezó con los enlaces relativos del respaldo de esta tarea; se conservó ese respaldo fuera del árbol. El control posterior sigue bloqueado por un respaldo anterior: .altiora/backups/pre-pr86-20261110/creative-ads-os/WORK_ROUTER.md (ENOENT). Ese respaldo y el verificador no se modificaron. Por tanto, no se declara PASS general de la copia canónica. La rama de integración limpia sí pasó el control completo.

## Comprobación canónica final
- ecc:test: 9 PASS / 1 SKIP POSIX en Windows; secrets:test: 6 PASS.
- ecc:doctor: salida 0, ocho capacidades presentes, integrated=true, hook configured, functionalCheck not_run.
- Revisor independiente: confirmó raíz/remoto, alcance worktree y 11/11 archivos revisados equivalentes por SHA-256 normalizando CRLF/LF. No lo presentó como PASS global ni como commit sobre trabajo real.
- No se fusionó el PR; la instalación local no sustituye la integración remota.
