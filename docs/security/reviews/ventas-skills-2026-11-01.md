# Revisión de seguridad: skills de ventas (bloque B)

Fecha: 2026-11-01. Rama: `feature/altiora-ventas-skills`. Aprobación del dueño: bloque B de la [propuesta](../../operations/propuesta-equipo-ia-2026-11-01.md). Gate: [third-party-skill-gate](../third-party-skill-gate.md).

## Estado del gate

| Paso | Estado |
|---|---|
| 1. Cuarentena sin ejecutar | **Hecho.** Clon superficial sin checkout y extracción solo de las carpetas elegidas en `.references/quarantine-2026-11-01/` (ignorada por Git) |
| 2. Revisión manual | **Hecho** (abajo) |
| 3. `npm run security:scan` | **Hecho.** SkillSpector 2.12.0 (commit revisado `54921c8`), instalado en un entorno virtual en `C:/Users/Usuario/.altiora-tools/skillspector` (fuera del repo por el límite de rutas de Windows). Modo estático `--no-llm` |
| 4. Adaptación e integración | **Hecho** en `skills/`, con `LICENSE.txt` y `SOURCE.md` por skill |
| 5. `agents:build` y `check` | Ver commit del bloque |

## Fuentes fijadas

| Repo | Commit | Licencia | Carpetas extraídas |
|---|---|---|---|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | `2574e29377c7173d0cecffef29a6ecbd7f8ccb5d` | Apache-2.0 (`sales/LICENSE`) | `sales/skills/{account-research, call-prep, draft-outreach, call-summary, close-plan}` |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | `88c79f6528a9347420e57ceb1fff9a60de651768` | MIT | `skills/{cold-email, sales-enablement, revops}` |

No se extrajeron `sales/.mcp.json` ni `.claude-plugin/plugin.json`, que configurarían conectores remotos.

## Revisión manual

- **Contenido:** 5.336 líneas, solo Markdown y JSON de evaluaciones. No hay scripts, hooks, binarios ni dependencias.
- **Patrones buscados:** `curl`, `wget`, `npx`, `pip install`, `.env`, `ssh`, claves, tokens, `eval`/`exec`, URLs `http://`. Ninguno, salvo las URLs de la licencia Apache.
- **Red:** `revops` enlaza a guías de integración en GitHub (HubSpot, Apollo, Zapier…). Son enlaces de lectura; no se copian ni se siguen.
- **Conflicto con las reglas de Altiora (debe corregirse al adaptar):** las 5 skills de `sales` dicen que, cuando el usuario pide una acción (enviar un correo, publicar en un chat, actualizar el CRM, agendar), se ejecute por el conector y que no se rechace por criterio propio. En Altiora, enviar mensajes, escribir en el CRM o agendar requiere confirmación explícita por acción. La adaptación las deja en **modo borrador**: redactar y proponer cambios; ejecutar solo con un sí explícito.
- **A favor:** tratan correos, transcripciones y datos externos como contenido no confiable y piden mostrar al usuario cualquier acción que salga de ese contenido antes de ejecutarla. Coincide con Altiora.
- **Correo en frío:** `cold-email` cubre configuración de envío y cadencias. En Costa Rica aplica la Ley 8968 de protección de datos; la adaptación debe exigir base legal y opción de baja, y no automatizar envíos. **Sin revisión legal.**
- **Solapamientos con el catálogo:** `call-prep` con `sales-discovery`, `cold-email` con `cold-outbound-system` y `prospecting`, `sales-enablement` con `sales-objection-analysis`. Se propone que las importadas entren al núcleo y que las solapadas sigan en reserva.

## Resultados del escaneo

| Skill | Original (cuarentena) | Adaptada (catálogo) | Hallazgos y decisión |
|---|---|---|---|
| account-research, call-prep, call-summary, close-plan, draft-outreach | CAUTION 21 | **SAFE 0** | AR1 (HIGH), real: la regla «no rechazar acciones pedidas». Se sustituyó por el modo borrador de Altiora |
| cold-email | CAUTION 25 | **SAFE 0** | AR1 «always respond» y EA2 «without consent»: falsos positivos (frase descriptiva y regla de cumplimiento). Se reformularon sin cambiar el sentido y se añadió la nota de la Ley 8968 |
| sales-enablement | SAFE 7 | **SAFE 7** | EA2 «without asking»: consejo para guiones de demo («hablar más de 3 minutos sin preguntar»). Benigno |
| revops | SAFE 20 | **SAFE 20** (en el límite) | EA2 «Auto-approve» y 2 × RA2 «Create task for»: describen reglas de un CRM, no acciones del agente. Benigno |

Un SAFE no autoriza por sí solo: la revisión manual de arriba y estos hallazgos forman la revisión humana del gate. Las 8 entran al núcleo (`references/skill-core.json`, lista `sales`) por decisión del dueño del 2026-11-01.

## Pendiente

- Autorizar HubSpot en `/mcp`, en solo lectura (lo hace el dueño).
- Revisión legal del correo en frío según la Ley 8968. Avance 2026-11-12: [correo-comercial-no-solicitado-cr-2026-11-12.md](../../research/correo-comercial-no-solicitado-cr-2026-11-12.md) (Ley 8642 art. 44 y Ley 10946 art. 29; falta abogado).
- Volver a escanear si se actualiza cualquiera de las fuentes.

## Integración en `altiora-unificado` (2026-11-01)

La rama unificada ya contenía `cold-email` y `sales-enablement` de la misma revisión (`88c79f6`), importadas el 2026-10-31, traducidas al español y con notas de uso de Altiora (solo borradores). **Se conservan esas versiones** y no se sustituyen por las de esta revisión. Solo se añaden las 6 nuevas: account-research, call-prep, call-summary, close-plan, draft-outreach y revops. Las 8 forman la lista `sales` del núcleo.

**Aviso:** la versión de `cold-email` que ya estaba en `altiora-unificado` da CAUTION 25 con SkillSpector (los mismos dos falsos positivos: «always respond» y «without consent»). No se modifica en esta integración; queda para quien mantenga esa importación.
