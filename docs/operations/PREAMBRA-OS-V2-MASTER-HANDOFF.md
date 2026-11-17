# PREAMBRA OS V2 — Documento maestro de integración multi-IA

> **Fecha:** 2026-11-17 · **Estado:** propuesta de arquitectura **APROBADA PARA PREPARAR IMPLEMENTACIÓN**, NO activación automática de agentes.  
> **Destino:** repositorio alvaradom1304/Altiora · **Marca comercial:** PREAMBRA · **Núcleo técnico histórico:** Altiora.  
> **Destinatario:** Claude Code (director operativo propuesto), con Codex, Antigravity, ChatGPT y Orca.  
> **Principio rector:** *No vendemos lo que hacemos. Hacemos lo que tu negocio necesita.*

## 0. Mandato ejecutivo para Claude Code

Consolida y adapta este diseño a la arquitectura **ya existente** en Altiora. No instales otro framework de orquestación ni reemplaces el router vigente por uno nuevo sin comparar sus capacidades. Primero inspecciona el código, los contratos, los tests, los permisos, las fuentes de estado y las reglas compartidas; después prepara cambios mínimos por etapas y documenta las decisiones.

**Meta real:** que un encargo iniciado desde ChatGPT, Claude Code, Codex o Antigravity aproveche el sistema completo sin exigir que participen todas las IAs. La plataforma de entrada conoce las alternativas, asigna a un ejecutor capaz, selecciona esfuerzo apropiado, utiliza Orca solo cuando hay beneficio y entrega resultados con evidencia y QA.

**Esta entrega está destinada a integración por Claude:** el archivo no acredita que el sistema V2 esté desplegado, ni autoriza publicar, gastar, modificar cuentas, lanzar agentes sin permisos o migrar nombres técnicos históricos. Claude debe proponer PRs, ejecutar validaciones y registrar el resultado comprobado antes de declarar implementado.

## 1. Situación existente y continuidad (leer antes de editar)

Referencias de trabajo ya presentes en el repositorio:

| Recurso | Función actual / instrucción |
|---|---|
| AGENTS.md | Instrucciones compartidas e identidad comercial PREAMBRA. Mantenerlo corto y enlazar documentos de detalle. |
| CLAUDE.md / GEMINI.md | Puntos de entrada existentes; comprobar que importan AGENTS.md, no duplicar reglas. |
| team/ROUTING.md | Enrutamiento por dominio y procedimiento de delegación. |
| scripts/orca-dispatch.py | Router / plan de distribución existente; distinguir planeación de ejecución. |
| scripts/preambra-orca-smoke.py | Prueba offline; no ejecuta ninguna IA. |
| scripts/test_orca_dispatch.py | Tests del router y protección de ejecución. |
| docs/operations/PREAMBRA-MULTI-AI-ORCHESTRATION.md | Política V1 de conocimiento común y delegación. |
| docs/operations/MULTI-AI-CAPABILITY-ROUTING.md | Matriz histórica y enlaces a proveedores. |
| docs/operations/CHATGPT-ENTRY.md | Contrato de entrada cuando la sesión de ChatGPT tiene acceso al repo. |
| docs/operations/preambra-model-matrix.json | Preparación operativa, NO desempeño intelectual de los modelos. |
| continuity/checkpoint.json | Hitos y decisiones verificables; actualizar tras integración. |
| skills/ y team/ | Fuente canónica de habilidades y roles; cargar bajo demanda. |
| creative/visual-studio/ | Dirección audiovisual y herramientas visuales existentes. |

Hitos previos: PR [#90](https://github.com/alvaradom1304/Altiora/pull/90) (reglas multi-IA + smoke offline) y PR [#91](https://github.com/alvaradom1304/Altiora/pull/91) (registro de evidencia CI). El historial indica que el router pasó pruebas en GitHub Actions Windows/Ubuntu; **no** equivale a ejecutar Orca en la PC ni a verificar sesiones autenticadas de Claude/Codex/Antigravity.

No sobreescribir cambios ajenos ni asumir que el checkpoint representa el estado GitHub en tiempo real. Realizar git status, revisar rama/PR/CI y verificar los archivos efectivos.

## 2. Investigación: qué practican otros equipos y qué aprendemos

### 2.1 Fuentes primarias y experiencias públicas

| Fuente | Naturaleza de evidencia | Hallazgo útil | Límite |
|---|---|---|---|
| [Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents) | Guía técnica del proveedor | Routing, prompt chaining, paralelismo, orquestador-trabajadores, evaluador-optimizador; empezar por la solución más simple. | No demuestra que un modelo de una marca supere a otro. |
| [Anthropic — Common workflow patterns](https://claude.com/resources/articles/common-workflow-patterns-for-ai-agents-and-when-to-use-them) | Experiencia de equipos de producción | Patrones secuencial, paralelo y evaluador-optimizador; cada uno introduce costos. | Generalización de producción, no benchmark de PREAMBRA. |
| [Anthropic — Multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system) | Relato técnico de sistema real | El paralelismo ayuda en investigación compleja, pero el sistema multiagente descrito usa muchos más tokens (aprox. 15× frente a chats en ese caso). | NO aplicar 15× como factor de costo universal. |
| [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/) | Experiencia operativa del proveedor | Repositorio legible para agentes, instrucciones breves, pruebas, controles y recuperación permiten desarrollo agent-first. | Caso interno de ingeniería, no proceso comercial completo. |
| [OpenAI — Iterating development workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex) | Guía de flujo | Especificaciones y entregables de fase, pruebas y ciclos de revisión antes de implementar. | Adaptar a stack y cuenta actuales. |
| [stablyai/orca — orchestration](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx) | Documentación del producto | Runs, Tasks, worker-start, dispatches y coordinación de agentes; worktrees, según runtime disponible. | La documentación NO verifica instalación ni permisos locales. |
| [stablyai/orca — worktrees](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/model/worktrees.mdx) | Documentación del producto | Aislar trabajo concurrente y revisar diferencias. | Los worktrees no se crean por mencionar la palabra en un plan. |
| [dsifry/metaswarm](https://github.com/dsifry/metaswarm) | Implementación comunitaria pública | Gates de revisión adversarial, fases, TDD, artefactos y coordinación entre varios agentes. | Estudiar patrones, NO copiar ni instalar todo el framework. |
| [Reddit — Claude planning + Codex implementation/review](https://www.reddit.com/r/ClaudeCode/comments/1rht68z/how_i_run_long_tasks_with_claude_code_and_codex/) | Testimonio individual | Dividir plan/interfaz, implementación y revisión resulta útil para ese usuario. | Anecdótico; no prueba superioridad general. |
| [Reddit — Claude implements, Codex reviews](https://www.reddit.com/r/ClaudeCode/comments/1rh0kuo/anyone_else_using_claude_code_codex_together_way/) | Testimonio/comunidad | Revisión cruzada del diff, sin añadir un swarm para tareas simples. | Sesgo de selección y preferencias personales. |
| [Reddit — hub session + worktrees](https://www.reddit.com/r/ClaudeCode/comments/1xscwkp/how_i_run_claude_code_like_a_small_engineering/) | Testimonio individual reciente | Una sesión directora, un worktree por tarea y verificación de PR antes de fusionar. | No comprobar costos ni reproducibilidad solo con el comentario. |

**Conclusión de investigación:** el patrón más prometedor es orquestación **adaptativa**, con un director que no ejecuta todo, delegaciones delimitadas, revisión independiente basada en evidencia y trabajo paralelo solo cuando las tareas son independientes. No hay evidencia suficiente para nombrar un único proveedor como ganador permanente en todas las disciplinas.

### 2.2 Alternativas estratégicas evaluadas (estimación editorial, NO benchmark)

| Arquitectura | Puntuación de diseño preliminar | Ventaja | Principal costo/riesgo |
|---|---:|---|---|
| Una sola IA para todo | 7.5/10 | Muy simple, rápida | Cobertura limitada para tareas multidisciplinares |
| Claude coordina y todas las IAs intervienen siempre | 5.9/10 | Supervisión uniforme | Transferencias, duplicación, latencia y créditos |
| Orca coordina cada solicitud desde el inicio | 7.1/10 | Gran observabilidad potencial | Complejidad que no aporta a trabajos pequeños |
| **Router adaptativo + Orca selectivo + QA** | **9.0/10 (hipótesis)** | Balance entre especialidad, costo y control | Requiere diseño y evaluación propios |

Estas puntuaciones son **criterio de arquitectura provisional**, no resultados observados. Pesos de la comparación conceptual: calidad potencial 30%, recursos 20%, facilidad 20%, mantenimiento 20%, ampliación 10%. Reevaluar después del piloto.

## 3. Identidad, gobierno y ámbitos de responsabilidad

- **PREAMBRA:** marca, contratos, comunicación y relación con clientes. Categoría: firma de estrategia y ejecución empresarial. Prioridad: liquidez, ventas, margen y operación si corresponde; no recomendar ads, webs o automatizaciones prematuras.
- **Altiora:** núcleo técnico histórico, repositorios, skills, agentes y continuidad; no renombrar rutas técnicas de golpe.
- **Dirección humana:** aprueba presupuestos, cambios externos, acciones irreversibles, compromisos comerciales, publicaciones, permisos y tratamiento de datos sensibles.
- **ChatGPT:** candidato preferente para diagnóstico, investigación empresarial, hipótesis, alternativas, priorización y revisión ejecutiva. No asumir que una sesión de ChatGPT ejecuta CLIs del PC.
- **Claude Code:** director operativo candidato para planes de varios hitos, dependencia de trabajo, propuestas, copy, UX y coordinación de entregas.
- **Codex:** candidato preferente para ingeniería, automatizaciones, código, integraciones, pruebas, análisis reproducible y revisión técnica cruzada.
- **Antigravity:** candidato preferente para prototipos visuales, escenas 3D/WebGL, motion, navegación y QA visual, siempre que el entorno tenga herramientas efectivamente disponibles.
- **Director Audiovisual existente:** selecciona pipeline (Blender, Adobe, Remotion, FFmpeg, etc.) según valor y capacidades reales; **no** crear un segundo director por duplicación.
- **Orca:** transporte y coordinación técnica opcional. **No** es un LLM ni autoridad de negocio. Solo usar sus features después del preflight de versión, permisos y comandos.

**La matriz anterior es una preferencia inicial, NO exclusividad.** El router puede usar otra IA si supera criterios de calidad, disponibilidad, costo o tiempo en tareas comparables. El decisor no debe afirmar acceso no verificado.

## 4. Clases de modelo y esfuerzo (sin fijar versiones)

Separar el nombre del modelo, su *tier* de capacidad, el esfuerzo de razonamiento admitido y la superficie de ejecución. Un proveedor puede ofrecer distintas opciones por plan, modelo y CLI.

| Clase interna | Tipo de tarea | Esfuerzo deseado | Control |
|---|---|---|---|
| **E1 ligero** | Clasificación, limpieza, extracción y acciones mecánicas | low / equivalente válido | QA simple si es reversible |
| **E2 estándar** | Copy acotado, componentes, documentación, análisis sencillo | medium / equivalente válido | Revisión cuando el resultado sea visible al cliente |
| **E3 profundo** | Arquitectura, diagnóstico complejo, depuración, investigación estratégica | high / equivalente válido | Evidencia + revisión por riesgo |
| **E4 crítico** | Seguridad, finanzas sensibles, contratos y operaciones irreversibles | máximo **admitido** y justificado, no siempre el más caro | Aprobación humana + QA independiente obligatorio |

**Descubrimiento previo por sesión:** comprobar herramientas instaladas, versión, modelos listados, permisos, cuota y comandos admitidos. Usar las fichas vigentes del proveedor:
- OpenAI: https://developers.openai.com/api/docs/models y https://developers.openai.com/api/docs/guides/reasoning
- Claude Code: https://code.claude.com/docs/en/model-config
- Antigravity: https://antigravity.google/docs/models y https://antigravity.google/docs/cli/commands/effort
- Orca: https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx

La matriz de modelos de noviembre de 2026 presente en el repo es una **fotografía**, no verdad perpetua. No inventar IDs, flags, niveles de esfuerzo, precios ni acceso a modelos. Registrar el modelo **observado realmente**; si no existe evidencia, escribir UNKNOWN. No escalar automáticamente de tier/costo sin motivo y presupuesto.

## 5. Cuatro modos de operación (router contextual)

**Modo A — DIRECTO:** una IA resuelve tareas pequeñas, acotadas, reversibles y de bajo riesgo; sin Orca ni subagentes. Salida y verificación simple.

**Modo B — CONSTRUCTOR + REVISOR:** un productor y otra IA/revisor independiente. Predeterminado para código importante, material que verá un cliente, decisiones de arquitectura y entregables con consecuencias. El revisor lee requisitos, diff/artefactos y pruebas, NO solo el resumen del productor.

**Modo C — PARALELISMO SELECTIVO:** 2–3 especialistas con entradas suficientes y áreas/archivos independientes; worktrees solo cuando haya escritura simultánea en código. Integración secuencial posterior. No paralelizar decisiones encadenadas.

**Modo D — PROYECTO INTEGRAL:** dirección empresarial → diagnóstico → decisión → plan de hitos → selección dinámica A/B/C por hito → integración/QA → entrega → resultados comerciales. No lanzar todas las IAs en todas las fases.

Reglas del router, en orden:
1. Verificar problema, objetivo de negocio, limitaciones y aprobación de intervención.
2. Clasificar complejidad, riesgo, duración prevista, datos necesarios, tareas y dependencias.
3. Si una IA actual basta y no existe ganancia material al delegar, **Modo A**.
4. Si el entregable es sustancial o tiene riesgo, **Modo B**.
5. Si existen 2–3 frentes de trabajo independientes que comparten solo contratos claros y el beneficio de paralelismo supera el overhead, **Modo C**.
6. Si existe un encargo multidisciplinar empresarial con fases y gates, **Modo D** (sus hitos pueden ser A/B/C).
7. Seleccionar modelos realmente disponibles y menor razonamiento suficiente; fijar presupuesto/uso máximo.
8. Rechazar delegaciones que provoquen colisión de archivos, circularidad, datos faltantes o falta de autorización.
9. Opciones caras y escalaciones solo con motivo registrado. Dos intentos correctivos automáticos como techo inicial, luego bloquear y consultar.

## 6. Diagrama de ejecución

~~~mermaid
flowchart TD
 A["Solicitud en ChatGPT, Claude Code, Codex o Antigravity"] --> B["Contexto empresarial PREAMBRA y repositorio"]
 B --> C["Diagnóstico del problema y decisión de valor"]
 C --> D{"¿Qué intervención conviene?"}
 D -->|No justificada| E["Replantear, no vender entregables prematuros"]
 D -->|Justificada| F["Plan y Definition of Done"]
 F --> G{"Seleccionar modo A, B, C o D"}
 G -->|A| H["IA actual: ejecutar y verificar"]
 G -->|B| I["Constructor + revisor independiente"]
 G -->|C| J["2–3 especialistas, dependencias y rutas aisladas"]
 G -->|D| K["Hitos empresariales con gates"]
 J --> L["Orca si runtime y beneficio verificados"]
 I --> M["Integración y QA"]
 H --> M
 L --> M
 K --> M
 M --> N{"Cumple aceptación y presupuesto"}
 N -->|No| O["Corrección acotada: máx. 2 vueltas"]
 O --> M
 N -->|Sí| P["Aprobación humana si corresponde"]
 P --> Q["Entrega, medición y continuidad"]
~~~

## 7. SOP de proyecto integral PREAMBRA

| Fase | Responsable líder sugerido | Salida obligatoria | Gate |
|---|---|---|---|
| 0. Intake | ChatGPT | Objetivo, datos, restricciones, responsabilidades | Brief claro |
| 1. Discovery | ChatGPT + especialistas pertinentes | Diagnóstico, hipótesis, evidencia, incertidumbres | Calidad y suficiencia de información |
| 2. Research | Responsable según tema | Mercado, clientes, competidores, alternativas y fuentes | Fuentes trazables |
| 3. Decision Gate | Dirección empresarial + fundador | Problema prioritario, inversión razonable, solución elegida | Aprobación de alcance y presupuesto |
| 4. Plan | Claude Code | Hitos, tareas, dependencias, propietario por archivo, QA, costos | Plan ejecutable y sin circularidad |
| 5. Routing | Router existente | Modo, ejecutor, modelo observado, esfuerzo, herramientas disponibles | Acceso y recursos verificados |
| 6. Production | Codex / Claude / Antigravity / audiovisuales | Entregables y evidencia, no solo narrativa | Contrato cumplido |
| 7. Integration | Responsable designado | Artefactos unidos sin conflicto | CI, fallos y conflictos resueltos |
| 8. Independent QA | Revisor distinto + scripts | Hallazgos, pruebas, material rechazado/aprobado | Sin defectos bloqueantes |
| 9. Delivery | Dirección | Versión aprobada, documentación, licencias | Permisos de publicación |
| 10. Growth | ChatGPT / analista | Métricas de negocio reales vs línea base | Aprendizaje y próximo hito |

**Norma PREAMBRA:** un sitio impresionante, una automatización o una campaña no es un resultado empresarial en sí. La prueba debe relacionar producción con ventas, rentabilidad, tiempo, confianza o cumplimiento del objetivo del cliente.

## 8. Contrato universal de tarea y handoff

Todas las entradas (ChatGPT, Claude, Codex, Antigravity) deben entender este contrato. Preferir un JSON pequeño y rutas a documentos; no copiar transcripciones completas. Ejemplo:

~~~json
{
  "schema_version": "2.0-proposed",
  "job_id": "PRE-ORCH-002",
  "brand": "PREAMBRA",
  "technical_system": "Altiora",
  "project": "PREAMBRA OS V2",
  "goal": "Auditar el router y proponer la mejora mínima",
  "business_value": "Menos retrabajo y mejor decisión de delegación",
  "mode": "B",
  "owner": "codex",
  "reviewer": "claude",
  "model_observed": "UNKNOWN",
  "reasoning_effort": "medium",
  "tool_access": {"orca": "UNKNOWN", "github": "VERIFY"},
  "inputs": ["AGENTS.md", "team/ROUTING.md"],
  "owned_paths": [],
  "dependencies": [],
  "acceptance": [
    "Matriz de diferencias contra V2",
    "Evidencia por archivo y línea",
    "Ningún cambio de código en fase de auditoría"
  ],
  "max_correction_attempts": 2,
  "budget_limit": "TO_BE_APPROVED",
  "artifacts": [],
  "checks": [],
  "status": "PLANNED",
  "evidence": [],
  "risks": [],
  "next_action": "AUDIT_READ_ONLY"
}
~~~

Estados admitidos propuestos: PLANNED → READY → IN_PROGRESS → REVIEW → APPROVED → DONE; alternativas BLOCKED, FAILED, CANCELED. **DONE** exige evidencia de ejecución. Un plan de Orca sin worker real sigue PLANNED. Usar identificadores reales de Run/Task/Dispatch cuando existan.

Almacenamiento: contrato por tarea en carpeta de proyecto apropiada, referencias a archivos versionados; secreto, credencial y datos personales nunca en GitHub público. No generar un objeto gigante de memoria global ni automatizar el envío de transcripciones.

## 9. Orquestación técnica: cuándo y cómo usar Orca

**No tratar Orca como cuarto modelo.** Comparar las funcionalidades existentes con las guías vigentes del proveedor antes de crear wrappers nuevos.

- **A/directo:** resolver desde la herramienta actual; no activar Orca por costumbre.
- **B/revisión:** handoff a otro agente por método disponible y verificado; Orca es útil si administra sesiones y capturas, pero no obligatorio.
- **C/paralelo:** Orca puede coordinar Runs/Tasks/worker-start; cada trabajador con worktree propio en código; una sola autoridad para integrar cambios.
- **D/integral:** un coordinador operativo por proyecto, gates de negocio separados del coordinador CLI, dependencias DAG y evidencia de cierre por hito.

En la PC autorizada comprobar primero, sin revelar credenciales: 
- git status y versiones de node/python;
- orca --version; orca status --json (si el CLI admite ese comando);
- claude --version, codex --version, agy --help; listado real de modelos en cada producto;
- npm run orca:smoke; npm run orca:test; npm run check;
- npm run orca:dispatch -- --router heuristic --json "Auditar estrategia, copy y prototipo 3D de PREAMBRA" (plan sin ejecutar).

**No habilitar ALTIORA_DISPATCH_EXECUTE=1 en el piloto de lectura.** Nunca inferir que un worktree fue creado porque el JSON diga new-child. Consultar la documentación de la versión instalada antes de iniciar Run, Task o worker.

Si Orca no funciona o no mejora tiempos, mantener handoffs manuales con GitHub hasta superar los requisitos. No bloquear un cliente por el software del orquestador.

## 10. Aislamiento de archivos y seguridad

- Antes de delegar, registrar propiedad de archivos y rutas específicas, no carpetas genéricas superpuestas.
- Si dos tareas editan los mismos archivos: secuenciar o crear una sola tarea con único responsable.
- Workers en worktrees diferentes no deben tocar producción por defecto.
- Fusionar mediante PR con diff revisado y CI. No editar branch main sin gate.
- Todo repositorio externo, skill, agente, MCP o instalador pasa el gate de terceros ya existente; comprobar licencia, permisos y compatibilidad.
- No exportar catálogos privados, datos de clientes, claves o credenciales hacia modelos sin acceso autorizado.
- La auditoría financiera/legal y decisiones contractuales requieren revisión competente humana cuando aplique; una IA no sustituye profesionales habilitados.
- No publicar ni activar pagos/anuncios con una salida generada por agente sin aprobación.
- Evitar bucles abiertos: dos intentos correctivos automáticos máximo inicial; luego BLOCKED + evidencia.

## 11. QA: tres puertas obligatorias según riesgo

1. **QA determinista:** test, build, diffs, validación de datos, links, renders reales, navegación, accesibilidad, móvil, permisos y evidencias de ejecutor. No aceptar autodeclaraciones.
2. **QA adversarial independiente:** revisor con contexto suficiente que compara la solución contra criterios, fuente original y artefactos; identifica errores con severidad y pasos de reproducción. El agente creador NO se autoaprueba.
3. **QA empresarial:** la solución corresponde a la necesidad y al presupuesto del cliente. Aprobación humana en riesgos, inversión, publicación, promesas comerciales o cambios irreversibles.

Un defecto crítico bloquea publicación incluso si otros scores son altos. Correcciones acotadas por defecto; registrar defectos corregidos, sin reabrir todo el plan si el contrato no cambió.

## 12. Piloto para elegir IA y arquitectura con datos propios

**No declarar «mejor modelo» ni ahorro sin comparar.** Preparar 12 tareas representativas y versiones equivalentes del brief. El objetivo inicial es exploración operativa, no significación estadística.

| ID | Categoría | Trabajo representativo | Evidencia esperada |
|---|---|---|---|
| STR-01 | Estrategia | Diagnóstico de caja/ventas sin datos sensibles | Hipótesis, supuestos y decisiones priorizadas |
| STR-02 | Estrategia | Evaluación de una oferta comercial | Justificación de costos y restricciones |
| STR-03 | Investigación | Mapa de oportunidades con fuentes | URLs, fechas, citas y contraste |
| BRD-01 | Marca | Propuesta de valor PREAMBRA | Diferenciación sin clichés; feedback experto |
| BRD-02 | Copy | Descripción de servicios de conversión | Claridad, coherencia y control de afirmaciones |
| BRD-03 | UX | Journey de cliente en landing de consultoría | Wireframe y criterios de conversión |
| ENG-01 | Código | Reparar script con tests fallidos en fixture | Diff y tests |
| ENG-02 | Código | API de pedidos en entorno ficticio | Pruebas, seguridad y contrato |
| ENG-03 | Ingeniería | Auditoría de dependencia/arquitectura | Defectos reproducibles, severidad |
| VIS-01 | Visual | Prototipo GSAP accesible | Render/capturas y fallback |
| VIS-02 | Visual | Escena R3F sencilla y optimizada | FPS/móvil y evidencia visual |
| VIS-03 | QA visual | Auditoría comparativa desktop/móvil | Lista de defectos con capturas |

Comparadores: IA sola, constructor+revisor y paralelo solo cuando se cumplan sus condiciones. Mismo input, versiones de herramientas registradas, mismos criterios, sin variar otras condiciones cuando sea posible. Las pruebas visuales y comerciales requieren juicio humano además de medidas automáticas.

**Score por tarea, 0–100 (propuesto, aún no medido):** calidad y aceptación 30%, exactitud/trazabilidad 25%, valor de negocio 20%, tiempo hasta entrega útil 15%, consumo de recursos 10%. Registrar también defectos críticos, retrabajos, costo/uso real y número de intervenciones humanas. Cualquier defecto crítico puede bloquear la aceptación aunque el score agregado sea alto.

Métricas: tasa de aceptación al primer intento, defectos que escaparon a QA, tiempo por hito, gasto/uso por tarea, número de reintentos, minutos de coordinación, valor de negocio. No extrapolar ahorro 15× ni porcentajes sin métricas de PREAMBRA.

**Regla de promoción a default:** comparar contra baseline simple, comprobar mejora material en calidad o eficiencia, mantener riesgo controlado y documentar aceptación humana. Repetir evaluaciones tras cambios relevantes de proveedor o versión; nunca asumir que un ranking dura para siempre.

## 13. Dos playbooks de negocio (casos reales de uso)

### 13.1 El Tilichero CR — Prioridad: liquidez, pedidos y confianza

Entrada: catálogos reales de tres proveedores (si el usuario los facilita o conecta), precios, condiciones de compra tras pedido, modalidad de pago y referencias de imagen.

1. **ChatGPT:** diagnóstico comercial, hipótesis de demanda, selección de oportunidades verificables y restricciones de caja.
2. **Codex:** extracción trazable de SKUs, proveedor/página exacta, costo, margen y archivo de referencia; comparar referencia del catálogo con imagen de IA y registrar diferencias; no inventar stock.
3. **Claude Code:** copy, portadas, secuencia de contenido, respuestas de WhatsApp y propuesta comercial adaptada a los productos validados.
4. **Antigravity / Director audiovisual:** producción visual únicamente cuando exista material autorizado y una necesidad concreta; comprobar que imagen y producto concuerden.
5. **QA:** productos reales, claims, disponibilidad, precio y decisión de gasto aprobados.
6. **Medición:** pedidos, margen estimado vs realizado, consultas cualificadas, abandono y señales de confianza.

No imponer anuncios, inventario ni web compleja cuando el cliente requiere flujo de caja inmediato.

### 13.2 La Central del Queso — Prioridad: experiencia de marca + pedidos

1. **ChatGPT:** historia, modelo comercial, recorrido de compra, prioridades y contenidos verificados.
2. **Claude Code:** arquitectura UX/UI, storytelling, estructura de páginas y especificaciones.
3. **Director Audiovisual + Antigravity:** una escena representativa de entrada a finca/granero antes de construir todo el recorrido; materiales reales y degradación progresiva.
4. **Codex:** implementación fiable, formularios, catálogos, accesibilidad, seguridad y rendimiento; revisión independiente del código generado por otros.
5. **QA:** móvil, tiempos de carga, accesibilidad, derechos de assets, pedidos funcionales y experiencia visual.
6. **Aprobación y medición:** navegación útil, pedidos y confianza, no solamente estética.

## 14. Plan de implementación para Claude: fases y tickets

### Sprint 0 — Auditoría de lo que existe (no alterar nada)
- Leer archivos listados en sección 1 y el estado Git/PR/CI.
- Identificar duplicados: AGENTS.md, team/ROUTING, dispatcher, matriz, skills, orquestadores.
- Comparar V1 vs V2: qué se mantiene, qué se elimina, qué se modifica.
- Verificar que la investigación y modelos catalogados no se confunden con disponibilidad real.
- Entregar matriz GAP y arquitectura mínima. **Criterio:** ninguna propuesta exige un orquestador duplicado.

### Sprint 1 — Contratos y clasificación A/B/C/D
- Definir un único esquema versionado de handoff con validación.
- Extender **el router existente** para seleccionar modo según riesgo, independencia y dependencias, no solo keywords.
- Guardar recomendación de modelo/esfuerzo como candidato hasta preflight real.
- Pruebas de: directa, revisión, paralelo, integral, bloqueo por dependencias, conflicto de rutas, ausencia de cuota y permisos.
- Conservar compatibilidad con contratos actuales o establecer migración explícita.

### Sprint 2 — Ejecución + observabilidad real
- Antes de modificar el launcher, verificar la CLI Orca instalada, su documentación actual y las sesiones locales.
- Un worker de lectura y su handoff real, sin escritura. Registrar ID, versión, modelo observado, esfuerzo, terminal, resultado y QA.
- Solo después ensayar constructor+revisor con una rama aislada y autorización expresa de ejecución.
- No habilitar ejecución automática general ni saltarse guardias de dispatch.

### Sprint 3 — QA empresarial y técnico
- Integrar gates deterministas y revisión independiente, con defectos y severidad.
- Añadir evidencia de impacto empresarial por objetivo, no solo test verde.
- Verificar diseño visual real cuando aplica; la existencia de test o adapter no acredita render.

### Sprint 4 — Benchmark interno y optimización
- Ejecutar el piloto de 12 tareas en condiciones comparables.
- Seleccionar modelos, esfuerzos y fallbacks por evidencia local.
- Retirar reglas rígidas que contradigan datos; limitar costo/reintentos y latencia.
- Actualizar matriz, skills pertinentes y continuidad; documentar nuevas decisiones y fuente.

## 15. Definition of Done de la integración

La V2 solo puede declararse **implementada** si:
- La entrada desde cada herramienta documentada conoce las capacidades del ecosistema sin afirmar conexiones falsas.
- A/B/C/D tienen comportamiento y pruebas distinguibles.
- El contrato de handoff y su esquema pasan verificaciones automáticas.
- El enrutador no lanza Orca para tareas que deben ser directas.
- Nunca hay dos escritores sobre el mismo conjunto de archivos a la vez.
- Un worker real se ejecutó desde la PC autorizada y produjo evidencia, o se declara explícitamente **BLOCKED_RUNTIME**.
- Un revisor distinto observó los artefactos y sus pruebas.
- Todo cambio de código pasó CI y PR; la rama main no fue alterada sin revisión.
- Los puntajes de arquitectura/modelos se distinguen de mediciones reales.
- PREAMBRA sigue siendo la identidad comercial; Altiora se mantiene como sistema técnico hasta migración segura.
- Se registran costo/tiempo/defectos, estado, riesgos, fecha y siguiente paso en continuidad.

## 16. Primer encargo inmediato a Claude (con valor y bajo riesgo)

**PRE-ORCH-002 — Auditoría de diferencias V1 vs V2.**

Rol líder: Claude Code, esfuerzo inicialmente medio/alto según complejidad real. Colaborador: Codex como revisor si existe acceso autenticado, SIN ejecutar ambos obligatoriamente. Orca en modo plan o no usado.

Objetivo: producir una **matriz de brechas verificable** sobre el código existente (routing, contracts, QA, cuentas disponibles, duplicación, fallbacks, costos). NO cambiar de golpe el runtime. Identificar los tres cambios mínimos que más mejoren la capacidad de trabajar para clientes. Priorizar, como primer hito implementable, **selección A/B/C/D** con pruebas y guardia de acceso. Hacer PR con modificaciones acotadas cuando el alcance esté claro y autorizado. Nunca confundir "PR generado" con "worker corriendo" o "agente integrado".

Entregables:
- docs/operations/PREAMBRA-OS-V2-GAP-ANALYSIS.md (propuesto)
- mapa de modificaciones y criterios de aceptación
- propuesta de primer PR técnico con costo/riesgo
- QA y evidencia de comandos realmente ejecutados
- decisión documentada entre continuar con router/Orca existentes o cambiar alguna parte por razones comprobadas

## 17. Mensaje de arranque listo para Claude Code

> Trabaja con el repositorio actual alvaradom1304/Altiora. Lee este documento maestro completo y los archivos existentes que aquí se enumeran. Actúa como director operativo, pero no te autoatribuyas permisos o accesos a otras IAs. Ejecuta primero PRE-ORCH-002, audita diferencias entre V1 y V2, entrega matriz de brechas con fuentes de archivo y propone PR mínimo. Después integra por hitos la arquitectura A/B/C/D, el contrato de handoff, selección dinámica de modelo/esfuerzo y QA independiente, respetando las autorizaciones y las protecciones de Orca. No introduzcas frameworks redundantes. Cuando un cambio reversible y local esté bien delimitado, implementa y prueba; para gasto, publicaciones, conexiones nuevas, modificaciones irreversibles o ejecución multiagente sin verificar, solicita aprobación. Al terminar informa QUÉ CAMBIÓ, QUÉ CORRIÓ, QUÉ QUEDÓ SIN PROBAR y QUÉ SIGUE.

## 18. Estado al redactar este documento

- **Investigación y propuesta conceptual:** elaboradas a partir de documentación oficial y testimonios públicos; evaluaciones editoriales, no benchmarks.
- **Router V1 / guardias offline:** presentes en GitHub y documentados como aprobados en PR #90/#91.
- **PREAMBRA OS V2:** documento maestro para integración, **no desplegado por crear este Markdown**.
- **Orca PC / uso autenticado de varias IAs:** no verificado en esta sesión.
- **Ahorro real / ranking definitivo de modelos:** no medido.
- **Siguiente paso:** Claude ejecuta PRE-ORCH-002 y propone la integración mínima verificable.

---

**Regla final:** *La mejor orquestación es la que aporta soluciones de negocio superiores con menos complejidad, menos retrabajo, menor consumo justificable y mayor evidencia, no la que invoca más agentes.*
