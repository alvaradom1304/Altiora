# 01 · Ficha de encaje: [empresa] · [fecha]

Una ficha por oportunidad. Solo datos reales del comprador. Lo que no se sepa se deja «desconocido», sin rellenarlo con suposiciones. El registro resumido va en `docs/altiora-business/pipeline.json`.

## Comprador y decisión
- Empresa, sector y fuente pública con fecha (el foco de una campaña o piloto **no** es el sector de la empresa):
- Interlocutor y cargo · ¿decide la compra? (sí / no / desconocido):
- Cómo compran (quién aprueba, plazo, proceso):
- Presupuesto declarado por el comprador (cita textual, no inferida):

## Cobertura del negocio (BSCG)
Norma: [CONTEXT-FIRST-BSCG.md](../CONTEXT-FIRST-BSCG.md). Estados: `VERIFIED` · `REPORTED` · `INFERRED` · `UNKNOWN` · `CONFLICTED` · `OUTDATED`. Una declaración del comprador es `REPORTED`, nunca `VERIFIED`.

| Categoría o línea | Quién la declara | Revisada con una fuente específica (sí/no) | Ventas · margen · inventario (estado) |
|---|---|---|---|
| | | | |

- ¿La decisión afecta a toda la empresa o solo a una campaña o producto?:
- Categorías que existen en la documentación pero no se han revisado:
- Resultado del BSCG (`bscg.py`): PASS / CONDITIONAL / HOLD. Si la decisión afecta a toda la empresa, la documentación de una sola campaña no permite PASS.

## Problema (con sus palabras)
- Episodio reciente concreto (fecha aproximada, qué pasó):
- Proceso actual (cómo lo hacen hoy y con qué herramientas):
- Volumen con sus datos (p. ej., consultas al mes):
- Qué intentaron antes y por qué no funcionó:

## Valor que justifica el precio
El comprador cuantifica el coste del problema con sus propios datos. Altiora no lo estima por él.

| Concepto | Valor declarado | Fuente (cita o documento) |
|---|---|---|
| Consultas u oportunidades perdidas al mes | | |
| Valor medio de una oportunidad | | |
| Horas internas dedicadas al seguimiento manual | | |
| Otro coste que mencionen | | |

Si el comprador no puede o no quiere cuantificarlo, **G1 queda en HOLD**. No se calcula retorno con supuestos de Altiora, ni se promete.

## Resultado, alcance y exclusiones
- Resultado del recorrido que se comprometería (de la página comercial al registro, la asignación, el aviso y la medición):
- ¿Cabe en el alcance base de `OFERTA.md`? (sí / no; si no, qué sobra):
- Exclusiones que hay que decir explícitamente desde el principio:
- Dependencias de terceros (CRM, WhatsApp, correo, hosting) y quién las controla:

## Criterios de aceptación propuestos (verificables)
1. 
2. 
3. 

## Compuerta G1 · Proponer
| Criterio | Cumple | Evidencia |
|---|---|---|
| Problema reciente y concreto | | |
| Coste del problema cuantificado por el comprador | | |
| Decisor identificado y presupuesto declarado | | |
| Alcance dentro de la oferta y de la capacidad libre | | |
| Siguiente paso consentido con fecha | | |

Veredicto: GO / HOLD / NO-GO · fecha · decide:
