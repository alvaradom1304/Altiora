# Graphify MCP: validación en frío con MCP_TIMEOUT=60000 (2026-11-10)

Estado: **implementado-pendiente-QA** (sin autoaprobación; QA independiente pendiente).

## Identidad del encargo

- Workspace (VERIFICADO, `git rev-parse --show-toplevel`): `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado`
- Repositorio (VERIFICADO, `git remote -v`): `github.com/alvaradom1304/Altiora`
- Task: `task_3605bc9c96ab` · Dispatch: `ctx_72f05aa613b1`
- Terminal del worker (el de los comandos `--from` del brief): `term_02e57333-b7a0-42e7-9523-d8f98a76f5ea`. Terminal del coordinador: `term_09a5e197-4615-4d8e-b414-339f7b105a9c`. Nota: el encabezado del brief no lista el handle del worker; se tomó el de `--from`.
- `modelo_planeado`: Sonnet 5.5 (`claude-sonnet-5-5`), según el entorno de la sesión; es solo plan.
- `modelo_efectivo`: `null` · `estado_modelo: no_observado` · `procedencia_modelo: null` (sin recibo Orca del proceso exacto).

## 1. `MCP_TIMEOUT` en el proceso hijo

- Comando: `node -e "console.log('MCP_TIMEOUT=' + process.env.MCP_TIMEOUT)"`
- Salida literal: `MCP_TIMEOUT=60000` · código de salida: `0`.
- VERIFICADO: la sesión fría heredó `MCP_TIMEOUT=60000` desde `env` de `.claude/settings.json`. No se imprimió ninguna otra variable.

## 2. Descubrimiento nativo de Graphify MCP

- Al arrancar, el cliente listó `graphify` como «still connecting» (no `CONNECT_TIMEOUT`, no apareció el mensaje de 30000 ms).
- Primer `ToolSearch select:mcp__graphify__graph_stats`: «No matching deferred tools… graphify still connecting». Segundo intento, poco después: herramienta descubierta y esquema cargado (`graph_stats`; además `get_community`, `get_neighbors`, `get_node`, `get_pr_impact`, `god_nodes`, `list_prs`, `query_graph`, `shortest_path`, `triage_prs`).
- No apareció diálogo de autorización MCP; no se autorizó ni cambió nada.
- Tiempo de conexión: no medido con reloj. Solo se observa que tras el arranque tardó más que el primer intento de descubrimiento y menos que el segundo, sin error de timeout. No se registran segundos.

## 3. Única llamada nativa a `mcp__graphify__graph_stats`

- Una sola invocación, sin argumentos, desde el cliente nativo. Salida literal:

```
Nodes: 21510
Edges: 24557
Communities: 792
EXTRACTED: 99%
INFERRED: 1%
AMBIGUOUS: 0%
Built at commit: e438b3a684fdb578307edd00bbaa39e67a52d62e
```

- Coincide con el registro previo (21.510 nodos / 24.557 aristas). El commit del grafo `e438b3a` coincide con el HEAD reciente indicado al inicio de la sesión.
- Tiempo de la llamada: no cronometrado; la respuesta volvió dentro del turno sin error ni reintento.
- No se ejecutaron handshakes stdio aislados, `npm run check` ni `coordinator:test`.

## Conclusión (limitada)

Con `MCP_TIMEOUT=60000` en `env` del proyecto, esta sesión fría conectó `graphify` sin `CONNECT_TIMEOUT` y `graph_stats` respondió por el cliente nativo. Esto responde al pendiente 1 y 2 de `GRAPHIFY-ESTABILIDAD-20261110.md` para esta única sesión.

## Límites

- Una sola sesión y una sola observación; no demuestra ausencia de timeouts futuros bajo otra carga ni que 60 s baste siempre. No hay tiempos medidos del arranque.
- No se aísla causalmente que el cambio de timeout sea lo que permitió conectar (no hay grupo de control en esta sesión).
- Conexión de otras IAs: no verificada.
- Estado `implementado-pendiente-QA`: requiere revisión independiente.
