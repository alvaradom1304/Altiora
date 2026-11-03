# Context First · Discovery inteligente y control de cobertura (BSCG)

Versión 1 · 2026-11-03 · V7, complementa V5 y V6. Aplica a todo cliente, proyecto y agente antes de recomendar, diseñar o ejecutar. Regla de fondo: **primero comprender, después decidir, finalmente ejecutar.** Es proporcional: una tarea pequeña no exige una auditoría empresarial.

Piezas: este protocolo (norma), `scripts/bscg.py` (verificador), `scripts/test_bscg.py` (regresión), la sección «Cobertura del negocio» de [01-ficha-encaje](plantillas/01-ficha-encaje.md) y la skill `aem-stage-01-discovery`. Primer caso: [El Tilichero](../../../projects/tilicheros/CONTEXTO-NEGOCIO.md).

## 1. Orden de trabajo
1. **Recuperar** lo que ya existe: brief, discovery, decisiones, checkpoint, evidencia. No se reinicia un Discovery completado salvo evidencia de que está incompleto, desactualizado o contradicho.
2. **Clasificar** lo que se sabe con la matriz de la sección 2.
3. **Investigar** lo verificable (repositorio, documentos, fuentes públicas autorizadas) antes de preguntar.
4. **Preguntar** solo lo que sigue desconocido y cambia una decisión (sección 4).
5. **Pasar el BSCG** (sección 5) antes de aprobar una estrategia que afecte a la empresa entera.
6. **Ejecutar** con criterios de aceptación y **aprender** (sección 7).

## 2. Matriz de conocimiento
| Estado | Significado |
|---|---|
| `VERIFIED` | Comprobado con evidencia confiable (documento, medición, registro). Una declaración del cliente **no** es `VERIFIED` |
| `REPORTED` | Lo dijo el cliente o el fundador |
| `INFERRED` | Deducción razonable, sin confirmar |
| `UNKNOWN` | No hay información. Ausencia de dato no es ausencia del hecho |
| `CONFLICTED` | Hay fuentes que se contradicen |
| `OUTDATED` | Pudo cambiar desde la fecha de la fuente |

Cada dato importante lleva: afirmación, estado, fuente, fecha, confianza, impacto si es incorrecto y método de validación. Nunca se pasa `REPORTED` a `VERIFIED` ni `INFERRED` a hecho sin una nueva evidencia citada.

## 3. Contexto que se recupera (proporcional a la decisión)
- **Empresa:** actividad, modelo de negocio, mercado, categorías, segmentos, canales, propuesta de valor, competidores, operación y logística, recursos, situación financiera conocida, objetivos, restricciones, riesgos.
- **Digital** (si aplica): web, redes, catálogo, experiencia del cliente, reputación pública, herramientas, analítica.
- **Interno de Altiora:** brief, discovery, decisiones, documentos canónicos, estado, entregables, evidencia, agentes y skills relacionados.
- La información pública no equivale a datos internos de la empresa.

## 4. Preguntar antes de suponer
Cuando falte un dato que puede cambiar una decisión material (alcance real, categorías, objetivos, presupuesto, márgenes, inventario, público, autorizaciones, derechos, riesgos legales, criterios de éxito), el agente se detiene en esa decisión y pregunta. Cómo:
1. Preguntas breves y específicas; primero las que más cambian la decisión.
2. Decir por qué se necesita el dato.
3. No preguntar lo ya documentado (buscar antes).
4. Agrupar las relacionadas e indicar **qué puede avanzar mientras tanto**.

No saber algo no es una falla; ocultarlo con suposiciones sí.

| Ejemplo | Texto |
|---|---|
| Incorrecto | «El negocio vende sobre todo X, así que construimos la estrategia en torno a X» |
| Correcto | «Encontré una campaña de X, pero también referencias a otras categorías. No tengo cifras que digan cuál lidera las ventas. Antes de elegir qué impulsar necesitamos confirmar el portafolio y su rentabilidad» |

## 5. BSCG · Business Scope Coverage Gate
Se aplica antes de aprobar una estrategia que afecte a **toda** la empresa. Diez criterios, cada uno `SI`, `PARCIAL` o `NO`:

| # | Criterio | Cómo se determina |
|---|---|---|
| 1 | Modelo de negocio identificado | manual, con evidencia |
| 2 | Todas las categorías conocidas revisadas | **calculado**: categorías con `revisada: true` ÷ total |
| 3 | Productos o servicios principales identificados | manual |
| 4 | Hechos y supuestos diferenciados | manual y **calculado**: ninguna afirmación no fiable en la decisión |
| 5 | Objetivos conocidos | manual |
| 6 | Decisores identificados | manual |
| 7 | Riesgos importantes investigados | manual |
| 8 | Datos suficientes para priorizar | **calculado**: ventas y margen de cada categoría en `VERIFIED` o `REPORTED` |
| 9 | Alternativas evaluadas | manual |
| 10 | La solución responde al negocio completo o solo a una parte | **calculado** según el alcance de la decisión |

Resultado:
- **PASS:** alcance suficientemente comprendido para la decisión solicitada.
- **CONDITIONAL:** alcance parcial; solo tareas compatibles con esa limitación.
- **HOLD:** faltan datos críticos para decidir.

Criterios críticos: para una decisión de `empresa_completa`, los criterios 1, 2, 5, 6, 8 y 10; para `campana` o `producto`, los criterios 4, 5 y 6. Un crítico en `NO` da **HOLD**; un crítico en `PARCIAL`, cualquier otro criterio que no sea `SI`, o una afirmación no fiable usada en la decisión, da **CONDITIONAL**. El verificador rechaza (HOLD) lo que se declara `SI` pero los datos contradicen, y rechaza un `VERIFIED` sustentado solo en una declaración. **No se marca PASS usando documentación de una sola campaña cuando la decisión afecta a toda la empresa.**

**Límite del verificador:** comprueba coherencia interna, no veracidad. Los datos del archivo son entrada manual y el resultado lo declara (`entrada: MANUAL_NO_VERIFICADA`); que una fuente exista o diga lo anotado lo comprueba una persona. Un criterio manual `SI` sin evidencia citada cuenta como `PARCIAL`, y un `VERIFIED` sin fuente citada es un error.

Uso: `python docs/altiora-business/entrega/scripts/bscg.py <archivo.json>` (códigos de salida: 0 PASS, 10 CONDITIONAL, 20 HOLD, 2 entrada inválida). Formato de entrada: ver `projects/tilicheros/COBERTURA-NEGOCIO.json`.

## 6. Revisión adversarial
Antes de una estrategia importante y con riesgo que lo justifique, un revisor distinto del autor cuestiona: qué se da por cierto; qué dato contradice la hipótesis; si se prioriza algo solo porque ya se construyó; qué categorías se ignoran; si se confunde popularidad con rentabilidad; qué datos faltan; qué alternativa podría ser mejor; qué evidencia refutaría la recomendación. No se declara «revisión independiente» si la hizo el mismo modelo sin separación suficiente; en ese caso se etiqueta **parcial**.

## 7. Aprendizaje y prevención
Si una decisión falla por contexto incompleto: (A) registrar el incidente (qué pasó, qué supuesto lo causó, qué evidencia se ignoró, impacto, qué control debió detectarlo); (B) corregir la plantilla o skill responsable; (C) añadir una prueba de regresión; (D) ejecutarla y anotar PASS o FAIL. Una política escrita no cierra el incidente: lo cierra la prueba. Caso obligatorio de regresión: El Tilichero (`scripts/test_bscg.py`).

## 8. Ejecución adaptativa
| Clase | Qué incluye |
|---|---|
| Puede avanzar | investigación, preparación, prototipos internos, organización, análisis preliminar |
| Debe esperar confirmación | priorización comercial definitiva, presupuestos, campañas con afirmaciones no verificadas, decisiones irreversibles |
| Debe detenerse | riesgos críticos de seguridad, legales, financieros o de privacidad |

Un dato pendiente no bloquea el resto del trabajo independiente.

## 9. Límites
Este protocolo no crea agentes ni skills nuevas, no cambia permisos ni credenciales y no mide ahorro de tokens. Un PASS del BSCG no aprueba publicar, cobrar, gastar ni contactar a terceros.
