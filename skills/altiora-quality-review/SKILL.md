---
name: "altiora-quality-review"
description: "Revisa cambios de Altiora contra el encargo, las funciones afectadas y su evidencia de prueba. Se usa para comprobar una entrega o una tarea de otro agente antes de integrarla."
metadata:
  version: 1.2.0
---

# Revisión de entregas de Altiora

Recibir el brief, los archivos cambiados y las comprobaciones declaradas. Inspeccionar el resultado real. No dar por pasada una prueba solo porque el agente implementador la mencione.

Escoger verificaciones según el riesgo y las funciones afectadas. Para una web: navegación, móvil, teclado y formulario o pedido relevante. Para una escena: carga, movimiento reducido y alternativa sin WebGL. Para un catálogo o skill: rutas, formato, fuentes y correspondencia entre descripción y comportamiento.

Dar prioridad a fallos reproducibles que afecten al objetivo. Devolver para cada uno impacto, ubicación, forma de observarlo y corrección concreta. No reabrir decisiones aceptadas ni exigir refactorizaciones o pruebas sin relación con el cambio.

Cuando falte una capacidad de ejecución, indicar qué se pudo inspeccionar y qué sigue pendiente. Diferenciar objetivos de rendimiento, ejemplos ficticios y resultados medidos.

Terminar con una de estas conclusiones, apoyada en evidencia: cumple lo comprobado; necesita correcciones concretas; o falta una comprobación identificada. Revisar un cambio no concede autorización para publicarlo o fusionarlo.


## Laboratorio disponible en este equipo
Para localizar las fuentes y proyectos de Altiora, consultar [la ubicación local](references/altiora-workspace.md) cuando sea pertinente.

## Ingeniería: método ECC adaptado
Para revisar ingeniería sustancial, consultar [verificación y evaluación](references/ecc-workflow.md). Reutiliza los controles actuales; no instala ECC ni duplica agentes.
