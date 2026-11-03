# Sistema de entrega de Altiora · proceso por fases

Para vender y entregar un proyecto de unos US$10.000 en seis semanas, con mantenimiento mensual opcional que se presupuesta aparte. **Estado: hipótesis de proceso, sin ninguna entrega de pago que la valide** (0 clientes de pago a 31/10/2026). Las condiciones comerciales salen de [OFERTA.md](../OFERTA.md) y las cifras de [FINANZAS.md](../FINANZAS.md). Este paquete no las repite: las convierte en pasos, plantillas y compuertas. Diagnóstico y prioridades en [EVALUACION-2026-10-31.md](EVALUACION-2026-10-31.md).

**Alcance del proceso:** las fases, compuertas y controles sirven para cualquier proyecto de Altiora de ese tamaño. Siguen el método de [POSICIONAMIENTO.md](../POSICIONAMIENTO.md): diagnosticar, priorizar, diseñar, implementar, medir y mejorar. Los entregables y criterios de ejemplo de las plantillas 02, 05 y 06, y la sección B de la aceptación, corresponden al paquete piloto de recorrido web de `OFERTA.md`. En un proyecto de marca, ventas u operación se sustituyen por los entregables de ese proyecto, cada uno con su criterio verificable. Las compuertas, el presupuesto de horas, el control de cambios, los derechos y el acta no cambian.

## Cómo usarlo (5 minutos)

1. Copia `plantillas/` en la carpeta del proyecto, en `docs/proyecto/`. Así cada cliente tiene sus propios documentos y estas plantillas no se tocan.
2. Avanza fase por fase. Una fase se cierra con su **compuerta**: GO, HOLD o NO-GO, con evidencia y fecha. Si hay un bloqueo crítico no se avanza, sea cual sea la puntuación total.
3. Registra cada prueba y cada decisión con **fecha, versión** (commit, URL de vista previa o manifiesto) y **archivos**. Lo que no se pudo comprobar se marca NO VERIFICADO, explicando qué falta.
4. La aceptación final se revisa con [ACEPTACION.md](ACEPTACION.md). Los riesgos del sistema están en [RIESGOS.md](RIESGOS.md). Hay un ejemplo aplicado, no comercial, en [EJEMPLO-PILOTO.md](EJEMPLO-PILOTO.md).

## Responsables

| Rol | Quién | Responde de |
|---|---|---|
| Director/a de proyecto | Una persona de Altiora; hoy, el fundador | Alcance, calendario, horas, compuertas, comunicación y aprobación de cada entrega. Firma los compromisos. |
| Decisor del cliente | Una sola persona, nombrada en la propuesta | Materiales, accesos, consolidar comentarios, aprobaciones y aceptación |
| Responsable técnico | Persona de Altiora; puede ser el director | Construcción, integraciones, cuentas y documentación técnica |
| Revisor independiente | Persona o agente distinto de quien construyó | Pruebas y veredicto de calidad; nunca revisa su propio trabajo |
| Asesoría legal y contable | Profesionales externos de la jurisdicción. Hoy pendientes: no hay ninguno contratado | Contrato, propiedad intelectual, privacidad, impuestos y facturación |

Las IAs apoyan a estos roles: coordinan `altiora-commercial-director` y `altiora-project-director`, y hay agentes en `.claude/agents`. No sustituyen la decisión humana, no tienen habilitación profesional y no cuentan como capacidad contratada.

## Fases, plantillas y compuertas

| Fase · semana | Etapa | Plantilla | Responsable · apoyo IA | Compuerta para avanzar |
|---|---|---|---|---|
| F0 Encaje · antes de contratar | 1. Diagnóstico y venta | [01-ficha-encaje](plantillas/01-ficha-encaje.md) y [CONTEXT-FIRST-BSCG](CONTEXT-FIRST-BSCG.md) | Director · `altiora-commercial-director`, `mom-test-interviewing`, `sales-discovery` | **G1 Proponer:** problema reciente con impacto que el comprador cuantifica, decisor y presupuesto declarados, alcance que cabe en la oferta |
| F1 Propuesta · antes de contratar | 2. Propuesta y contrato | [02-propuesta-alcance](plantillas/02-propuesta-alcance.md) | Director · `sales-proposal`, `copy-editing`; asesoría legal | **G2 Iniciar:** estimación ≤ presupuesto de horas (F2), contrato revisado y firmado, anticipo de US$5.000 **recibido** |
| F2 Inicio · semana 1 | 3. Planificación | [03-plan-presupuesto](plantillas/03-plan-presupuesto.md) | Director · `altiora-os-strategy`, `unit-economics` | **G3 Plan aprobado:** materiales y accesos mínimos recibidos, calendario con las decisiones del cliente, riesgos con responsable |
| F3 Definición · semana 2 | 4. Estrategia y experiencia | [05-brief-experiencia](plantillas/05-brief-experiencia.md) | Director · agentes `altiora-experience`, `altiora-os-creative`; `site-architecture` | **G4 Alcance congelado:** recorrido, estructura, diseño y responsables del contenido aprobados por escrito → cobro de US$3.000 |
| F4 Construcción · semanas 3–4 | 5. Producción | [07-registro-activos](plantillas/07-registro-activos.md), [04-control-cambios](plantillas/04-control-cambios.md) | Responsable técnico · `altiora-engineering`, `test-driven-development` | **G5 Listo para revisión:** recorrido completo con datos de prueba, todos los activos con derechos registrados y demo semanal hecha |
| F5 Revisión técnica · semana 5 | 6. Calidad | [06-plan-pruebas-evidencia](plantillas/06-plan-pruebas-evidencia.md) | Revisor independiente · `altiora-os-qa`, `web-quality-assurance`, `accessibility` | **G6 Sin bloqueos críticos:** pruebas registradas y manifiesto creado de la versión candidata |
| F6 Entrega · semana 6 | 7. Lanzamiento y traspaso | [08-acta-aceptacion-traspaso](plantillas/08-acta-aceptacion-traspaso.md) | Director · `launch-readiness`, `conversion-tracking` | **G7 Aceptación expresa:** manifiesto verificado (lo entregado = lo probado), cuentas, formación y manual entregados → cobro de US$2.000 e inicio de los 14 días de corrección |
| F7 Cierre · ≤ 10 días hábiles tras G7 | 8. Rentabilidad y aprendizaje | [09-cierre-rentabilidad](plantillas/09-cierre-rentabilidad.md) | Director · `altiora-case-study` | **G8 Cerrado:** margen real calculado, mejoras llevadas a estas plantillas y caso de estudio solo con permiso del cliente |
| Mantenimiento opcional · mensual | 7–8 | [10-informe-mantenimiento](plantillas/10-informe-mantenimiento.md) | Director · `customer-success`, `attribution` | Contrato aparte; las horas consumidas se registran y se comparan con la bolsa |

Sin anticipo recibido no hay inicio: facturar no es cobrar (`FINANZAS.md:47`). La revisión de la semana 5 no es aceptación final ni inicia la garantía (`OFERTA.md:25`).

## Presupuesto de horas (aprobado el 31/10/2026; el esfuerzo real aún no se ha medido)

El fundador aprobó planificar cada proyecto con **75 h**. Es el máximo compatible con un margen económico del 25 % (E/P) usando D = US$3.000, R = US$750 y US$50/h (`FINANZAS.md:35`). Con 90 h ese escenario daría 17,5 %. Si los costes D o R reales difieren, se recalcula el techo antes de firmar. Lo que se aprobó es el presupuesto; que el trabajo quepa en 75 h se comprobará en el cierre del primer proyecto (plantilla 09).

| Fase | h |
|---|---:|
| F2 Inicio y plan | 6 |
| F3 Definición | 12 |
| F4 Construcción | 28 |
| F5 Revisión técnica y correcciones | 8 |
| F6 Entrega, formación y manual | 7 |
| Gestión y comunicación (6 semanas) | 7 |
| Corrección en los 14 días de garantía | 4 |
| F7 Cierre | 3 |
| **Total** | **75** |

F0 y F1 se imputan a ventas, dentro de las 40 h de ventas y administración del bloque (`FINANZAS.md:53`), no al proyecto. Si la estimación de la F1 supera 75 h, G2 queda en NO-GO hasta reducir el alcance o cambiar el precio. Una desviación semanal de más del 15 % sobre lo planificado en una fase obliga a decidir en esa misma semana: recortar, usar contingencia o pedir un cambio aprobado. Ese 15 % es un umbral propuesto, sin medir todavía.

## Reglas que no cambian

- Contactar, publicar, gastar, firmar, instalar o conectar servicios reales exige autorización expresa y específica.
- No se prometen ventas, posicionamiento ni retorno. Los objetivos medibles son del recorrido entregado.
- 3D, vídeo, audio, más integraciones o más idiomas no entran en el alcance base: se tratan como cambio (plantilla 04), con estimación y aprobación.
- Las cuentas, accesos y documentación quedan bajo control del cliente.
- Para el detalle técnico de la calidad se reutiliza la Definition of Done y los presupuestos de rendimiento del laboratorio (`quality/` en la raíz del repo). No se copian aquí.

## Herramienta incluida

`scripts/manifiesto.py` crea y verifica huellas SHA-256 de los archivos de una entrega. Usa el formato de [PILOT-SOURCE-MANIFEST.json](../PILOT-SOURCE-MANIFEST.json), solo la biblioteca estándar de Python, y nunca escribe en el proyecto que verifica.

```bash
python docs/altiora-business/entrega/scripts/manifiesto.py crear --root <proyecto> --salida <manifiesto.json> <archivo-o-carpeta>...
```

```bash
python docs/altiora-business/entrega/scripts/manifiesto.py verificar --manifiesto <manifiesto.json>
```
