# Altiora OS — Estándar de funcionamiento verificable (Quality Gate v1)

**Estado:** propuesta normativa para integrar en el flujo de entregas. **Alcance:** todas las solicitudes de estrategia, análisis, software, automatización, creatividad y consultoría. No equivale a una garantía de resultados comerciales.

## Principio
Altiora se compromete con la diligencia, la evidencia, la seguridad y criterios de aceptación acordados; nunca promete que toda solución producirá resultados externos garantizados. Una entrega no se declara «funcionando» solo porque haya código, documentos o agentes configurados.

## Definición operativa de «funcionar»
Cada proyecto debe registrar, antes de ejecutarse:
1. **Resultado esperado:** problema, usuario beneficiario y objetivo empresarial concreto.
2. **Criterios de aceptación medibles:** métricas y umbrales acordados (por ejemplo, respuesta HTTP válida, flujo completo, integridad de datos, claridad del análisis o aprobación del cliente).
3. **Entorno y dependencias:** accesos, presupuesto, herramientas, datos y restricciones comprobados.
4. **Pruebas y evidencias:** test automatizado o revisión humana trazable, según riesgo; enlaces, logs saneados o capturas sin secretos.
5. **Responsable y fecha de revisión:** quién valida y bajo qué condiciones se reabre una entrega.

## Puertas de calidad (gates)
- **G0 Discovery:** necesidad real, capacidad económica, riesgos, baseline y permisos; si falta información crítica, registrar la hipótesis.
- **G1 Strategy:** propuestas priorizadas por impacto, coste, liquidez, viabilidad y evidencia. No obligar al cliente a comprar tecnología innecesaria.
- **G2 Build:** implementation plan compatible con arquitectura existente; seguridad, mínimo privilegio, privacidad, accesibilidad y reversión.
- **G3 QA:** verificar criterios de aceptación con pruebas positivas, negativas y de regresión; documentar defectos e incertidumbres. Para estrategias, revisar fuentes, supuestos, escenarios y coherencia económica.
- **G4 Delivery:** prueba reproducible o validación documentada del cliente; instructivo de operación, límites conocidos y soporte definido.
- **G5 Outcomes:** medir después de implementar contra baseline, según ventana pactada; distinguir entregable correcto de resultado de negocio, pues ventas y crecimiento dependen también de factores externos.

## Semáforo de decisión
- **PASS:** todos los criterios críticos cumplen y hay evidencia; autorizado para entregar.
- **CONDITIONAL:** solo defectos no críticos conocidos, con aceptación explícita del responsable y plan fechado; nunca presentar como «100 % validado».
- **FAIL:** defecto crítico, falta de permisos, riesgos de seguridad, dato esencial ausente o prueba obligatoria fallida. Bloquear entrega y activar corrección.
- **NOT TESTED:** no hay evidencia; no afirmar «operativo» ni «validado».

## Loop correctivo obligatorio
FAIL → registrar defecto y severidad → asignar responsable → hipótesis de causa raíz → corregir el mínimo necesario → repetir prueba afectada + regresión → actualizar evidencia → reevaluar gate. Establecer límites de intentos, coste y tiempo según alcance; si se supera el límite, escalar a revisión humana y renegociar, nunca iterar indefinidamente.

## Rúbrica base por entrega (0–100)
- Cumplimiento de criterios pactados: **30**
- Fiabilidad y pruebas reproducibles: **25**
- Seguridad, privacidad y gestión de riesgos: **20**
- Utilidad empresarial y viabilidad económica: **15**
- Documentación y transferibilidad: **10**

**Condición de aprobación sugerida:** >= 85/100 **y** cero fallos críticos **y** evidencia de todos los criterios obligatorios. Esta puntuación es una herramienta interna; no reemplaza los criterios contractuales ni la revisión de riesgo.

## Contrato de evidencia — plantilla
```yaml
client_or_internal_project: ""
deliverable_id: ""
owner: ""
baseline: ""
acceptance_criteria:
  - id: AC-01
    condition: ""
    test_method: ""
    expected: ""
    observed: ""
    evidence_uri: ""
    status: NOT_TESTED
risk_level: medium
security_review: NOT_TESTED
qa_score: null
quality_gate: NOT_TESTED
known_limits: []
corrective_actions: []
approver: ""
review_date: ""
outcome_metrics: []
```

## Indicadores de gestión Altiora
Medir tasa de entregas PASS al primer intento, fallos escapados, tiempo de corrección, coste por entrega, cumplimiento del alcance, satisfacción, margen por proyecto y resultados empresariales **observados** (no atribuir causalidad sin evidencia).

## Integración técnica sin duplicar agentes
El orquestador de Altiora aplica este contrato antes de delegar, y cada agente entrega evidencia mínima. El QA existente evalúa G3 y G4; el equipo no debe crear un segundo QA paralelo. OmniRoute selecciona modelos, no valida por sí solo calidad. Los gates pueden implementarse gradualmente en CI y workflows, pero este documento por sí solo **no instala bloqueos automáticos ni demuestra su ejecución**.

## Regla de comunicación al cliente
Se puede prometer una metodología rigurosa, entregables evaluables, transparencia y corrección dentro de condiciones acordadas. No prometer ventas, retorno económico, ausencia absoluta de errores o funcionamiento universal garantizados.
