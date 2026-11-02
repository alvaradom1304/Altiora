# Altiora · documento único para Claude

**Versión 2 · corte del 31 de octubre de 2026.** La versión 1 es de Codex; esta la actualizó Claude Code con verificaciones de la propia sesión. Claude Code la carga automáticamente desde `CLAUDE.md`. Abre fuentes extensas solo para la tarea pertinente. Este documento informa y orienta: no crea sesiones, no conecta herramientas y no concede acceso.

## Qué construimos

Altiora diagnostica, diseña e implementa sistemas de crecimiento para empresas. Según el problema puede combinar investigación de mercado, estrategia, branding y rebranding, redes, Meta Ads y otros anuncios, ventas, experiencia digital y presencial, tecnología, automatización, operación y análisis económico. Cada proyecto busca una experiencia completa para **la empresa que nos contrata y para sus consumidores**: claridad, utilidad, confianza, capacidad de operar lo entregado y cambios que se puedan medir.

- **Meta confirmada por el fundador:** US$10.000 **por proyecto**, con mantenimiento mensual opcional y aparte.
- **Realidad confirmada:** cero clientes de pago. Precio, demanda, costes, caja, capacidad y resultados comerciales siguen sin validar.
- La propuesta de web y consultas es un paquete piloto, no toda la firma.
- Ser reconocida como empresa de élite es una aspiración, no una promesa.

## Decisiones vigentes del fundador

| Fecha | Decisión | Dónde consta |
|---|---|---|
| 31/10/2026 | Alcance integral de la firma; el recorrido web es solo un paquete piloto | `POSICIONAMIENTO.md` |
| 31/10/2026 | **Presupuesto de planificación de 75 h por proyecto.** Es el máximo compatible con un margen del 25 % en el escenario de referencia; con 90 h queda en 17,5 %. Si una estimación supera 75 h, recortar alcance o cambiar el precio antes de firmar | `OFERTA.md:13,15`, `entrega/README.md` |
| 31/10/2026 | **El piloto registra los pedidos por API.** WhatsApp queda solo como aviso o procedimiento manual | `entrega/EJEMPLO-PILOTO.md` |

Si otro documento contradice esta tabla (por ejemplo, `ALTIORA-MAESTRO-PROYECTOS.md` aún dice 90 h), prevalece la decisión con fecha. Señala la diferencia.

## Cómo trabajar

- **Proyecto integral:** usa la skill `altiora-project-director`. En Claude es el **Director de Experiencia y Resultados**: define el resultado empresarial y el humano, estima la economía, coordina especialistas, revisa QA, exige aceptación expresa y registra el aprendizaje.
  - **Contexto y estándar:** `ALTIORA-MAESTRO-PROYECTOS.md`, partes II y III.
  - **Operación:** `docs/altiora-business/entrega/`, con las compuertas G1–G8, 10 plantillas, la lista de aceptación y `scripts/manifiesto.py` para comprobar que lo probado es lo entregado.
- **Hacer especial un proyecto:** `altiora-creative-analyst`, como skill y como agente. Al inicio de la definición escribe el brief diferencial con insight, territorio y un momento firma por canal; también audita piezas con la rúbrica anti-plantilla. La librería creativa por disciplina está en `MAPA-CAPACIDADES.md` §4 ter.
- **Vender:** `altiora-commercial-director`.
- **Caso empresarial abierto:** `company-builder-orchestrator`.
- **Meta Ads:** `meta-ads-growth` para estrategia y medición; `meta-ads-creator` para conceptos y guiones.
- **Tareas pequeñas:** trabaja directamente.

Selecciona solo las skills pertinentes; el routing completo está en `docs/altiora-toolkit/MAPA-CAPACIDADES.md`. Marca cada afirmación como `HECHO`, `SUPUESTO`, `HIPÓTESIS` o `NO VERIFICADO`. Entrega siempre el resultado, la comprobación y el límite.

No contactes prospectos, gastes, instales, publiques, cambies permisos o cuentas ni programes trabajo por esta ficha. Que una skill, un rol, un repo o un MCP esté configurado no acredita ejecución. Respeta el trabajo concurrente (Codex coordina: `docs/altiora-toolkit/ORQUESTADOR.md`) y la autoridad del fundador y del cliente. Antes de editar un archivo de otra sesión, deja constancia en la nota de traspaso.

## Mejora continua de capacidades

El fundador quiere que mejores de forma continua **las entregas y las herramientas de Altiora**: skills, agentes, subagentes, Superpowers, MCP, rutas y procesos. Hazlo dentro del encargo autorizado. No abras auditorías de toda la biblioteca ni crees agentes por cada mensaje. Al terminar el objetivo activo, detente.

- **Selecciona primero:** usa el inventario real de la sesión. Lanza subagentes reales solo cuando varias especialidades independientes lo justifiquen, cada uno con archivos propios y revisión.
- **Afila antes de añadir:** reproduce el fallo, conserva la variante anterior (en `.altiora/retired/`) y corrige el punto débil. Crea algo nuevo solo si hay un hueco concreto y un caso para evaluarlo.
- **Comprueba la fuente:** al traer algo de GitHub, fija versión y licencia, y añade `SOURCE.md` y `LICENSE.txt`. Regístralo en `docs/altiora-toolkit/skill-sources.json`. No ejecutes código sin leerlo.
- **Verifica el uso real:** distingue `DEFINIDO`, `INSTALADO`, `DESCUBIERTO` y `EJECUTADO`. No prometas ahorro sin medirlo.
- **No dupliques nombres entre runtimes:** Codex lee `~/.codex/skills` y `.agents/skills`; Claude, `.claude/skills` y `~/.claude/skills`.
- **Prioriza el negocio:** si el problema es falta de comprador, evidencia o capacidad, trabaja en eso antes de sumar otra herramienta.

## Estado verificado

Estado de cada línea (31/10/2026): **V** = verificado en una sesión de Claude ese día; **R** = registro recibido de otra sesión.

| Área | Estado | Límite |
|---|---|---|
| Negocio | R: propuesta maestra, estándar de doble experiencia, oferta piloto, finanzas y calculadora hipotéticas | No hay margen ni ventas reales |
| Entrega | V: paquete `entrega/` con 10 plantillas; tests del manifiesto 4/4 | Proceso hipotético, sin entregas de pago |
| Mercado | R: 8 páginas públicas estudiadas; 0 contactos y 0 entrevistas | El segmento logístico de Costa Rica es solo exploratorio |
| Piloto (La Central del Queso) | V: pedido por API implementado en `web` (main sobre `73519f0`), **sin commit**. 12/12 pruebas, `tsc` y `next build` PASS; manifiesto PASS | NO VERIFICADO: navegador, n8n real y destino durable en producción (en Vercel responde 503 a propósito) |
| Skills en Claude | V: descubiertas en sesión las 27 importadas de GitHub (incluye Superpowers y la librería creativa), las de Meta Ads, los directores y el analista creativo. Catálogo: 277 entradas, METADATA_CURRENT. Verificador de runtimes: 0 errores y 10 avisos (4 duplicados en Codex y 6 finales de línea mezclados en skills personales) | Agentes cargados pero no lanzados: ejecución NO VERIFICADA |
| Kit Altiora Agent System | V: 1.3.0 (verificador de runtimes y rol de analista creativo); `doctor` PASSED; bloque de versión actualizado en CLAUDE, AGENTS y GEMINI | Comprobación estructural; el descubrimiento real se ve en una sesión |
| MCP `altiora-shared` | V (02/11): una sola definición, `fixed-shared.mjs` sobre la carpeta `shared/`, igual en Claude (`~/.claude.json`), Codex y Antigravity; `claude mcp get altiora-shared` → Connected. Se quitó la entrada de `.mcp.json`, que exponía las carpetas de la sesión en vez de `shared/` | Es la carpeta de coordinación, no el repo: cada IA lee el repo canónico directamente. Detalle: `docs/operations/VERIFICACION-CONEXIONES-2026-11-02.md` |
| Graphify | V (02/11): por CLI con `GRAPHIFY_BACKEND=none` en las tres IAs; grafo regenerado desde la copia canónica | Sin servidor MCP: el de `.mcp.json` fallaba al arrancar (faltaba el módulo `mcp`) y se retiró |
| Conectores claude.ai | V: Gmail, Slack, Notion, HubSpot, Canva, Figma, Vercel, Ahrefs, Supermetrics y Claude Docs conectados | Conectado ≠ autorizado para usarlo. Los 13 servidores de plugins sin autenticar requieren `/mcp`; marketing/gmail y calendar fallan por falta de URL |
| Máquina | R: Node, Python, Blender, FFmpeg y FFprobe detectados; aerender no | V (02/11): `claude`, `codex` y `agy` están en el PATH |
| Informe de calculadora | R: `context/CLAUDE-CALCULATOR-REVIEW.md` en la carpeta privada compartida | Esta sesión no tiene acceso a esa carpeta: NO VERIFICADO |

## Pendientes materiales

1. **Fundador:** autorizar la prueba en navegador del piloto (servidor local), elegir el destino durable de producción y conseguir revisión legal y contable de las cláusulas marcadas `[REVISIÓN PROFESIONAL]`.
2. **Codex:**
   - dejar una sola `altiora-project-director` (hoy hay versiones distintas en `~/.codex/skills` y `.agents/skills`);
   - pasar a 75 h `ALTIORA-MAESTRO-PROYECTOS.md` y la calculadora;
   - reevaluar `PRUEBA-PILOTO.md` frente al código nuevo.
3. **Negocio, la prioridad:** preparar entrevistas con compradores reales. Ninguna herramienta sustituye esa evidencia.

## Fuentes bajo demanda

- **Dirigir un proyecto:** `docs/altiora-business/ALTIORA-MAESTRO-PROYECTOS.md` y `docs/altiora-business/entrega/README.md`.
- **Negocio:** `docs/altiora-business/INICIO.md` y solo la sección necesaria.
- **Capacidades:** `docs/altiora-toolkit/MAPA-CAPACIDADES.md` y `AUDITORIA-HERRAMIENTAS-2026-10-31.md`.
- **Orca:** `docs/altiora-toolkit/ORCA-ALTIORA.md`.
- **Laboratorio:** `docs/operations/SHARED-OPERATIONS.md`.

No busques otras rutas para ampliar permisos.

**Comprobación nativa:** al retomar, si hay un cambio o una duda material, comprueba qué instrucciones, roles y herramientas ves en la sesión y el estado de los conectores, sin cambiar configuraciones. Si no puedes inspeccionarlo, márcalo `NO VERIFICADO`. No repitas una revisión ya documentada en la tabla anterior sin motivo.
