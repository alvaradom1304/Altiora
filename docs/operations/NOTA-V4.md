# Nota de preparación empresarial V4

Una sola nota para Claude, Codex, Antigravity y Gemini. Se obtiene con `npm run readiness:report -- --resumen` y se cita tal cual, con su fecha. No se estima a ojo.

**No confundir con la nota de skills.** El 98,3/100 de `quality/skills-report.md` mide la redacción de las skills (estructura y verificabilidad). No mide si Altiora opera ni vende. Se cita aparte y con esa etiqueta.

## Ejes y pesos

| Eje | Peso | Condición para una nota alta |
|---|---:|---|
| Integridad, historia y recuperación | 20 | Verificación de contenido y restauración comprobada |
| Automatización, agentes y QA | 15 | Pruebas pasando y tareas reales aceptadas con revisión independiente |
| Conectores y acceso en vivo | 15 | Pruebas autenticadas de cada cliente nativo |
| Demanda y ventas | 25 | Problema validado, acuerdos, ventas y cobros verificables |
| Calidad de entregables | 15 | Entregas aceptadas por clientes, accesibles y estables |
| Economía y capacidad | 10 | Horas, costes y márgenes medidos en proyectos reales |

Nivel de cada eje, de 0 a 5: 0 sin evidencia, 1 diseñado, 2 parcial, 3 probado en entorno controlado, 4 probado en entorno real, 5 repetidamente validado con clientes. Nota = suma(peso × nivel / 5).

## Cómo se calcula

El script lee `quality/readiness-evidence.json` y `docs/altiora-business/pipeline.json`. Cada nivel queda limitado por tres cosas:

- **El tipo de evidencia.** `design` sostiene hasta 1, `partial` hasta 2, `test` hasta 3 y `real` hasta 4. Un 5 exige dos evidencias `real` con fechas distintas. Una fuente que no existe no cuenta.
- **Los hechos de `pipeline.json`, en demanda.** Sin contactos enviados el tope es 1; con contactos, 2; con entrevistas u oportunidades, 3; con un cliente de pago, 4; con dos o más, 5.
- **Los fallos críticos abiertos (`p0_open`).** Mientras haya uno, la calidad de entregables no pasa de 2.

La decisión es `HOLD_SCALE` si hay un fallo crítico abierto o la demanda está por debajo de 2; `READY_FOR_PILOT` si los entregables llegan a 3; y `READY_FOR_REPEATABLE_DELIVERY` si demanda y entregables llegan a 4 y la economía a 3.

## Cómo se sube la nota

Se añade evidencia al registro (una acción con fuente y fecha). No se edita el número. Los ejemplos más rápidos: enviar la Ronda 1 de correos sube la demanda a 2; cerrar los tres fallos críticos desbloquea los entregables; registrar costes reales sube la economía.
