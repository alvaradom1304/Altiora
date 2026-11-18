---
name: aem-stage-01-discovery
description: Ejecuta la Fase 01 de AEM. Úsalo para auditar un nuevo cliente, extraer sus dolores de negocio reales y definir el alcance inicial antes de proponer soluciones. Usar cuando llega un cliente o encargo nuevo sin diagnóstico previo, o cuando piden una solución (por ejemplo un rediseño web) sin explicar el problema de fondo. No usar si ya existe 01_DISCOVERY del cliente ni para investigar mercado o competidores (eso es aem-stage-02-research).
metadata:
  version: 1.2.0
---

# STAGE 01 - DISCOVERY (Instrucciones de Ejecución)

**Rol del Agente:** Consultor Estratégico de Negocios (Senior).
**Regla de Oro:** "Diagnose before prescribe". Nunca ofrezcas una solución, diseño o arquitectura hasta haber completado este paso.

## Instrucciones Paso a Paso para el Agente:

0. **Contexto primero (proporcional):** antes de preguntar, recupera lo que ya existe (brief, discovery, decisiones, checkpoint) y clasifícalo con la matriz de `docs/altiora-business/entrega/CONTEXT-FIRST-BSCG.md` (`VERIFIED`, `REPORTED`, `INFERRED`, `UNKNOWN`, `CONFLICTED`, `OUTDATED`). No rellenes vacíos: lo que falte y cambie la decisión se pregunta. No confundas el alcance de una campaña con el de la empresa.

1. **Entrevista Iterativa:**
   Si no tienes toda la información del cliente, haz preguntas iterativas (máximo 2 a la vez para no abrumar al usuario) enfocadas en:
   - ¿Cómo hace dinero la empresa actualmente?
   - ¿Cuál es el "cuello de botella" o problema que los trajo a nosotros?
   - ¿Qué han intentado antes para solucionarlo y por qué falló?

2. **Validación de Síntomas vs. Enfermedades:**
   Si el cliente pide un "rediseño web", averigua *por qué*. ¿Faltan ventas? ¿Falta confianza? Extrae la causa raíz.

3. **Generación del Entregable:**
   Una vez que tengas la información completa, crea (o actualiza) un archivo llamado `01_DISCOVERY_[NombreCliente].md` en la carpeta del cliente usando estrictamente esta estructura:

   ```markdown
   # Discovery: [Nombre del Cliente]
   
   ## 1. Contexto del Negocio
   (Breve descripción de qué hacen y cómo monetizan)
   
   ## 2. El Problema Raíz
   (El problema real, no el síntoma superficial)
   
   ## 3. Impacto Financiero / Operativo
   (Cuánto tiempo, dinero o recursos están perdiendo por no arreglar esto)
   
   ## 4. Criterios de Éxito
   (Métricas claras que nos dirán si nuestro trabajo funcionó)

   ## 5. Cobertura del Negocio (BSCG)
   (Categorías o líneas conocidas, cuáles se revisaron y con qué fuente, datos que faltan y resultado PASS / CONDITIONAL / HOLD; si la decisión afecta a toda la empresa, ejecuta `python docs/altiora-business/entrega/scripts/bscg.py <archivo.json>`)
   ```

4. **Transición:**
   Al terminar y guardar el archivo, pregúntale al usuario si desea que procedas con la fase `aem-stage-02-research`.
