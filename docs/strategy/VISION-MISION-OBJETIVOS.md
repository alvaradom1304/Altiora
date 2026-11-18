# Altiora · visión, misión y objetivos

Fecha: 2026-11-02. Estado: **propuesta para aprobación del fundador**. Integra la definición confirmada ([POSICIONAMIENTO](../altiora-business/POSICIONAMIENTO.md)), la intención del fundador ([experiencia total](../altiora-business/ESTANDAR-EXPERIENCIA-TOTAL.md)), la [oferta de US$10.000](../altiora-business/OFERTA.md) y los [paquetes](PAQUETES-BORRADOR.md). Ningún precio está validado con compradores y hay cero clientes de pago (`pipeline.json`).

## Visión

**Que cualquier empresa con un buen producto pueda dar a sus clientes una experiencia de marca y de compra de primer nivel, y demostrarlo con números.**

## Misión

**Diseñamos e implementamos la experiencia completa de compra de nuestros clientes, desde la primera impresión hasta el pago y la recompra. Cada proyecto se entrega con dos resultados medidos: uno para el negocio y otro para su consumidor.**

## Promesa: la doble experiencia

Antes de proponer una solución, cada proyecto firma dos resultados ([estándar](../altiora-business/ESTANDAR-EXPERIENCIA-TOTAL.md)):

| Para la empresa que nos contrata | Para el consumidor de esa empresa |
|---|---|
| Sabe qué compra, cuánto cuesta, quién responde y cuándo se entrega. | Entiende la propuesta y puede elegir sin fricción. |
| Ve avances y decisiones; recibe un sistema que puede operar sin nosotros. | Pasa del anuncio a la compra, la entrega y el soporte sin cortes. |
| Conoce qué cambió en un indicador suyo y qué no se pudo medir. | Encuentra ayuda cuando algo falla, en móvil y con teclado. |

"Total" significa **coherencia en cada punto de contacto, no alcance ilimitado**. La profundidad se pacta y se presupone en cada proyecto: el margen mínimo es del 25 % con un tope de 75 h ([FINANZAS](../altiora-business/FINANZAS.md)).

## Escalera de valor: cómo se llega al high ticket

El ticket alto se gana con casos medidos. Cada escalón fabrica la prueba que vende el siguiente.

| Escalón | Para quién | Precio de referencia (sin validar) | Qué debe dejar |
|---|---|---|---|
| **1. Entrada Cash-First** | Negocios que empiezan (El Tilichero, La Central del Queso) | Comisión sobre ventas o diagnóstico pagado pequeño | Un caso con antes y después medido, y testimonio autorizado |
| **2. Núcleo** | Pymes con flujo de pedido por catálogo o WhatsApp | US$3.000–5.000 ([Paquete 1](PAQUETES-BORRADOR.md)) | Entregas aceptadas y horas reales frente a lo planificado |
| **3. High ticket** | Empresas donde una consulta perdida vale más que el proyecto (B2B de servicios) | US$10.000 ([OFERTA](../altiora-business/OFERTA.md)) | Recorrido comercial completo, aceptado y medido |
| **4. Recurrente** | Clientes de los escalones 2 y 3 | Cuota por calcular | Ingresos previsibles sin depender de proyectos nuevos |

**Regla:** no se vende un escalón sin la prueba del anterior. El escalón 3 exige al menos dos casos medidos de los escalones 1 o 2. Mientras tanto, la Ronda 1 de entrevistas valida el problema del público B2B sin venderle todavía.

## Valores

- **Evidencia antes que opinión.** Lo que no se puede comprobar no se promete.
- **El pedido primero.** Ninguna experiencia visual puede romper el camino a la venta.
- **Cash-First.** Al cliente que empieza se le ayuda a ganar antes de venderle lo premium.
- **Honestidad comercial.** Sin escasez falsa, sin testimonios inventados y sin garantizar ventas.

## Objetivos (propuestos; las fechas cuentan desde la aprobación)

| # | Objetivo | Meta medible | Plazo | Cómo se comprueba |
|---|---|---|---|---|
| 1 | Cerrar los riesgos abiertos | LCQ en producción con el número oficial; claves revocadas; un solo proyecto de Vercel | 2 semanas | `curl` del sitio; P0 vacíos en `quality/readiness-evidence.json` |
| 2 | Validar demanda B2B | 8 entrevistas cualificadas | 3 semanas desde el envío | `pipeline.json` |
| 3 | Primer ingreso | Primer pago de comisión de El Tilichero o primera propuesta firmada | 30 días | Cobro registrado |
| 4 | Primer caso medido | Antes y después de LCQ o El Tilichero, con ambos resultados (negocio y consumidor) | 60 días | Informe con la aceptación del dueño |
| 5 | Economía real | Costes fijos y horas por proyecto registrados | 2 semanas | `FINANZAS.md` |
| 6 | Preparación | Nota V4 de 40 a 53 (`READY_FOR_PILOT`) y luego a 80 | 30 / 90 días | `npm run readiness:report -- --resumen` |
| 7 | Primer high ticket | Un proyecto del escalón 3 firmado y con anticipo | Tras dos casos medidos | Contrato y anticipo |

## Cómo se usa este documento

Ante cada encargo nuevo se preguntan tres cosas:
1. ¿Mejora a la vez la experiencia de la empresa y la de su consumidor?
2. ¿Acerca a un cobro o a un caso medido?
3. ¿Cabe en el margen?

Si alguna respuesta es "no", el encargo se replantea o se descarta.
