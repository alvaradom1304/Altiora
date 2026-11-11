# Altiora OS — Sprint de mejora con evidencia (2026-11-03)

## Objetivo
Aumentar la preparación **demostrada** de Altiora; no subir puntuaciones por documentación nueva. Baseline 62,5/100 estimado en `docs/operations/ALTIORA-EVALUACION-INTEGRAL-2026-11-03.md`. No cambiarlo sin nueva evidencia.

## Orden de ejecución (priorizar impacto x factibilidad)

| Prioridad | Trabajo | Dueño | Prueba de aceptación | Evidencia |
|---|---|---|---|---|
| P0 | Capturar SHA actual y CI para `main`; ejecutar `npm run check`, `npm run routing:eval` y `npm run capability:doctor -- --text` en checkout limpio | Codex, revisión Claude | Comandos concluyen sin errores; registrar versión, fecha y ambiente | Logs sin secretos, hashes, run URL |
| P0 | Ensayo de handoff Claude → Antigravity → Codex sobre un brief ficticio, con archivos y ramas separadas | Claude dirige | Los tres clientes ejecutan realmente y Codex verifica; sin edición simultánea | 3 sesiones, commits, pruebas, revisión |
| P1 | Probar Blender desde cada cliente (distinguir CLI y MCP); `npm run visual:preflight` | Antigravity, QA Codex | Detección real y prueba por cada IA | Versiones, artefactos, método de acceso |
| P1 | Evaluar instalación/licencia After Effects; ejecutar `npm run after-effects:setup` en modo plan, sin `--apply` automático | Claude / operador local | Plan revisado; configuración solo tras aprobación; después `after-effects:check` y `after-effects:mcp:test` | Checklist por cliente y resultado |
| P0 comercial | Discovery de El Tilichero con ventas, stock, márgenes, costos, conversiones y tiempos de atención; consentimiento para datos | ChatGPT y responsable comercial | Baseline completo, hipótesis priorizada por caja/margen | Informe privado, sin PII ni credenciales |
| P1 comercial | Experimento orgánico de 14–30 días orientado a ventas rentables y atención al cliente | Dirección humana | Medir ventas incrementales, margen de contribución, tiempo, costos y devolución | Comparación antes/después; límites y supuestos explícitos |

## Reglas
- No declarar integraciones conectadas, agentes en vivo ni clientes activos por existir scripts o documentos.
- La evidencia se clasifica: **NOT_TESTED**, **BLOCKED**, **FAIL**, **PASS**, con fecha, entorno, responsable y artefacto.
- Ninguna IA aprueba su propio código como control de QA independiente.
- No publicar, gastar, vender ni contactar clientes sin autorización específica.
- Productos compatibles o similares a marcas: descripción clara de autenticidad; nunca vender réplicas como originales ni usar afirmaciones engañosas.
- Mantener el primer piloto comercial de bajo costo. Priorizar liquidez y aprendizaje antes de automatización o anuncios.

## Fórmula de recalificación
`score = 0.20*skills + 0.15*architecture + 0.15*qa + 0.15*multi_ai + 0.10*integrations + 0.20*commercial + 0.05*governance`.
Solo aumentar una dimensión con evidencia verificable; no confundir resultado de un test aislado con validación end-to-end.
Objetivos de referencia, **no resultados obtenidos**: [95,95,95,95,90,80,95] ⇒ **91,5/100**.

## Primer checkpoint
1. Obtener evidencia de CI de `main`.
2. Completar prueba local sin secretos.
3. Registrar bloqueos de ejecución por cada cliente/IA en [issue #65](https://github.com/alvaradom1304/Altiora/issues/65).
4. Entregar Discovery resumido y ficha de indicadores de El Tilichero.
5. Recalificar únicamente dimensiones con pruebas nuevas.
