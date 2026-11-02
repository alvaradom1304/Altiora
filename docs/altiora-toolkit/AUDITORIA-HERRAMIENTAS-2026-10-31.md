# Auditoría y consolidación de herramientas de Altiora · 31/10/2026

Encargo: «afilar el hacha»: auditar skills, agentes y coordinadores, consolidarlos y añadir lo que falta para la oferta de US$10.000 por proyecto. El usuario autorizó un cambio de fondo. Se aplicó sin borrar nada, sin commits y sin tocar los archivos que coordina Codex (`.altiora/handoff.json`, `CLAUDE.md`, `docs/altiora-toolkit/CLAUDE-MASTER.md`). Ejecución: una sesión de Claude Code, sin subagentes.

Routing resultante: [MAPA-CAPACIDADES.md](MAPA-CAPACIDADES.md).

## 1. Inventario (antes → después)

| Ubicación | Antes | Después | Runtime |
|---|---|---|---|
| `.claude/skills` | 16 | 34 (+17 importadas de Codex, +3 nuevas, −2 retiradas) | Claude Code |
| `.claude/agents` | 12 | 11 (−1 retirado; 2 redefinidos) | Claude Code |
| `~/.claude/skills` | 30 | 30 (bibliotecario sincronizado) | Claude Code, todos los proyectos |
| `~/.claude/agents` | 4 | 4 | Claude Code |
| `.agents/skills` | 157 entradas (148 con `SKILL.md`, 9 carpetas de categoría) | 160 (+3 nuevas) | Codex y Antigravity |
| `.codex/agents` | 4 | 4 | Codex |
| `~/.codex/skills` | 243 | 243 | Codex |
| `altiora-os/agents` | 8 | 7 (copias sincronizadas) | fuente portable |
| Laboratorio (`2026-10-30`, `main`) | `skills/` 253 entradas, `team/ROUTING.md` | sin cambios | repositorio aparte |

Descubrimiento verificado tras los cambios: 62 skills y 15 agentes de Claude con frontmatter válido, `name` igual a la carpeta, descripción de 60–1024 caracteres y ninguna referencia inexistente en los coordinadores ni en el mapa (script de validación propio, parser de respaldo sin PyYAML).

## 2. Problemas encontrados, por prioridad

### P1 · Bloquean la oferta o la autoselección

1. **Claude no podía cargar la pila comercial que la propia operación exige.** `docs/altiora-business/OPERACION.md:10-16` asigna `high-ticket-offer`, `customer-research`, `financial-diagnostic`, `capacity-planning`, entre otras; `OFERTA.md:57` se hizo con `~/.codex/skills/high-ticket-offer`. Ninguna estaba en `.claude/skills` ni en `~/.claude/skills`. **Corregido:** se importaron 17 skills de venta, finanzas y entrega (§4).
2. **Ningún coordinador para vender ni para entregar un proyecto.** Había cuatro coordinadores genéricos que se solapaban (`altiora-os-coordinate` como skill y como agente, `altiora-agent-orchestrator`, `company-builder-orchestrator`) y ninguno cubría el ciclo prospecto → propuesta → entrega → caso. **Corregido:** `altiora-commercial-director` y `altiora-project-director`.
3. **Coordinadores definidos como subagentes.** En Claude Code un subagente no puede lanzar otros subagentes, así que el agente `altiora-os-coordinate` no podía delegar. **Corregido:** retirado; los directores son skills de la sesión principal.
4. **Descripciones truncadas a 180 caracteres a mitad de palabra.** `.claude/agents/altiora-engineering.md:3` terminaba en «Eje», `altiora-experience` en «movim», `altiora-research` en «compatibilida» y `altiora-review` en «por ». Causa raíz: `.altiora/system/scripts/manage.py:172` (`[:180]`). **Corregido en el generador** (kit 1.1.0, §5 bis): cada rol declara su descripción completa en el frontmatter.
5. **`company-builder-orchestrator` enviaba a skills no descubribles y contradecía las reglas.** El original (`kit-originals/…/company-builder-orchestrator/SKILL.md`) remitía a `aem-venture-architect` y `business-health-assessment` en las líneas 23-24, que solo existen en `.agents/skills`; tenía secciones numeradas dos veces (13/16 y 20/41); y en la línea 45 pedía hablar «orientado a ROI», en contra de la regla de no prometer retorno. Además se presentaba como «orquestador principal». **Corregido:** reescrito como clasificador A–H con skills disponibles en Claude.

### P2 · Herramientas mal asignadas y rutas rotas

6. **Revisor que no puede reproducir.** El agente `altiora-review` tenía `tools: Read, Glob, Grep`, pero su descripción pedía «reproducir los problemas». `altiora-research` tampoco tenía acceso web. Origen: `manage.py:176` fijaba las herramientas según el sufijo del nombre; ahora cada rol las declara en `tools` (kit 1.1.0). **Corregido:** `altiora-os-qa` (todas las herramientas, incluido el navegador) es el revisor de aceptación y aplica `altiora-quality-review`, `web-quality-assurance` y `accessibility`. Los dos agentes del kit se redefinieron como «revisión estática» e «investigación local». No se pueden retirar: el instalador del kit los restauró a las 14:34:18 tras moverlos.
7. **`altiora-experience` no podía guardar su entregable** (solo lectura). **Corregido:** se le añadieron `Write`, `Edit`, `WebFetch` y `WebSearch`. `altiora-engineering` hereda ahora todas las herramientas, para poder verificar en el navegador.
8. **Referencias rotas en `altiora-agent-orchestrator`**: la línea 20 citaba `altiora-repository-research` (no existe en Claude) y la línea 24 citaba `.agents/agents/` (no existe). **Corregido:** ahora remiten a `altiora-os-research`, `.claude/agents` y `.codex/agents`.
9. **Laboratorio desfasado.** `references/altiora-workspace.md:3`, en el orquestador y en `altiora-quality-review`, apuntaba a `Codex/2026-10-18/…`, una copia sin Git. `CLAUDE-MASTER.md` y `~/.claude/CLAUDE.md:46` usan `2026-10-30` (`main`, PR42), y el MCP `altiora-shared` expone `2026-10-29` (rama de docs, commit f332c3c). **Corregido** en las dos referencias locales. **Pendiente:** alinear el MCP (§6).
10. **Copia personal del Bibliotecario desfasada.** El `library.py` de `~/.claude/skills/altiora-bibliotecario` (hash `ef492c7d…`) no coincidía con el del laboratorio ni con el del proyecto (`eced56bf…`), y le faltaba `test_evaluate_routes.py`. **Corregido:** sincronizada; la anterior se respaldó en `home-skills/`.
11. **`~/.claude/CLAUDE.md:9` remite a `team/ROUTING.md` y `skills/INDEX.md`**, que existen en el laboratorio pero no en este proyecto. No es un error, aunque confunde. El mapa canónico del proyecto es ahora `MAPA-CAPACIDADES.md`.

### P3 · Duplicados y vaguedad

12. **Duplicados funcionales**: `altiora-os-qa` (skill) ≈ `altiora-quality-review`; `altiora-os-coordinate` (skill) ≈ `altiora-agent-orchestrator`; `altiora-research` ≈ `altiora-os-research`; `altiora-review` ≈ `altiora-os-qa`. **Corregido:** retirados o redefinidos (mapa, §5).
13. **Descripciones que no permiten elegir**: el patrón generado «`x: Sales Intelligence. Usar para producir campo_a, campo_b…`», `business-diagnostic` y las ocho `altiora-os-*`, sin cuándo usarlas ni en qué se diferencian. **Corregido:** 27 descripciones reescritas con disparador («Usar cuando…») y desempate.
14. **`.agents/skills` incompleta para Antigravity**: faltan 105 skills de `~/.codex/skills`, casi todas de la «n» a la «z» (`negotiation` … `working-capital`), además de `high-ticket-offer`, `pricing` y `sales-*`. Parece una copia interrumpida. Además, 9 carpetas de categoría (`branding/`, `sales/`, `Altiora_OS_4_Tactical_Skills/`, etc.) anidan copias de skills que ya existen en el nivel superior. **No corregido** (es territorio de Codex/Antigravity; §6).

## 3. Consolidación aplicada

| Acción | Elementos |
|---|---|
| Crear | skills `altiora-commercial-director`, `altiora-project-director`, `altiora-case-study` (también copiadas en `.agents/skills`) |
| Importar a Claude | `high-ticket-offer`, `problem-validation`, `mom-test-interviewing`, `lead-qualification`, `sales-discovery`, `sales-objection-analysis`, `sales-proposal`, `sales-follow-up`, `value-proposition-design`, `pricing`, `unit-economics`, `launch-readiness`, `web-quality-assurance`, `accessibility`, `nextjs-architecture`, `n8n-webhook-architect`, `customer-success` (sin scripts ni rutas absolutas; revisadas antes de copiar) |
| Fusionar o retirar | skills `altiora-os-coordinate` y `altiora-os-qa`; agente `altiora-os-coordinate` |
| Redefinir | agentes `altiora-review` (estático) y `altiora-research` (local); `altiora-os-qa` como revisor con ejecución |
| Reescribir | `company-builder-orchestrator`; 27 descripciones de skills; 11 de agentes |
| Alinear routing | `MAPA-CAPACIDADES.md` (un coordinador por encargo, ciclo de la oferta y desempates) y un enlace en `ROUTING.md` |
| Catálogo | `.altiora/catalog.local.json` reconstruido con sus 4 raíces: 216 entradas, `METADATA_CURRENT` (copia previa en el archivo) |

Todo lo retirado y todos los originales del kit, con hash verificado, están en `.altiora/retired/20261031-claude/`.

## 4. Por qué esto acerca a «la élite»

La oferta ya estaba bien definida en `OFERTA.md`; lo que faltaba era que la herramienta la ejecutara de principio a fin. Ahora cada etapa tiene una skill descubrible y una compuerta:

- **Vender:** validación del problema → calificación → entrevista Mom Test o descubrimiento → oferta, margen y precio → propuesta → objeciones y seguimiento (solo borradores).
- **Entregar:** seis semanas con responsable por fase, QA independiente con navegador, preparación del lanzamiento, aceptación expresa y éxito del cliente.
- **Demostrar:** caso de estudio verificable para salir de cero clientes sin inventar pruebas.

Las herramientas no sustituyen la evidencia comercial: las compuertas de validación siguen en HOLD hasta tener entrevistas reales (`OPERACION.md`).

## 5. Verificación

| Comprobación | Resultado |
|---|---|
| Descubrimiento de skills nuevas en esta sesión | DISCOVERED: el cliente listó las 17 importadas y las 3 nuevas sin reabrir |
| Frontmatter, nombres y referencias (script propio) | 62 skills y 15 agentes; sin problemas |
| `library.py check` tras reconstruir | `METADATA_CURRENT`, 216 entradas; búsquedas de prueba devuelven los directores |
| Pruebas del Bibliotecario | 26/27; la que falla requiere la estructura del laboratorio (`REPO_ROOT/skills`) y falla igual antes del cambio |
| `manage.py doctor` (kit 1.1.0) | PASSED: 92 archivos gestionados, sin errores; `handoff-check` PASSED |
| Agentes nuevos o redefinidos en una sesión real | NOT_VERIFIED: Claude Code carga los agentes al iniciar la sesión; hace falta abrir una sesión nueva |

## 5 bis. Corrección del kit (Altiora Agent System 1.1.0)

Fuente: `C:/Users/Usuario/Documents/Codex/2026-10-18/cr/outputs/altiora-agent-system` (sin Git; copia previa en `.altiora/retired/20261031-claude/kit-source-backup/`).

- `scripts/manage.py`:
  - Los roles aceptan frontmatter con `description` y `tools`; `tools: inherit` hace que el agente herede las herramientas de la sesión.
  - Sin frontmatter se mantienen las herramientas anteriores y la descripción se acorta en un límite de palabra, no a mitad de palabra.
  - El recibo registra también los archivos que ya coinciden con lo esperado.
  - Nuevo comando `adopt --path … [--apply]`, para aceptar ediciones locales ya revisadas, con transacción y rollback.
- `roles/*.md`: frontmatter con las descripciones y herramientas de este informe. Engineering hereda las herramientas de la sesión; experience añade escritura y web; research y review siguen en solo lectura, de forma declarada y coherente con su descripción.
- Documentación: `docs/COMPATIBILITY.md`, `README.md`, `CHANGELOG.md` y `package.py` (la versión ya no está fija). `manifest.json` regenerado; `package.py --verify` PASSED. El ZIP 1.0.0 publicado no se tocó.
- Pruebas: 24/24 (20 existentes + 4 nuevas: frontmatter, modo de respaldo sin cortar palabras, registro en el recibo, y `adopt` con su rollback).
- Despliegue en el proyecto:
  - Transacción `20261031T204919Z-33b8c238`: instalación 1.1.0, sin `CLAUDE.md`, `AGENTS.md` ni `GEMINI.md`. Los `.toml` de Codex se regeneraron con las descripciones completas; los anteriores están en `kit-originals/.codex/agents/`.
  - Transacción `20261031T204930Z-4db7501a`: `adopt` de las 6 mejoras de skills.
  - Para revertir: `python .altiora/system/scripts/manage.py rollback --target . --transaction <id> --apply`, empezando por la más reciente.
- Incidencia corregida: en este Windows, Python escribe CRLF. Durante el trabajo cambió los finales de línea de 45 archivos; se restauró en cada uno la convención de su original.

## 6. Pendientes fuera de este alcance (dueño: Codex o el laboratorio)

1. **Resuelto:** generador del kit corregido; ver §5 bis. Falta que Codex actualice la línea de versión del bloque del kit en `CLAUDE.md`, `AGENTS.md` y `GEMINI.md` (dice 1.0.0; no se tocó porque son archivos del coordinador; `doctor` no lo exige).
2. **`.agents/skills` para Antigravity:** completar las 105 skills que faltan, decidir qué hacer con las carpetas de categoría anidadas y propagar las descripciones nuevas.
3. **Resuelto el 02/11/2026:** `altiora-shared` expone solo la carpeta de coordinación `…/2026-10-18/…/altiora-connection/shared`, con la misma definición en las tres IAs; el laboratorio se lee directamente desde la copia canónica. Ver `docs/operations/VERIFICACION-CONEXIONES-2026-11-02.md`.
4. **`FINANZAS.md:76-79`** cita `altiora-os-coordinate`, `altiora-research` y `altiora-review`: siguen siendo válidas en Codex; en Claude, consultar el mapa.
5. Llevar al laboratorio los directores, el caso de estudio y las importaciones, para que la fuente de verdad los contenga y una reinstalación no los pierda.

## 7. Importación desde GitHub (31/10/2026, mismo método que Codex)

Método: los mismos 4 repositorios que Codex evaluó el 18/10 (`anthropics/skills`, `obra/superpowers`, `coreyhaines31/marketingskills`, `vercel-labs/agent-skills`), clonados en modo de solo lectura en el scratchpad. Por cada skill se fijó la revisión y se añadieron `LICENSE.txt` y `SOURCE.md`; el registro está en `docs/altiora-toolkit/skill-sources.json`. No se ejecutó código de ningún repositorio.

- **Instaladas (21)**, en `.claude/skills` y `.agents/skills`, por etapa de la oferta:
  - venta: `cold-email`, `sales-enablement`, `competitor-profiling`, `copy-editing`;
  - definición: `site-architecture`, `brainstorming`;
  - construcción: `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `test-driven-development`, `frontend-design`, `vercel-react-view-transitions`, `mcp-builder`;
  - revisión: `requesting-code-review`, `receiving-code-review`;
  - entrega: `conversion-tracking`, `launch`, `finishing-a-development-branch`;
  - mantenimiento: `attribution`, `ai-seo`;
  - herramientas: `writing-skills`.
- **Cambios locales:** descripción en español con desempates. Nota «Uso en Altiora» en `cold-email` (solo borradores), `brainstorming` (servidor local solo si se acepta), `finishing-a-development-branch` (commit, push y PR con confirmación), `conversion-tracking` (scripts leídos; GTM y cuentas con autorización) y `mcp-builder` (sin instalar dependencias ni usar credenciales).
- **Contexto de producto:** 19 skills de marketingskills, incluidas las 11 que importó Codex, leen primero `.agents/product-marketing.md`. Ese archivo no existía, así que trabajaban sin el contexto de Altiora. Se creó como índice: distingue los encargos de Altiora de los de un cliente y remite a `docs/altiora-business/`.
- **Directores:** `altiora-commercial-director` (etapa 2b de primer contacto, material de venta) y `altiora-project-director` (sitemap, plan, TDD, revisión, medición, lanzamiento) enlazan ya estas skills; sus copias en `.agents/skills` son idénticas.
- **Descartadas, con motivo:**
  - `deploy-to-vercel` y `vercel-cli-with-tokens`: actúan fuera del equipo y con tokens;
  - `vercel-optimize`: requiere métricas y credenciales de Vercel;
  - `writing-guidelines`: descarga sus reglas en cada uso;
  - `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator` y `claude-api`: ya disponibles en Claude como plugin;
  - `aso`, `paywalls`, `signup`, `onboarding`, `churn-prevention` y `sms`: son para SaaS o apps móviles;
  - `doc-coauthoring` y `product-marketing`: solapan con `sales-proposal` y `value-proposition-design`;
  - `marketing-council`, `public-relations` y `revops`: no son prioritarias sin un primer cliente.
- **Verificación:**
  - Claude Code descubrió las 21 en caliente, en esta misma sesión.
  - El frontmatter es válido en `.claude/skills`, `.agents/skills` y `~/.claude/skills`: 0 problemas, nombres iguales a sus carpetas y descripciones de ≤1024 caracteres.
  - El catálogo tiene 258 entradas y está en METADATA_CURRENT.
  - `doctor` y `handoff-check` dan PASSED.
  - El buscador léxico del Bibliotecario devuelve `cold-email`, `conversion-tracking` y `requesting-code-review` para consultas en español. `site-architecture` queda en el puesto 4 porque el alias `web` favorece a `nextjs-architecture`; `library.py` no se tocó porque está sincronizado con el laboratorio.
  - Codex y Antigravity: NOT_VERIFIED en una sesión real; requieren reabrir el proyecto.
- **Actualizaciones pendientes de las importaciones de Codex:**
  - Upstream tiene versiones de parche nuevas de `ab-testing` (2.0.2 → 2.0.4), `analytics` (2.2.0 → 2.2.2), `free-tools` (2.0.2 → 2.0.3) y `lead-magnets` (2.1.0 → 2.1.1).
  - `web-design-guidelines` difiere a propósito: Codex fijó sus reglas.
  - Las otras 13 coinciden. Dueño: Codex, en el laboratorio.
