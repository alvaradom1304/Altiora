# Conectores bajo demanda y ahorro de tokens

Regla común para Claude Code, Codex, Antigravity y Orca. Cada conector encendido carga los nombres de todas sus herramientas en **cada** turno, aunque no se usen. Por defecto se mantienen apagados los pesados; se encienden solo cuando la tarea los necesita y se apagan al terminar.

## Cuándo activar cada conector

| La tarea pide… | Conector | Herramientas aprox. |
|---|---|---|
| Publicar o revisar un despliegue web, dominios, logs de producción | Vercel | 244 |
| SEO: palabras clave, backlinks, competencia orgánica, auditoría de sitio | Ahrefs | 157 |
| Leer o escribir páginas o bases de Notion | Notion | 68 |
| Diseños en Canva (crear, exportar, plantillas) | Canva | 42 |
| Leer un archivo de Figma o pasar diseño a código | Figma | 42 |
| Leer o redactar correos | Gmail | 30 |
| CRM: contactos, negocios, campañas en HubSpot | HubSpot | 29 |
| Leer o enviar mensajes de Slack | Slack | 27 |
| Analítica de anuncios multiplataforma | Supermetrics | 21 |

Siempre encendidos (ligeros y de uso diario): Metricool (redes de Tilicheros, `.mcp.json`), `altiora-shared`, `altiora-after-effects` (solo preflight y plan) y Claude Docs.

**Cómo activar:**
- **Claude Code:** menú «+» → Conectores, o la herramienta de conectores de la sesión si el usuario lo pide. Se aplica desde el turno siguiente.
- **Codex y Antigravity:** solo usan los servidores de `.mcp.json` y de su configuración. Si falta uno, dilo y propón activarlo; no lo instales.

Activar un conector no concede permiso para publicar, enviar ni gastar: cada acción externa sigue necesitando aprobación.

## Hábitos que ahorran sin perder calidad

1. **Una sesión por tarea.** Al terminar, deja el traspaso (`altiora-session-handoff`) y empieza un chat nuevo. Una sesión larga relee todo el historial en cada mensaje: es la mayor fuente de gasto.
2. **Modelo y esfuerzo mínimos que cumplan** (`team/ROUTING.md` §3): Sonnet o Flash por defecto; Opus, Argon high o GPT con esfuerzo alto solo para arquitectura, decisiones difíciles o depuración profunda.
3. **Subagentes solo si el paralelismo compensa.** Cada uno vuelve a leer todas las instrucciones fijas (100.000 tokens o más). Para leer pocos archivos, hazlo tú.
4. **Salidas cortas.** Muestra solo el final de los logs (`| tail`), y no pegues archivos enteros si basta una sección.
5. **Graphify antes que grep masivo,** siempre con `GRAPHIFY_BACKEND=none` (skill `graphify`).
6. **Plugins sin uso fuera.** Los que piden iniciar sesión y no se usan (Windsor.ai, Marketing, Adobe, SearchFit) listan skills largas en cada turno; desactívalos en la configuración de plugins.

**Responsable:** el rol `ai-economist` (`team/roles/ai-economist.md`) aplica estas reglas y entrega el plan de economía de cada tarea grande. Medir una sesión: `npm run usage:report -- <transcript.jsonl>`.

Medición de referencia (sesión del 2026-11-01, 576 turnos): 33 % historial releído, 27 % subagentes, 25 % instrucciones fijas (unos 150.000 tokens por turno con todos los conectores encendidos).
