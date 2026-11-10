---
name: superpowers
description: Planifica, ejecuta con TDD y verifica de forma autónoma cualquier cambio técnico antes de darlo por terminado. Aplica el Superpowers Quality Gate sin requerir intervención del usuario en pasos intermedios.
---

# Superpowers: Autonomous Engineering & Quality Loop

Esta habilidad otorga a cualquier agente la capacidad de ejecutar tareas complejas de ingeniería con rigor militar y verificación autónoma.

## Principios Operativos

1. **Planificación Quirúrgica Previa:**
   - Define el archivo exacto a editar y el comando de prueba que validará el cambio.
   - Si no existe prueba automatizada, escribe un script de verificación determinista en Python o Bash.

2. **Ejecución y Resiliencia Autónoma:**
   - Aplica cambios acotados en rangos de líneas.
   - Si el comando de verificación falla (exit code != 0), inspecciona el `stderr`, diagnostica la causa raíz y corrígela en un bucle cerrado sin detenerte a preguntar detalles de implementación al usuario.

3. **Criterios Inmutables de Entrega:**
   - La entrega solo se declara completada cuando:
     - El compilador/linter pasa con 0 errores.
     - Las pruebas o scripts de verificación concluyen con código 0.
     - El working tree de Git queda limpio y documentado.

