# Altiora OS — grafo modular / integración incremental
Estado: **ADAPTERS_DESIGNED / EXTERNAL_RUNTIME_NOT_CONNECTED**. Fecha: 2026-11-02.

## Esquema previo a cualquier modificación de los archivos de producción

```text
Usuario / Canal
    │ intención, client_id, permisos
    ▼
Altiora AGENTS.md / team/ROUTING.md (autoridad existente; NO REEMPLAZAR)
    │
    ▼
Bibliotecario / smart-model-router / Orca (selección local de tarea y skill)
    │        │
    │        └── OmniRoute GATEWAY [opcional, sólo si hay modelos API autorizados]
    │              └── proveedor/modelo elegido (NO reemplaza el router de tareas)
    │
    ├── Headroom [opcional]: compresión del payload activo recuperable
    ├── MemPalace [bajo demanda]: recuperar contexto histórico permitido
    ├── Playwright [bajo demanda]: navegador/pruebas web autorizadas
    ├── Frontend Design [skill local existente]: diseño/componentes Next.js
    └── ClaudeRed [bajo demanda]: sólo revisiones defensivas autorizadas
    │
    ▼
QA independiente -> Evidence/Handoff -> continuity/checkpoint.json
```

El grafo es una arquitectura lógica de adaptación, **no** un nuevo runtime activado. No se cambia el router de Next.js ni la topología existente. n8n se usa únicamente donde existan workflows reales; no añadir Langflow/Flowise sin necesidad demostrada.

## Auditoría de solapamientos (evidencia en repositorio)

| Capacidad propuesta | Ya existente | Decisión |
|---|---|---|
| Routing de tareas | `team/ROUTING.md`, `altiora-bibliotecario`, `scripts/orca-dispatch.py` | Mantener; no duplicar en OmniRoute |
| Routing de modelos | `smart-model-router` | OmniRoute sólo como *gateway* opcional, nunca segundo director |
| Análisis de grafo | `graphify` con `GRAPHIFY_BACKEND=none` | Reutilizar; no añadir framework de grafos alternativo |
| Diseño frontend | `skills/frontend-design`, `nextjs-architecture`, `react-three-fiber`, `gsap-animation` | Reutilizar; exportar componentes TSX compatibles |
| Browser QA | `webapp-testing` (Playwright) | Reutilizar skill; MCP de Playwright sólo si aporta ejecución real aislada |
| Memoria de continuidad | `continuity/checkpoint.json`, `altiora-session-handoff` | No indexar dos veces; MemPalace opcional para corpus consentido |
| Compresión | `smart-model-router`, Bibliotecario, `skills:compact` | Headroom sólo para salidas grandes; evitar doble compresión con OmniRoute |
| Seguridad | Skills de OWASP/QA; ClaudeRed sin importar | Incorporar sólo revisión defensiva con autorización |

## Contrato de nodo

Entrada mínima: `{job_id, intent, scope, authorized_tools, source_refs, constraints, token_budget}`.
Salida: `{job_id, node, status, artifact_refs, evidence_refs, next_action, cost_observed}`.
**Nunca** pasar transcriptos completos, secretos, credenciales ni archivos de otro cliente al nodo.
`authorized_tools` es lista explícita: una ruta no autoriza ejecución por sí sola. En errores, devolver `NOT_CONNECTED`/`NOT_VERIFIED` y fallback al flujo existente. Evitar invocaciones recursivas y fanout indiscriminado.

## Fuentes candidatas; revisión obligatoria antes de instalar

- Playwright: https://github.com/microsoft/playwright-mcp; ejecutarlo sólo en dominios autorizados y perfil de navegador aislado.
- OmniRoute: https://github.com/arnoldwender/omniroute; gateway para modelos, no *intent router* empresarial. **Conflicto** con Headroom por su motor interno de compresión; escoger un único compresor por tráfico.
- Headroom: https://github.com/headroomlabs-ai/headroom; compresión de salidas, no almacén de memoria principal. Desactivar escritura en prompts/AGENTS y hooks automáticos por defecto.
- MemPalace: https://github.com/MemPalace/mempalace; memoria local opt-in con ACL por cliente, borrado y TTL; no indexar chats ajenos por defecto.
- Frontend Design: existe `skills/frontend-design/SKILL.md`; no reemplazar con una segunda copia de la skill Anthropic.
- **ClaudeRed está ambiguo:** `kayleegeorge/claudered` es una plataforma gamificada de red teaming LLM (2023); `SnailSploit/claude-red` es una biblioteca ofensiva de skills. No fusionar ninguno automáticamente. Si se elige el segundo, importar exclusivamente criterios defensivos de revisión y QA tras inspeccionar licencia y contenido; no instalar playbooks ofensivos en producción.

## Activación y límites

1. `team/ROUTING.md` y Bibliotecario resuelven intención; acción simple se ejecuta sin nodos extras.
2. MemPalace solo se consulta si `context_missing=true`, identidad y permiso de cliente validados, y las fuentes locales/checkpoint no bastan; devolver como máximo fragmentos citados pertinentes.
3. Headroom solo en logs, JSON o resultados extensos; proteger código, valores de negocio y contratos; conservar recuperación reversible. No apilar Headroom con compresión agresiva de OmniRoute.
4. Playwright sólo con ejecución autorizada, entorno aislado y política de dominio, sin saltarse login ni CAPTCHA.
5. Frontend Design entrega `*.tsx` accesibles y componentes compatibles con Next.js/Tailwind/R3F/GSAP; sin añadir router, framework CSS ni controlador de scroll.
6. ClaudeRed sólo en rama de revisión con alcance y autorización documentados, sin pruebas activas sobre terceros.

## Validación antes de habilitar

- Capturar baseline: rutas elegidas, tokens totales de todos los modelos, coste, latencia, tasa de aceptación QA y fugas entre clientes (objetivo: cero).
- Probar por separado cada adaptador con fixtures; falla cerrada ante falta de permiso o ejecutable.
- Repetir `npm run check` con Node 20+ y Python 3.11+, y `npm run capability:doctor` en el entorno real. Ningún README prueba conexión local.
- Comparar 20 encargos representativos contra baseline; **no** prometer ahorro sin medición.
- No modificar `main` ni el sitio del cliente hasta revisión de PR y checks aprobados.
