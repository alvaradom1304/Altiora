# Protocolo para cambios protegidos de skills (Zero-Loss)

**Objeto:** conservar el conocimiento de Altiora mientras se permiten mejoras legítimas. Los controles automáticos detectan diferencias; no certifican por sí solos la equivalencia semántica ni el funcionamiento real de una skill.

## Baselines protegidos

- `references/capability-protection-baseline-2026.json`: 355 identidades de skills, 22 roles, 5 workflows y 26 archivos críticos.
- `references/protected-skill-content-baseline-2026.json`: hash Git blob SHA-1 de los 2.757 archivos originales dentro de `skills/` en el commit `f49c57d`.
- El hash se calcula con `SHA1("blob " + tamaño_en_bytes + "\\0" + contenido)`, exactamente como un blob normal de Git; no es una firma criptográfica moderna ni sustituye controles de autenticidad de terceros.

Verificación local de solo lectura:

```bash
npm run capabilities:protect
npm run skills:integrity
npm run check
```

Los tests funcionan sin iniciar Claude, Codex, Antigravity, After Effects o servicios de pago.

## Si una skill cambia legítimamente

1. Crear rama con punto de partida verificable, conservar una copia recuperable del contenido anterior y registrar propósito y archivos afectados.
2. Revisar el diff de la fuente (no solamente de la copia de Antigravity); especificar qué capacidades se añadieron, qué instrucciones se movieron y qué ejemplos siguen disponibles.
3. Verificar licencia, referencias, vínculos, tests y dependencias de todos los archivos afectados.
4. Si la skill se amplía, mantener todos los casos y documentación previa relevantes. No aceptar un resumen como reemplazo de la fuente.
5. Ejecutar los casos de evaluación de esa skill y los controles `npm run check`.
6. Preparar en **la misma PR** una actualización explícita de ambas baselines si cambian identidades o hashes. Enumerar los archivos nuevos, editados o retirados y justificar cada uno.
7. Exigir revisión independiente para reemplazos, retiros o integraciones con permisos elevados. Un SHA correcto en un manifiesto actualizado sin esta revisión **no es prueba** de que el cambio sea seguro.
8. Tras aceptar el cambio, generar de nuevo los adaptadores con `npm run agents:build` y comprobar que no aparece deriva.
9. No fusionar ni publicar si una prueba crítica falla o falta una restauración viable.

## Límites deliberados

- La integridad compara los **bytes rastreados** con el baseline; no inspecciona la semántica, el comportamiento en un modelo ni conexiones activas.
- Añadir una skill o un archivo de soporte sin actualizar el inventario genera FAIL. Esto obliga a documentar explícitamente la incorporación, no a rechazarla permanentemente.
- El baseline original permanece en el historial de Git; las revisiones posteriores deben conservar referencias a versiones anteriores para recuperación.
- La configuración del PC, archivos privados ignorados y secretos requieren respaldo local seguro separado. No añadir esos datos al repositorio.
- `AGENTS.md` y `GEMINI.md` son entradas, pero el descubrimiento real de instrucciones, adaptadores y MCP debe verificarse en los clientes nativos.

**Una puntuación documental elevada o 100 % de pruebas aprobadas no equivale a un 100 % de preparación comercial.** Para este segundo objetivo hacen falta entrevistas, contratos, cobros, entregas aceptadas y costos reales.
