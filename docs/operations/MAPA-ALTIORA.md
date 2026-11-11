# Mapa de Altiora · dónde pedir y dónde mirar

Verificado 2026-11-10. Es un índice de navegación: no duplica ni mueve documentos y no concede permisos. El estado operativo vigente sigue en [ESTADO-ACTUAL](ESTADO-ACTUAL.md); los números de roles y skills, en el [INDEX](../../INDEX.md) generado.

## 1. Tres raíces distintas (no confundir)

| Qué es | Raíz local | Remoto | Para qué |
| --- | --- | --- | --- |
| **Empresa Altiora** (canónica) | `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado` | `alvaradom1304/Altiora` | Negocio, estrategia, equipo, skills, router, runtime, laboratorio y documentos de clientes |
| **Web cliente La Central del Queso** | `C:/Users/Usuario/OneDrive/Desktop/client-central-del-queso` | `alvaradom1304/la-central-del-queso` | Código de la web del piloto |
| **Carpeta de entrada del usuario** | `C:/Users/Usuario/OneDrive/Desktop/altiora` | `alvaradom1304/la-central-del-queso` (mismo remoto cliente, otra copia) | Contexto histórico y runtime de pruebas; no es la empresa aunque se llame `altiora` |

Antes de escribir o publicar: `git rev-parse --show-toplevel` y `git remote -v`; para publicar, `node scripts/project-identity.mjs --expected owner/repo` ([guía](PROJECT-IDENTITY.md)). El nombre de la carpeta no define la identidad Git.

## 2. Cuatro áreas, una sola fuente cada una

Son áreas de trabajo dentro de este repo, no repos ni orquestadores nuevos. El router de la sección 3 sigue decidiendo IA y rol.

| Área | Pedir aquí cuando… | Fuentes actuales | Roles |
| --- | --- | --- | --- |
| **Dirección** | Hay que decidir alcance, oferta, prioridades o a qué cliente dedicar tiempo | [INICIO del negocio](../altiora-business/INICIO.md) · [Maestro de proyectos](../altiora-business/ALTIORA-MAESTRO-PROYECTOS.md) · [OFERTA](../altiora-business/OFERTA.md) · [estrategia](../strategy/VISION-MISION-OBJETIVOS.md) · [gobierno](../../team/ROUTING.md) | experience-director, business-strategist |
| **Análisis** | Hace falta evidencia: mercado, finanzas, entrevistas, competencia, repos | [FINANZAS](../altiora-business/FINANZAS.md) · [DIAGNOSTICO.json](../altiora-business/DIAGNOSTICO.json) · [pipeline.json](../altiora-business/pipeline.json) · [RONDA-ENTREVISTAS-01](../altiora-business/RONDA-ENTREVISTAS-01.md) · [VALIDACION-COMERCIAL](../altiora-business/VALIDACION-COMERCIAL.md) · [investigación](../research/repository-review.md) | business-strategist, market-intelligence-director, growth-analyst |
| **Producción** | Hay que crear web, marca, anuncios, video, audio o 3D | [Visual Studio](../../creative/visual-studio/README.md) · [Ads OS](../../creative-ads-os/WORK_ROUTER.md) · [proceso inmersivo](../workflows/immersive-project.md) · [sistema de entrega](../altiora-business/entrega/README.md) · `skills/` · `projects/<cliente>/` | creative-director, web-engineer, visual-producer, audio-specialist, etc. |
| **Operación** | Preparar IAs, delegar, diagnosticar, cerrar, traspasar | [ESTADO-ACTUAL](ESTADO-ACTUAL.md) · [Orquestador local](ORQUESTADOR-LOCAL.md) · [Contrato de reporte](AI-REPORT-CONTRACT.md) · [Conectores y ahorro](CONECTORES-Y-AHORRO.md) · [Registro de grietas](REGISTRO-GRIETAS.md) · [continuidad](../../continuity/README.md) | ai-economist, qa-reviewer |

Prioridad del negocio: lo que acerca a un cliente que paga (hoy 0 clientes de pago, [INICIO](../altiora-business/INICIO.md)) va antes que infraestructura.

## 3. Cómo pedir un encargo

1. Abrir la sesión en la raíz correcta (sección 1) y decir **proyecto + resultado + qué no tocar**. Ejemplo: «Empresa: preparar la guía de la segunda entrevista, solo `docs/altiora-business`».
2. La IA lee `AGENTS.md`, aplica [team/ROUTING.md](../../team/ROUTING.md) y elige rol y skills; tú no tienes que nombrarlos.
3. Si el encargo es grande o multi-IA, el coordinador ejecuta `npm run altiora:ready` y `node scripts/orca-coordinator.mjs preflight` desde su propia sesión; cada archivo tiene un único escritor y la entrega la revisa otra IA ([AI-REPORT-CONTRACT](AI-REPORT-CONTRACT.md)).
4. Estado de las IAs hoy: **Claude** primera opción; **Antigravity** para 3D/visual y como revisor; **Codex pausado por cuota** (no es avería; solo vuelve si lo pides).

## 4. Empresa, clientes y laboratorio

| Elemento | Ubicación | Estado verificado |
| --- | --- | --- |
| Empresa / negocio | `docs/altiora-business/`, `docs/strategy/` en la raíz empresa | Oferta US$10.000 en validación; 0 clientes de pago; pipeline sin oportunidades reales |
| La Central del Queso (piloto) | Brief y documentos en `projects/la-central-del-queso/` (empresa); código en `client-central-del-queso` (repo cliente) | Piloto; sin ventas acreditadas ([PRUEBA-PILOTO](../altiora-business/PRUEBA-PILOTO.md)) |
| Tilicheros | `projects/tilicheros/` (documentos, discovery, captación) en la raíz empresa | Documentos del cliente dentro del repo empresa; no tiene remoto propio. `El-Tilichero-CR/`, `imagenes/`, `instagram/`, `master-v3/`, `proveedores/` están **sin versionar** (ajenos a este encargo) |
| Laboratorio | `experiments/`, `creative/`, `references/` | Experimentos separados del sitio comercial hasta validarlos |

Cada cliente se trabaja solo bajo su carpeta o su repo; no se mezclan datos entre clientes ni se copian al área de empresa.

## 5. Traspaso al terminar

Dejar en el informe del encargo: raíz y remoto saneado, archivos propios vs. ajenos, comandos con resultado, IDs de retorno de otras IAs, pendientes reales y modelo planeado vs. efectivo (`null` sin recibo). Actualizar [ESTADO-ACTUAL](ESTADO-ACTUAL.md) solo con lo probado. Para retomar: [continuidad](../../continuity/README.md) y `npm run resume`. Una sesión por tarea.

## 6. Acceso al grafo (Graphify)

- **MCP real en la sesión Claude del 2026-11-10:** servidor `graphify` en [`.mcp.json`](../../.mcp.json), grafo único de empresa `C:/Users/Usuario/.altiora-tools/graphs/altiora/graphify-out/graph.json` (sin `projects/` ni `out/`), `GRAPHIFY_BACKEND=none`. Regenerado el 2026-11-11 desde `6c6a887`: `graph_stats` devolvió 21.514 nodos / 24.542 aristas y 0 nodos de clientes; `query_graph` devolvió nodos de `scripts/orca-coordinator.mjs`. El grafo `altiora-20261110b` queda archivado. Otras IAs: no verificado.
- **Cobertura:** solo código y datos estructurados (`--code-only`). Incluye los scripts nuevos (`orca-coordinator`, `altiora-ready`, `omniroute-client`), pero **no** los documentos Markdown operativos (`ESTADO-ACTUAL`, `ROUTING`, `INICIO`: 0 nodos) ni `projects/`. Para documentos, la fuente es este mapa y los enlaces de arriba.
- El grafo es una ayuda de orientación; confirmar siempre en el archivo real. No contiene datos de clientes ni secretos por política de `.graphifyignore`.
