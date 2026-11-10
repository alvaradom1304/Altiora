# Altiora Immersive Web Lab

**Entrada:** [mapa de Altiora](docs/operations/MAPA-ALTIORA.md) (raíces empresa/cliente, áreas Dirección · Análisis · Producción · Operación, cómo pedir un encargo) · [estado actual](docs/operations/ESTADO-ACTUAL.md) · [índice de skills y agentes](INDEX.md).

## Diagnóstico y calidad compartidos

Claude Code, Codex, Gemini CLI, Antigravity y ChatGPT utilizan [el mismo protocolo operativo](docs/operations/SHARED-OPERATIONS.md): `npm run capability:doctor` distingue archivos y herramientas de conexiones comprobadas; `npm run routing:eval` comprueba recuperación de skills con casos representativos; `npm run production:qa` reúne evidencia audiovisual y revisiones pendientes. No instala software, no conecta cuentas ni acredita aprobación comercial. El [índice generado](INDEX.md) contiene los recuentos vigentes de roles y skills.

Laboratorio de experiencias web inmersivas y comerciales. Primer caso: **La Central del Queso**, un recorrido de la finca a la mesa.

La base de investigación reúne **25 repositorios** con una función, una decisión y una revisión concreta. La selección inicial favorece Three.js + React Three Fiber + Drei + GSAP; glTF Transform prepara los modelos. Lenis se evalúa después de comparar con el scroll nativo.

## Altiora Visual Studio — Motion, Blender, Adobe y producción multi-IA

Nuevo: [sistema visual compartido](creative/visual-studio/README.md), [router para Claude, Gemini/Antigravity y ChatGPT/Codex](creative/visual-studio/ROUTER.md), [70 referencias visuales evaluables](references/visual-libraries-2026.json) y [workflow de producción](docs/workflows/visual-production-multi-ai.md). Son extensiones documentales; no se han instalado programas, addons ni servidores MCP.

La expansión avanzada agrega [matriz técnica](creative/visual-studio/PRODUCTION-MATRIX.md), [playbooks portables](creative/visual-studio/playbooks/README.md) y [protocolo común para Claude, Gemini/Antigravity y ChatGPT/Codex](creative/visual-studio/AGENT-PORTABILITY.md), sin instalar automáticamente las 70 referencias ni instalar aplicaciones Adobe.

## Experimento audiovisual ejecutable (código)

[Tilicheros · Cinematic Motion Pilot](experiments/tilicheros-motion-lab/README.md) contiene una plantilla Remotion 15s vertical, un diseño conceptual original y un script Blender para generar CGI reproducible. Los archivos están versionados y cuentan con validación automatizada, pero **no** representan un anuncio final ni un render certificado.

## Dirección audiovisual automática

El [Director de Experiencia Audiovisual](creative/visual-studio/agents/audiovisual-experience-director.md) es el nuevo rol formal en el [equipo](team/registry.md), con prompt compartido para Claude, Gemini y ChatGPT/Codex. La IA debe escoger el pipeline audiovisual según el resultado pedido, accesos verificables, licencias y calidad, sin obligar al usuario a escoger librerías. El Visual Tech Scout le entrega señales para mejorar el sistema.

## Mejora continua del stack visual

[Visual Tech Scout](creative/visual-studio/agents/visual-tech-scout.md) + [vigilancia semanal de los 70 repositorios](continuity/visual-watch/README.md) + `npm run visual:preflight`: detecta cambios de actividad, licencia y estado, crea informes y puede proponer PRs con revisión humana. Es una rutina automatizada de GitHub Actions, **no** instalación ilimitada de paquetes ni una IA conectada permanentemente.

## Recuperar trabajo sin repetir «continúa»

[Continuity OS](continuity/README.md) usa un [checkpoint versionado](continuity/checkpoint.json) y `npm run resume` para recuperar milestones, evidencia y próximos pasos entre chats de Claude, Gemini y ChatGPT/Codex. Se valida automáticamente con `npm run check`; no promete solucionar la interfaz de ChatGPT ni activar tareas en segundo plano.

## Empezar

1. Leer la [comparación de repositorios](docs/research/repository-review.md).
2. Consultar el [catálogo reproducible](references/repositories.json).
3. Seguir la [decisión de arquitectura](docs/decisions/0001-immersive-foundation.md).
4. Abrir el [caso La Central del Queso](projects/la-central-del-queso/BRIEF.md).
5. Trabajar con el [proceso de experimentos](docs/workflows/immersive-project.md) y la [plantilla](templates/experiment.md).
6. Revisar la [estrategia de diferenciación](docs/strategy/DIFERENCIACION.md) y el [borrador de paquetes](docs/strategy/PAQUETES-BORRADOR.md).

La [validación](docs/research/VALIDATION.md) distingue lo comprobado de lo pendiente.

## Qué contiene esta primera entrega

- Evaluación documental a fecha 2026-10-18: utilidad, actividad, compatibilidad y licencias.
- Revisiones de origen fijadas por commit para estudiar ejemplos reproducibles.
- Criterios de aceptación visual, accesibilidad, rendimiento y pedidos.
- Herramienta para traer una referencia a una carpeta local ignorada, sin instalar ni ejecutar su código.

El catálogo registra fuentes; no instala dependencias en la web ni incorpora copias de los proyectos externos. Aún no existe una escena ejecutable o una medición de rendimiento de Altiora.

## Comprobar el laboratorio

El control completo requiere Node.js 20+ y Python 3.11+ disponibles como `node` y `python`. Git se usa para descargar referencias. No necesita instalar paquetes. `npm run check` ejecuta las mismas suites que CI Windows/Linux; `npm run check:base` es solo el control parcial anterior.

~~~sh
npm run check
npm run reference -- codrops/OneElementScroll
~~~

La segunda orden descarga únicamente esa revisión en `.references/`. No ejecuta instrucciones del README externo. No es necesario descargar todos los repositorios.

## Proyectos

- [La Central del Queso](https://github.com/alvaradom1304/la-central-del-queso): la web existente vive en `src/web` (rama `hito2-exterior-realista`). Mantener allí el catálogo, pedidos, WhatsApp y ubicaciones mientras los experimentos se validan en Altiora.
- Primer experimento definido: [umbral de la finca → mesa](projects/la-central-del-queso/experiments/001-umbral-a-mesa.md).

## Equipo y Roles de Agentes (`team/`)

El laboratorio define sus roles operativos y directrices de orquestación en [team/registry.md](team/registry.md); el recuento vigente está en [INDEX.md](INDEX.md):
- **Director de experiencia**: Integración de estrategia, dirección de arte y gates de calidad.
- **Director creativo & Motion designer**: Concepto visual, narrativa de cámara, animaciones y fallbacks.
- **Ingeniero web & Shader artist**: Implementación WebGL, Three.js, React Three Fiber y shaders GLSL.
- **UX researcher & Diseñador UI**: Flujos de compra, accesibilidad WCAG y componentes táctiles.
- **Estratega de negocio & Analista de conversión**: Unit economics, calculadoras de feria y pasaporte VIP.
- **QA & Accessibility reviewer**: Control independiente de calidad, métricas de rendimiento y regresiones.

El [índice](INDEX.md) reúne agentes, chats, skills y repositorios. Los roles funcionan como agentes reales: subagentes de Claude Code en `.claude/agents/` y prompts portables para Codex, Gemini o ChatGPT en `team/agents/`. Las IAs se reparten el trabajo en el [chat del equipo](team/chat/README.md) (`npm run chat -- board`).

## Catálogo de Skills Integradas (`skills/`)

El repositorio cuenta con un catálogo de skills especializadas cuyo recuento se genera en [INDEX.md](INDEX.md). Las de terceros conservan licencia y procedencia en [skill-sources.json](references/skill-sources.json). Se categorizan en:
1. **Brand & Creative Intelligence**: Art direction, brand architecture, storytelling, color system, typography direction.
2. **Premium Web Experience**: Three.js, React Three Fiber, GSAP animation, motion design, responsive design, conversion UX.
3. **Business & Financial Intelligence**: Unit economics, pricing strategy, margin analysis, cash flow, financial forecasting.
4. **AI & Automation**: Agent design, orchestration, evaluation, n8n webhook architecture, RAG architecture.
5. **Cybersecurity & QA**: OWASP review, frontend/backend security, API security, vulnerability triage.

Las skills mejoran por ciclos PDCA medidos: `npm run skills:audit` puntúa cada una y bloquea regresiones. Ver [mejora continua de skills](docs/workflows/skill-improvement.md), el [informe actual](quality/skills-report.md) y el [registro de ciclos](quality/skills-improvement-log.md).

## Fuentes y uso

Las estrellas y fechas son una fotografía de investigación, no una garantía de calidad. La licencia de código no acredita automáticamente modelos, imágenes, sonidos o fuentes tipográficas. Registrar la procedencia de cada recurso utilizado y conservar avisos cuando se reutilice código.

GSAP usa su licencia propia Standard No Charge. El catálogo señala una discrepancia MIT/ISC en r3f-scroll-rig; ese candidato queda en espera.

## Descubrimiento Claude Code y auditoría pública

Corrección e inventario reconciliado: [diagnóstico de Claude](docs/operations/claude-discovery.md). Auditoría pública con límites y pruebas propuestas: [Instagram de El Tilichero](projects/tilicheros/ads/AUDITORIA_INSTAGRAM_PUBLICO_2026-10-29.md). Los 260 originales se conservan; la incorporación local comprobada lleva el catálogo a 261. Los 15 roles canónicos y siete adaptadores suman 22 identidades. Los comandos auxiliares se cuentan aparte.

## Visual Studio V3
[70 librerías curadas](references/visual-libraries-2026.json), [vigilancia de versiones estables](creative/visual-studio/SCOUT-V3.md), [CGI/color avanzado](creative/visual-studio/playbooks/advanced-cgi-color.md) y [animación 2D generativa](creative/visual-studio/playbooks/illustration-particles.md). Todas las IAs consumen el mismo Director Audiovisual y router; ninguna instala automáticamente todo el catálogo.

## Adobe After Effects · preparación de acceso
[Puente local AE y tutorial de permisos](creative/visual-studio/after-effects/README.md) y `npm run adobe:check`: permiten a las IAs planear y controlar renders de proyectos propios con After Effects instalado y autorizado. **No hay conexión comprobada con la laptop del usuario**; el conector Adobe de ChatGPT requiere autorización independiente.

## Acceso preparado a After Effects
Se añadió un [puente local aerender](scripts/after-effects-bridge.mjs), [guion de composición original](creative/visual-studio/after-effects/altiora-concept-comp.jsx) y [protocolo de acceso](creative/visual-studio/playbooks/adobe-post.md). El conector Adobe permite flujos de medios/Creative Cloud en ChatGPT, pero no edición nativa de archivos .aep. La activación local sigue pendiente de comprobar aplicación, proyecto y permisos; `npm run after-effects:check` informa sin instalar.

## Conexión de After Effects para Claude/Gemini/Antigravity/Codex
[Guía de un solo paso local](creative/visual-studio/after-effects/MCP-SETUP.md): `npm run ae:clients:plan` y `npm run ae:clients:connect`. Las configuraciones son locales de cada cliente y requieren instalaciones reales; no concede control remoto desde ChatGPT web o móvil.

---

# Altiora Enterprise OS (integrado el 01/11/2026)

<!-- ALTIORA_BUSINESS_ENTRYPOINT -->
## Operación comercial vigente

[Oferta, economía de proyecto y experiencia de cliente](docs/altiora-business/INICIO.md): objetivo US$10.000 por proyecto y mantenimiento mensual opcional. Etapa de validación, con cero clientes de pago confirmados. Capacidades y aspiraciones descritas abajo no acreditan resultados comerciales o personal contratado.

# Altiora Enterprise OS

**Altiora** diagnostica, diseña e implementa sistemas de crecimiento para empresas: estrategia, marca, marketing, ventas, tecnología y operación conectadas con resultados que puedan medirse. Su alcance incluye puntos de contacto digitales y físicos cuando el proyecto y la capacidad lo permitan. [Alcance de la empresa](docs/altiora-business/POSICIONAMIENTO.md).

Este repositorio contiene la arquitectura central (AEM OS), la biblioteca de capacidades empresariales (Skills) y el motor de automatización que permite a Altiora diagnosticar, construir, operar y escalar empresas.

## Laboratorio Fundacional: La Central del Queso
Para validar y demostrar la capacidad operativa del sistema al mundo empresarial, Altiora utiliza **La Central del Queso** como su caso de estudio y laboratorio piloto. Este proyecto aplica en tiempo real todas las metodologías de la firma:
- Business Discovery & Research
- Sales & Marketing Intelligence
- Premium Web Experience & E-commerce
- AI Automation & Growth Analytics

---
*Misión: Construir sistemas inteligentes capaces de ayudar a empresas a entender mejor su realidad, tomar mejores decisiones, operar mejor, crecer y escalar.*
