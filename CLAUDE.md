@AGENTS.md

## Equipo de agentes
Los roles canónicos de `team/registry.md` y los adaptadores locales de `team/local-agents.json` están disponibles como subagentes en `.claude/agents/`. Para trabajo multirrol, coordinarse en el chat del equipo (`team/chat/README.md`) firmando como `claude/<rol>`: reclamar la tarea antes de editar y cerrar con evidencia.

Índice completo en INDEX.md. En Claude Code: `/equipo <encargo>` reparte trabajo, `/chat-<rol> <mensaje>` habla con un agente, `/repos <necesidad>` consulta repositorios de referencia y cada skill de `skills/` está disponible como `/<nombre>` (todas son seleccionables por pertinencia salvo restricción explícita en la fuente). `.claude/skills/` e INDEX.md se generan con `npm run agents:build`; no editarlos a mano.

## Descubrimiento verificable
Consultar `references/discovery-manifest.json` para reconciliar fuentes, agentes y comandos auxiliares. No contar `/chat-*`, `/equipo` o `/repos` como skills del catálogo. Los roles y subagentes son las mismas identidades; no sumarlos dos veces. Si falta una capacidad, leer `docs/operations/claude-discovery.md`. Abrir esta raíz y la rama actualizada; no confundir el catálogo con una sesión activa.

## Expansión audiovisual
Antes de tareas de Blender, Adobe, motion, VFX, anuncios o video programático, leer [Visual Studio](creative/visual-studio/README.md) y [router visual](creative/visual-studio/ROUTER.md). Se trata de una capa de orquestación que utiliza las skills existentes. La presencia de repositorios externos no implica instalación, capacidades de editor ni permisos de render.

## Skill operativa V2 (compartida con Gemini y Codex)
Si la intención del usuario contiene **motion graphics, After Effects, Premiere, Photoshop, Blender, VFX, cinematic, shaders, web 3D o anuncios**, cargar [protocolo](creative/visual-studio/AGENT-PORTABILITY.md), [matriz](creative/visual-studio/PRODUCTION-MATRIX.md) y el [playbook correspondiente](creative/visual-studio/playbooks/README.md). Delegar a los agentes existentes solo las skills pertinentes, sin instalar servidores MCP de terceros por defecto.

## Reanudación sin reconstruir el chat
Antes de continuar una tarea de Altiora, leer [checkpoint](continuity/checkpoint.json) y [recovery runbook](continuity/README.md), ejecutar `npm run resume` si hay checkout y verificar PRs/CI. Si el usuario dice «sigue», priorizar siguiente paso desbloqueado; no duplicar milestones completados ni pedir de nuevo el brief existente.

## Visual Tech Scout — actualización periódica
Para decidir nuevas librerías o actualizar pipelines consultar el [rol de vigilancia](creative/visual-studio/agents/visual-tech-scout.md), el [reporte semanal de GitHub Actions](continuity/visual-watch/README.md) y el [preflight real](scripts/visual-preflight.mjs). Priorizar cambios de licencia, seguridad y P0; proponer PR/piloto y registrar QA, nunca auto-instalar o fusionar sin revisión. El workflow es el monitor programado; el subagente Claude solo interviene cuando se ejecuta/autoriza.

## Punto de entrada audiovisual automático
Cuando haya petición visual activar el subagente `audiovisual-experience-director` antes de repartir el trabajo. Leer su [contrato de decisiones](creative/visual-studio/agents/audiovisual-experience-director.md). Este director escoge Blender/Adobe/Remotion/Three u otras opciones sin hacer elegir tecnología al usuario; delega a creative-director, visual-producer, motion-designer, web-engineer y QA. `/chat-audiovisual-experience-director` abre su bandeja; las ejecuciones dependen del acceso real al repositorio y herramientas.

## Visual Studio V3 y skills actualizables
El Director Audiovisual consulta [SCOUT-V3](creative/visual-studio/SCOUT-V3.md) para nuevas versiones y activa por intención [CGI-color](creative/visual-studio/playbooks/advanced-cgi-color.md) o [2D-motion-artístico](creative/visual-studio/playbooks/illustration-particles.md). Las nuevas herramientas son referencias, no dependencias ya instaladas.

## Adobe After Effects
El [puente local AE](creative/visual-studio/after-effects/README.md) permite comprobar `aerender`, planear un render y, con permiso explícito y archivo .aep local, ejecutarlo en una computadora con After Effects instalado. Si no hay acceso, delegar alternativa. El conector Adobe de ChatGPT es una integración distinta.

## MCP local After Effects para Claude Code
Consultar [registro multi-cliente](creative/visual-studio/after-effects/MCP-SETUP.md): `npm run ae:clients:plan` y, solo desde la laptop con permiso, `npm run ae:clients:connect`. Comprobar con `claude mcp list`. El Director Audiovisual puede entonces elegir AE si `aerender` funciona; nunca afirmar acceso del ChatGPT remoto.

## After Effects en PC — MCP local
Desde la carpeta Altiora confiable, ejecutar `npm run after-effects:setup -- --apply` para crear configuración de este proyecto y verificar `/mcp`. Abrir [instrucciones MCP](creative/visual-studio/after-effects/MCP-SETUP.md). Usar siempre primero `after_effects_preflight`; si la app no está disponible, no afirmar acceso. Render solo tras autorización explícita del propietario y aprobación del proyecto exacto.

<!-- ALTIORA_BIBLIOTECARIO_START -->
## Selección y contexto
En cada mensaje conserva el objetivo activo y elige entre las capacidades realmente disponibles. Usa la skill más específica y carga sus referencias solo cuando hagan falta; si nada aporta, resuelve directamente. Para selección ambigua consulta [Bibliotecario](skills/altiora-bibliotecario/SKILL.md). En trabajos pequeños evita equipos; delega solo con autorización y capacidad real. Reutiliza evidencia vigente y responde con resultado, comprobación y límite material, sin repetir historia ni omitir requisitos para ahorrar. No presupongas ahorro medido, modelos cambiados o conexiones por existir un archivo.
<!-- ALTIORA_BIBLIOTECARIO_END -->

<!-- ALTIORA_AUDIO_SPECIALIST -->
Para sonido, voz, música, restauración, mezcla o masterización, usar [audio-specialist](team/agents/audio-specialist.md) y [audio-production](skills/audio-production/SKILL.md). Cargar solo la modalidad necesaria; separar medición, escucha y aprobación.

Para diagnóstico, evaluación de recuperación o QA audiovisual, seguir bajo demanda [operación compartida](docs/operations/SHARED-OPERATIONS.md). No declarar conexiones ni aprobación comercial por existencia de archivos o éxito de tests.

## Herramientas compartidas
La configuración HTTP de Metricool está en `.mcp.json`; su autorización y disponibilidad se verifican por cliente. Leer `docs/operations/shared-tools-claude.md` antes de usar conexiones compartidas. No contar una configuración o relato de conexión como una sesión autenticada. Reutilizar briefs, archivos y evidencia del mismo proyecto; no copiar tokens entre asistentes. Para la primera comprobación usar marcas y analítica de El Tilichero en solo lectura.

---

# Altiora Enterprise OS (integrado el 01/11/2026)

<!-- ALTIORA_AUTOMATIC_CAPABILITIES_START -->
## Uso automático de capacidades de Altiora

El usuario autoriza seleccionar y aplicar automáticamente skills y agentes pertinentes a cada solicitud. No debe mencionar nombres, comandos ni pedir expresamente que se use una capacidad instalada. Esta regla incluye capacidades añadidas en el futuro; no mantener una lista cerrada de nombres.

- Al recibir una tarea, usar primero los nombres y descripciones que el cliente ya haya descubierto. Si falta una capacidad pertinente en ese inventario, inspeccionar los metadatos de las carpetas locales de skills del proyecto (.claude/skills en Claude; .agents/skills en Antigravity; skills/ para la biblioteca existente). Leer el cuerpo y referencias únicamente de las seleccionadas. No cargar toda la biblioteca.
- Resolver directamente trabajos pequeños. Para varias especialidades, elegir el coordinador pertinente por descripción y repartir responsabilidades cuando aporte valor. Esta autorización incluye delegación pertinente dentro del alcance de la tarea, siempre que el cliente disponga de subagentes reales. En Claude descubrir roles en .claude/agents; en Antigravity consultar altiora-os/agents como instrucciones cuando no exista delegación nativa. No afirmar que esos archivos crean agentes activos.
- No pedir al usuario que invoque una skill o agente por nombre ni que repita esta preferencia. Ante capacidades equivalentes, elegir una variante adecuada y conservar las demás. Respetar una elección explícita del usuario.
- Al añadir una capacidad, incluir nombre y descripción claros, instalarla en la ruta de descubrimiento del cliente, conservar sus recursos y verificar su descubrimiento cuando sea posible. No marcarla como exclusivamente manual salvo petición expresa. Tras una incorporación, indicar si el cliente necesita reabrir el proyecto para actualizar su inventario.
- La selección automática no autoriza acciones externas, gasto, publicación, cambios fuera del alcance ni ejecución de código no revisado. Los permisos reales del host y las instrucciones del proyecto siguen vigentes. No inventar herramientas, conexiones ni revisiones independientes.

No hace falta usar siempre el mismo agente: escoger la capacidad mínima que resuelva el encargo. Informar brevemente de las capacidades aplicadas cuando ayude a verificar una entrega, sin convertirlo en un paso que deba realizar el usuario.
<!-- ALTIORA_AUTOMATIC_CAPABILITIES_END -->

<!-- ALTIORA_AGENT_SYSTEM_START -->
## Altiora Agent System 1.3.0
Leer `.altiora/system/core/constitution.md` al empezar trabajo en este proyecto. Usar `.altiora/project.json` como contexto y `.altiora/handoff.json` si existe, contrastando siempre con el encargo vigente. Seleccionar skills por descripcion. Las instrucciones propias del proyecto y las del usuario siguen aplicando.
<!-- ALTIORA_AGENT_SYSTEM_END -->

<!-- ALTIORA_INDEX_ROUTING_START -->
## Índice maestro y verificación rápida
Consultar [`INDEX.md`](INDEX.md) y [`docs/altiora-toolkit/MAPA-CAPACIDADES.md`](docs/altiora-toolkit/MAPA-CAPACIDADES.md) para coordinadores, especialistas y skills. Desde la unificación del 01/11/2026 la fuente única de skills es `skills/`; `.claude/skills` y `.agents/skills` se generan con `npm run agents:build`. El índice anterior del Enterprise OS está en [`docs/altiora-toolkit/INDICE-ENTERPRISE-OS.md`](docs/altiora-toolkit/INDICE-ENTERPRISE-OS.md). `npm run check` valida el Lab y el sistema Enterprise (doctor y traspaso).
<!-- ALTIORA_INDEX_ROUTING_END -->

<!-- ALTIORA_VALUE_BUSINESS_START -->
## Negocio de Altiora · contexto bajo demanda
Para estrategia, oferta, clientes, precios, finanzas u operación de Altiora, consultar docs/altiora-business/INICIO.md y solo la sección necesaria. Objetivo fijado por el fundador: US$10.000 por proyecto, con mantenimiento mensual opcional separado; es una hipótesis sin validar con compradores (ver `docs/operations/ALTIORA-SCALE-ZERO-LOSS-V4.md`) y hay cero clientes de pago confirmados. Para empresas cliente, clasificar su etapa y validar presupuesto antes de proponer, según `docs/altiora-business/CASH-FIRST-ADAPTIVE-GROWTH.md`. Reutilizar capacidades disponibles y conservar tareas técnicas anteriores. No cargar toda la biblioteca, inventar resultados, atribuir habilitación profesional a roles IA, contactar, contratar o gastar por efecto lateral. Esta guía no concede nuevos permisos ni crea ejecución persistente.
<!-- ALTIORA_VALUE_BUSINESS_END -->

<!-- ALTIORA_CLAUDE_MASTER_START -->
## Contexto de Altiora bajo demanda
Contexto actual único, cargado automáticamente en cada sesión de Claude Code:
@docs/altiora-business/CLAUDE-ALTIORA-UNIFICADO.md

Abrir fuentes extensas solo cuando la tarea lo exija. Cargar `docs/altiora-business/ALTIORA-MAESTRO-PROYECTOS.md` solo al dirigir un proyecto integral o resolver una decisión material; consultar secciones pertinentes, no todo por cada mensaje. El prompt anterior `docs/altiora-toolkit/CLAUDE-MASTER.md` queda como referencia histórica: su tarea de revisión de calculadora no se activa automáticamente. Respetar accesos y permisos reales.
<!-- ALTIORA_CLAUDE_MASTER_END -->

<!-- ALTIORA_COORDINATOR_MODE_START -->
## Coordinación de Altiora · Enrutamiento Automático Multi-IA con Orca
Antes de un encargo con varias partes, largo o multidisciplinar, consultar al especialista `altiora-os-delegation` (`altiora-os/agents/altiora-os-delegation.md`): dice al usuario si conviene repartirlo en Orca o hacerlo en un solo chat, sin lanzar nada. Ante un mensaje único del usuario que abarque múltiples especialidades, se puede ejecutar `npm run orca:dispatch -- "mensaje"` (`scripts/orca-dispatch.py`) solo para ver un plan de reparto (flujos, IA sugerida y esfuerzo). Desde el 01/11/2026 el despachador está en modo solo plan: no registra tareas ni lanza agentes, y no se reactiva (`ALTIORA_DISPATCH_EXECUTE=1`) sin autorización expresa del usuario. La delegación la decide el usuario en Orca eligiendo la IA (`orca worktree create --agent ...`). Consultar `docs/altiora-toolkit/FLUJO-DELEGACION.md`. Resolver directamente cambios pequeños de un solo dominio.

## Economía de razonamiento (Claude, Codex y Gemini)
Elegir el esfuerzo de razonamiento más bajo que cumpla el criterio de aceptación: low para tareas mecánicas, medium por defecto, high solo para arquitectura, auditoría, investigación o diseño de escenas, y xhigh o max solo con riesgo económico, legal o de seguridad, o si el usuario pide profundidad. El tema (3D, marca, ventas) no justifica subir el nivel; lo justifica lo que se pide. Modelo grande solo en high o más (Claude: haiku o sonnet por debajo, opus en high; Antigravity: Gemini 3.8 Flash por debajo, Gemini 4 Argon solo en high, con `agy --model` y `--effort`). No dar a Gemini/Antigravity tareas fuera de 3D, WebGL o auditoría visual salvo que Claude y Codex estén sin créditos. Si una tarea resulta no ser la adecuada para la IA asignada, detenerse y decirlo en vez de seguir gastando. El despachador de Orca (`npm run orca:dispatch`) aplica estas reglas al sugerir IA y esfuerzo.
<!-- ALTIORA_COORDINATOR_MODE_END -->

<!-- ALTIORA_META_ADS_GROWTH_START -->
## Meta Ads · estrategia y medición
Para auditoría, plan o análisis de Meta Ads, leer bajo demanda `docs/altiora-toolkit/skills/meta-ads-growth/SKILL.md`. Para conceptos y guiones, reutilizar `meta-ads-creator` si está disponible. Esta referencia no conecta cuentas ni autoriza gasto, edición de campañas o publicación.
<!-- ALTIORA_META_ADS_GROWTH_END -->

<!-- ALTIORA_PROJECT_DIRECTOR_START -->
## Dirección de proyectos integrales
Para un proyecto multidisciplinar de Altiora, leer bajo demanda `docs/altiora-business/ALTIORA-MAESTRO-PROYECTOS.md` y aplicar la Parte III (Director de Experiencia y Resultados), junto con la propuesta y el estándar incluidos en el mismo archivo. No cargarlo para cambios pequeños. El rol no crea una sesión, garantiza resultados ni amplía permisos.
<!-- ALTIORA_PROJECT_DIRECTOR_END -->
