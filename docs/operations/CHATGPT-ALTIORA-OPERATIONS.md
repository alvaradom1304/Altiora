# Altiora OS — punto de entrada operativo desde ChatGPT

Fecha de auditoría: 2026-11-02. Fuente: GitHub `alvaradom1304/Altiora` (`main`).

## Propósito
Este documento es un **handoff** consultable desde ChatGPT mediante el conector de GitHub. No instala skills en ChatGPT, no crea herramientas MCP, no modifica las instrucciones de sistema de ChatGPT y no da acceso a la computadora del propietario. Volver a leer las fuentes al comenzar un encargo nuevo: no asumir carga automática entre chats.

## Orden de lectura para un encargo
1. Leer `AGENTS.md`, `team/ROUTING.md`, `docs/operations/SHARED-OPERATIONS.md` y `continuity/checkpoint.json`. No confiar solo en el checkpoint: comparar con `main` y GitHub Actions.
2. Consultar `INDEX.md` para hallar el rol y las skills pertinentes, después leer el contenido real de `team/agents/<rol>.md` y `skills/<skill>/SKILL.md`. Los archivos son instrucciones/recursos, NO subagentes automáticamente ejecutados en ChatGPT.
3. Para cada cliente leer `projects/<cliente>/`, diagnóstico y finanzas en `docs/altiora-business/`, y `docs/strategy/`. No inventar ventas, presupuesto, inventario ni derechos audiovisuales.
4. Elegir el mínimo conjunto de herramientas conectadas que resuelva el encargo. Confirmar identidad/acceso mediante una operación segura antes de depender de Figma, Adobe, Vercel, Higgsfield u otras herramientas.
5. Separar estados: `DOCUMENTADO`, `AUTENTICADO`, `PROBADO`, `PRODUCCIÓN VALIDADA` y `PENDIENTE`. No confundir un CI verde con calidad comercial o un MCP configurado localmente con un MCP accesible en ChatGPT.
6. Aplicar `quality/definition-of-done.md`, QA independiente y aprobación humana para publicar, gastar, contactar clientes, fusionar cambios o manejar información sensible.
7. Entregar siempre: Resultado, Evidencia verificable, Supuestos, Bloqueos y siguiente acción.

## Capacidades comprobadas en esta auditoría
- GitHub: lectura y permisos de escritura/administración del repositorio; árbol de `main` consultado.
- Catálogo: 355 archivos canónicos `skills/*/SKILL.md`; 32 adaptadores Markdown bajo `.claude/agents/`; `INDEX.md` presenta 22 identidades de agentes (son métricas diferentes).
- CI: `Check` completado satisfactoriamente en la revisión `355f893d` de `main`, 2026-11-02. Esto valida las pruebas del workflow, no todos los sistemas finales.
- Conectores de este chat: lectura autenticada de Figma, Higgsfield y listado de proyectos de Vercel. Las herramientas Adobe están expuestas, pero no se probó una operación real.
- Configuración local: `.mcp.json` registra servidores para Claude/local. No implica conexión de esos mismos servidores con este chat.
- No se ha ejecutado `npm run check` desde este chat en un checkout propio ni se ha validado la conectividad con Blender/After Effects/Orca locales.

## Guía de activación por dominio
- Negocio/cliente: `business-strategist`, `commerce-growth-director`, skills `aem-company-builder`, `business-diagnostic`, `financial-diagnostic`.
- Ads/video: Director de experiencia audiovisual y `creative-ads-director`; consultar `creative/visual-studio/ROUTER.md` y licencia/activos antes de generar.
- Web: `web-engineer`, `ux-researcher`, `qa-reviewer`; preferir pruebas en ramas y Vercel preview antes de producción.
- Investigación: `market-intelligence-director`; etiquetar datos comprobados y supuestos.
- Calidad: `quality/definition-of-done.md`, `npm run check` o GitHub Actions y revisión humana.

## Pendientes explícitos
- Probar herramientas Adobe con un recurso de prueba autorizado; no extrapolar de la exposición de API.
- Verificar integración local de Blender, After Effects, Orca, n8n y servidores MCP desde la máquina del propietario.
- No afirmar que ChatGPT puede invocar directamente los subagentes de Claude Code, Gemini o Codex.
- Comprobar derechos, datos de producto, presupuesto, vías de publicación y conversión para cada cliente.
