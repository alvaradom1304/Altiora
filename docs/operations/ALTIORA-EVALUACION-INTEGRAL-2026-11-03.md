# Altiora — evaluación integral preliminar (2026-11-03)

**Estado:** diagnóstico de preparación empresarial, no certificación de resultados ni medición de capacidad de cada agente. El porcentaje 98,3% comunicado anteriormente corresponde, según el usuario, a skills/agentes y no debe extrapolarse a la empresa completa.

## Matriz de preparación (juicio de auditoría; no benchmark estadístico)
| Dimensión | Peso | Puntuación estimada (0–100) | Evidencia / condición pendiente |
|---|---:|---:|---|
| Skills y agentes | 20% | 90 | Catálogo y roles documentados; cobertura y funcionamiento end-to-end no probados |
| Arquitectura y procesos | 15% | 85 | Router, contratos, continuidad y documentación presentes |
| QA / reproducibilidad | 15% | 80 | Scripts y CI documentados; ejecución local integral pendiente |
| Coordinación multi-IA | 15% | 60 | Router y reglas implementadas; handoff Claude–Codex–Antigravity aún sin certificación en vivo |
| Integraciones creativas y MCP | 10% | 40 | Blender render local documentado; Adobe/MCP y acceso desde cada IA por probar |
| Ventas, clientes y tracción | 20% | 15 | Registro interno confirma cero clientes de pago, cero entrevistas y cero oportunidades calificadas; ausencia de resultados aún |
| Gobierno y gestión de riesgos | 5% | 75 | Protocolo de autoridad y gates incorporado; controles de cumplimiento pendientes |
| **Preparación empresarial global estimada** | **100%** | **62,5/100** | **No equivale a probabilidad de éxito** |

Cálculo: (90×0,20)+(85×0,15)+(80×0,15)+(60×0,15)+(40×0,10)+(15×0,20)+(75×0,05) = **62,5**.

### Datos revisados
- `team/ROUTING.md`: reglas de delegación; Claude asume dirección operativa sin invalidar preferencia de IA por dominio.
- `package.json`: `npm run check`, `npm run capability:doctor`, `npm run routing:eval`, pruebas MCP y QA.
- PR #66: workflow «Check» con conclusión success sobre su commit anterior; no es prueba de instalaciones locales ni del cambio posterior en `team/ROUTING.md`.
- `docs/altiora-business/pipeline.json`: `confirmed_paying_clients: 0`, `opportunities: []`, `interviews_completed: 0` y `contacts_sent: 0`.
- Issue #65: matriz para validación en vivo de modelos, Blender, After Effects y resultados comerciales.

### Criterios para elevar la preparación
1. QA: CI verde para la rama actual y `npm run check` ejecutado en entorno real.
2. Orquestación: tres sesiones reales con handoff, evidencias, commits distintos y revisión independiente.
3. Visual: preflight real de Blender, Adobe/MCP en cada cliente; registrar salida.
4. Comercial: entrevistar El Tilichero, medir baseline, ejecutar una prueba de captación autorizada, documentar ventas y rentabilidad reales.
5. Gobierno: no fusionar/publicar/consumir recursos externos sin permisos y revisión según riesgos.

**Alcance de juicio:** solo repositorio y registros observables. Cifras de skills catalogadas o porcentajes previos no equivalen a tests funcionales. Recalcular puntuación al obtener nueva evidencia.
