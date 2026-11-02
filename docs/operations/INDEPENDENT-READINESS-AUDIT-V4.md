# Protocolo de auditoría independiente V4 para Claude
**Estado:** guía de revisión; no representa una auditoría ya ejecutada.
**Objetivo:** determinar qué parte de Altiora está operativa y qué falta para vender y entregar proyectos, con pruebas que puedan reproducirse.

## Lecturas mínimas y orden
1. `docs/operations/ALTIORA-SCALE-ZERO-LOSS-V4.md`
2. `docs/operations/VERIFICACION-CONEXIONES-2026-11-02.md` (fotografía histórica, no pruebas actuales)
3. `docs/altiora-business/INICIO.md`, `FINANZAS.md`, `VALIDACION-COMERCIAL.md`, `pipeline.json`
4. `quality/skills-report.md`, `quality/definition-of-done.md`
5. `continuity/checkpoint.json`, `team/ROUTING.md`
6. `references/capability-protection-baseline-2026.json` y `references/scale-enhancement-repositories-2026.json`

**En un checkout confiable:**
```sh
git status --short
git log -1 --oneline
npm run capabilities:protect
npm run readiness:report
npm run check
```

La CI verifica regresiones y scripts; no verifica login en cuentas, calidad real de anuncios, integraciones con software del PC ni resultados comerciales.

## Protocolo de puntuación — evidencia obligatoria

| Eje | Peso | Condición para una nota alta |
| --- | ---: | --- |
| Integridad, historia y recuperación | 20 | Baseline íntegro + restauración comprobada + no pérdida semántica |
| Automatización, agentes y QA | 15 | Pruebas pasando y tareas reales aceptadas con revisión independiente |
| Conectores y acceso en vivo | 15 | Pruebas autenticadas del cliente nativo, permiso y funcionamiento |
| Demanda y ventas | 25 | Problema real validado, acuerdos, ventas y cobros verificables |
| Calidad de entregables | 15 | Entregas observadas, aceptadas, accesibles, estables y con evidencias |
| Economía y capacidad | 10 | Horas/costos medidos, márgenes reales y capacidad de entrega |
| **Total** | **100** | Solo sobre evidencia |

Calificar cada eje de 0 a 5: `0=sin evidencia`, `1=diseñado`, `2=implementación parcial`, `3=probado en entorno controlado`, `4=probado en entorno real`, `5=repetidamente validado con usuarios/clientes`. Nota ponderada = suma(peso × nota/5). Mostrar `NOT_VERIFIED` y no asignar un 5 cuando falte evidencia.

La nota documental de 98,3/100 reportada para las skills **no** es una nota de madurez de empresa ni establece la nota de estos ejes.

**Cálculo único para todas las IAs:** `npm run readiness:report` aplica esta tabla sobre [`quality/readiness-evidence.json`](../../quality/readiness-evidence.json) y `--resumen` imprime la línea que se cita. Cada evidencia declara su tipo: `design` sostiene hasta 1, `partial` hasta 2, `test` hasta 3 y `real` hasta 4. Un 5 exige dos evidencias `real` con fechas distintas, y una fuente inexistente no cuenta. Además, el script aplica topes calculados:
- **Demanda y ventas:** según `pipeline.json`. Sin contactos enviados el tope es 1; con contactos, 2; con entrevistas u oportunidades, 3; con un cliente de pago, 4; con dos o más, 5.
- **Integridad:** el tope es 1 si falla la protección de capacidades.
- **Calidad de entregables:** el tope es 2 mientras haya un P0 abierto.

**Decisión:**
- `HOLD_SCALE` si hay un P0 abierto o la demanda está por debajo de 2.
- `READY_FOR_PILOT` si la demanda llega a 2 y los entregables a 3.
- `READY_FOR_REPEATABLE_DELIVERY` si la demanda y los entregables llegan a 4 y la economía a 3.

Para subir un eje se añade la evidencia al registro. La nota no se edita a mano.

## Pruebas de no regresión
- Confirmar que siguen presentes las 355 skills protegidas, 22 roles, 5 workflows y ficheros críticos enumerados en el inventario base.
- Verificar que los adaptadores generados reflejan sus fuentes canónicas sin ejecutar modificaciones en la revisión.
- Comparar los registros de conexiones con pruebas dentro de Claude Code, Antigravity y Codex. Configurado ≠ autenticado.
- Comprobar que Graphify se usa por CLI sin reintroducir un MCP que no arrancaba.
- Inspeccionar rutas y reglas de acceso a `shared/`, sin ampliar `roots`.
- No ejecutar scripts externos ni instalar dependencias durante una simple auditoría sin autorización.

## Protocolo de negocio
- El pipeline actual declara cero clientes de pago confirmados y carece de cobros reales. No confundir hipótesis de mercado, investigación de candidatos ni entrevistas ficticias con oportunidades cualificadas.
- El precio deseado de US$10.000 todavía requiere comprador, problema, alcance, costo y prueba de disposición de pago.
- El piloto visual no acredita por sí solo ventas, retorno o seguimiento automatizado en producción.
- Cash-First debe recomendarse solo tras revisar condiciones comerciales y financieras de cada cliente.

## Salida obligatoria de Claude
1. Resultado y nota, con metodología y fecha.
2. Evidencias por eje con archivo/commit/comando o señal `NOT_VERIFIED`.
3. Hallazgos P0, P1, P2 con riesgos comerciales y técnicos separados.
4. Matriz de capacidades `LIVE_TESTED`, `CONFIGURED_NOT_TESTED`, `DOC_ONLY`, `BLOCKED`.
5. Regresiones o pérdida de conocimiento identificadas.
6. Acciones que sí elevan preparación empresarial; no premiar número de agentes o repos.
7. Decisión `READY_FOR_PILOT`, `HOLD_SCALE` o `READY_FOR_REPEATABLE_DELIVERY` basada en evidencia.

**No perseguir un 100 artificial.** La auditoría debe permitir al fundador tomar decisiones, no validar optimistamente nuestras propias afirmaciones.
