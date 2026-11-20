# Revenue Sprint 30/60/90 — Altiora

**Estado:** plan propuesto, no evidencia de ventas. **Objetivo:** pasar de capacidad técnica a ingresos verificables con riesgo financiero controlado. Complementa [la política Zero-Loss](../operations/ALTIORA-SCALE-ZERO-LOSS-V4.md), [la oferta](OFERTA.md), [las finanzas](FINANZAS.md) y [el pipeline](pipeline.json).

## Línea base (revalidar antes de ejecutar)

El registro `pipeline.json` declara cero clientes de pago confirmados y ningún contacto enviado; las ocho empresas investigadas **no** son leads calificados. El precio objetivo de US$10.000, mantenimiento opcional y 75 horas por proyecto son hipótesis de planificación. No publicar estas hipótesis como resultados.

## Segmentos y arquitectura de ofertas

| Perfil del cliente | Problema a validar | Entrada comercial proporcionada | Cuándo avanzar |
| --- | --- | --- | --- |
| Microempresa sin caja | Demanda, ventas, cobros y capital de trabajo | Diagnóstico acotado y sprint Cash-First con actividades orgánicas, seguimiento comercial y control de contribución por venta | Ventas/cobros y contribución demostrados |
| Pyme con demanda | Fugas de captación, conversión o seguimiento | Auditoría del recorrido de solicitud → responsable → respuesta; intervención pequeña medible | Mejora validada, costos aceptables |
| Empresa con capacidad de invertir | Experiencia de marca, conversión, sistemas o analítica con impacto medible | Proyecto por etapas; costo total, alcance, aceptación y soporte definidos | Comprador, presupuesto, capacidad y valor demostrados |

No imponer precio ni solución por categoría. El modelo de intermediación bajo pedido exige acuerdo de liquidación, garantía, devoluciones y gestión de entrega; pago contra entrega no elimina necesidad de capital salvo que se pacte con el proveedor.

## Días 1–30: probar necesidad antes de vender una plataforma

1. Elegir **un** segmento accesible mediante hechos del mercado y capacidad de contacto legítimo; registrar por qué se eligió y por qué se descartan alternativas.
2. Preparar 8–12 invitaciones personalizadas **en borrador**, nunca enviarlas sin autorización. Revisar canales y consentimiento.
3. Completar entrevistas con responsables del problema; registrar un caso real reciente, impacto económico, solución actual, decisor, restricciones y objeciones en `interview-template.json`.
4. Identificar problemas repetidos y hacer una propuesta acotada solo cuando exista encaje. Registrar pérdidas y negativas, no solo validaciones positivas.
5. Probar el piloto de La Central del Queso con datos sintéticos, rutas de pedido y fallback; no declarar conversiones ni automatización de producción sin pruebas.
6. Revisar el tiempo real disponible, costos de herramientas y liquidez de Altiora para no comprometer entregas inviables.

**Gate 30:** entrevistas reales registradas; al menos una hipótesis comercial con problemas documentados; capacidad de preparar una propuesta individual y demostrar un recorrido. Si no se cumplen, cambiar segmento o hipótesis, no ampliar el stack.

## Días 31–60: conseguir una primera entrega remunerada

1. Presentar propuestas individuales con objetivo, exclusiones, costos, hitos, aceptación, condiciones de cobro y responsabilidades.
2. Evitar ofertas sobredimensionadas: iniciar un sprint comercial pequeño cuando el cliente todavía no necesita una web compleja.
3. Ejecutar una única entrega principal hasta medir horas, fallos y costos reales; usar QA independiente.
4. Registrar aceptación explícita, factura, desembolsos y cobros en sistemas apropiados; nunca en un README público con datos privados.
5. Convertir desviaciones recurrentes en correcciones a SOPs y skills mediante loops limitados y pruebas.

**Gate 60:** al menos una entrega real contratada/aceptada y su cobro verificable son metas de validación, no promesas. Si no se logra, diagnosticar qué paso del embudo falló antes de contratar herramientas.

## Días 61–90: repetir lo que ya demostró valor

1. Calcular margen por servicio y capacidad (incluyendo horas reales del fundador, adquisición, revisiones, licencias y soporte).
2. Crear un caso de estudio solo con permiso, métricas comprobadas y límites claros.
3. Mejorar plantillas de ventas, discovery y entregas; medir reuso de skills, retrabajo y tiempo sin perder calidad.
4. Proponer mantenimiento solo cuando tenga valor y alcance real para el cliente.
5. Evaluar la segunda entrega en paralelo únicamente cuando el primer proceso sea reproducible.

**Gate 90:** repetibilidad de adquisición/entrega, calidad estable y margen real de la primera(s) entrega(s); sin ello, seguir validando antes de escalar costos fijos.

## Scorecard semanal (registrar datos observados)

| Métrica | Definición | Fuente |
| --- | --- | --- |
| Conversaciones calificadas | Diálogos reales con problema definido y permiso | CRM / notas consentidas |
| Propuestas presentadas | Ofertas individuales realmente enviadas | Registro comercial |
| Clientes contratados | Contrato/aceptación formal | Sistema privado |
| Dinero cobrado | Entrada bancaria conciliada, no facturación | Contabilidad |
| Contribución | Cobros netos atribuibles menos desembolsos variables | Finanzas |
| Horas por entrega | Horas reales de ejecución y corrección | Timesheet |
| Aceptación y defectos | Verificación acordada, incidencias y correcciones | QA |
| CAC estimado | Costos comerciales / nuevos clientes de pago, cuando el denominador sea válido | Registro de costos |

**Responsables:** Growth genera la hipótesis; Business Architect y Finanzas verifican capacidad y margen; Creative/Engineering construyen; QA revisa; el fundador autoriza contacto, gasto, precios finales y contratos.

**No hacer:** inventar tracción, llenar pipelines ficticios, activar publicidad de pago por defecto, publicar materiales de clientes sin autorización, llamar una prueba sintética 'venta' o usar un porcentaje de skills como readiness comercial.
