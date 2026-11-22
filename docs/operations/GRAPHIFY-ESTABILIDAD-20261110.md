# Graphify MCP: ajuste de timeout de arranque (2026-11-10)

Estado: **implementado-pendiente-QA** (sin autoaprobación; QA independiente pendiente).

## Identidad del encargo

- Workspace (VERIFICADO, `git rev-parse --show-toplevel`): `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado`
- Repositorio (VERIFICADO, `git remote -v`): `github.com/alvaradom1304/Altiora`
- `modelo_planeado`: Sonnet 5.5 (`claude-sonnet-5-5`), según el entorno de la sesión; es solo plan.
- `modelo_efectivo`: `null` · `estado_modelo: no_observado` · `procedencia_modelo: null` (sin recibo Orca del proceso exacto).

## Evidencia de la opción y sus unidades

Fuente: binario local `C:/Users/Usuario/.local/bin/claude.exe` (Claude Code 2.1.322), inspeccionado con `grep -a` sobre el ejecutable. No hay documentación oficial consultada en línea.

- Función de resolución (cadena literal extraída del binario):
  `function sd(){let _=i.MCP_TIMEOUT;return _&&_>0?Math.min(_,2147483647):30000}`
  → variable `MCP_TIMEOUT`, **milisegundos**, por defecto **30000**, tope 2147483647.
- Uso: `MCP server "<nombre>" connection timed out after ${sd()}ms`. Es el mismo mensaje y valor (30000 ms) que dio Graphify en esta sesión.
- `MCP_TIMEOUT` figura en la lista de variables que el cliente reconoce desde `env` de la configuración (junto a `MCP_TOOL_TIMEOUT`, `MAX_MCP_OUTPUT_TOKENS`).
- Otra variable distinta, `MCP_CONNECT_TIMEOUT_MS` (defecto 5000 ms), existe en el binario. **No** se tocó: no hay evidencia de que gobierne este error y su semántica no se verificó.
- No se halló propiedad de timeout por servidor en `.mcp.json` (no verificado en esquema; se buscó solo en el binario). El ajuste va en `env`.
- La opción reside en `.claude/settings.json` del proyecto: no se tocó configuración global.

## Cambio aplicado

- Respaldo: `.altiora/backups/claude-settings.json.20261110-pre-mcp-timeout` (sha256 idéntico al original: `f3be4816…12dc`).
- Diff exacto (`diff -u`, respaldo → actual):

```diff
   "env": {
-    "SLASH_COMMAND_TOOL_CHAR_BUDGET": "210912"
+    "SLASH_COMMAND_TOOL_CHAR_BUDGET": "210912",
+    "MCP_TIMEOUT": "60000"
   },
```

- Preservado: `SLASH_COMMAND_TOOL_CHAR_BUDGET`, `hooks`, `enabledPlugins`. `.mcp.json` no se modificó (conserva los demás servidores y `GRAPHIFY_BACKEND=none`). JSON validado con `JSON.parse`.
- Reversión: copiar el respaldo sobre `.claude/settings.json`.
- Elección de 60000 ms: SUPUESTO razonable, basado en el arranque medido de 16,8 s–30 s con el grafo de 21.510 nodos (ver `ORGANIZACION-ALTIORA-20261110.md`). No se probó que 60 s baste bajo cualquier carga.

## Prueba de conexión: nativa vs handshake aislado

- **(a) Conexión nativa de la sesión Claude: NO conectada.** Al iniciar esta sesión el cliente informó `graphify (CONNECT_TIMEOUT): connection timed out after 30000ms` (el valor previo al cambio). `ToolSearch select:mcp__graphify__graph_stats` devolvió «No matching deferred tools». Por tanto `graph_stats` **no se ejecutó**: no hay salida real que registrar.
- **(b) Handshake JSON-RPC aislado por stdio: no ejecutado en este encargo.** La única referencia es la ya registrada: `initialize` manual tardó 16,8 s (`ORGANIZACION-ALTIORA-20261110.md`). Un handshake aislado no prueba la conexión del cliente.
- **Efecto del cambio:** `env` de `.claude/settings.json` se lee al arrancar el proceso. Esta sesión ya arrancó con 30 s, así que el cambio **no la afecta**. Es SUPUESTO (no probado) que `/mcp` → reconnect la reintente con el valor nuevo: lo seguro es abrir una sesión nueva en este proyecto. Si el cliente exige confianza del proyecto o recarga de configuración, no se verificó.

## Límites

- El ajuste solo amplía la espera; no acelera el arranque ni garantiza que conecte. Si el timeout sigue ocurriendo con 60 s, la causa es otra (carga de CPU, proceso colgado) y no se ha diagnosticado.
- No se probó el efecto del cambio: hace falta una sesión nueva y una llamada real a `mcp__graphify__graph_stats`.
- Conexión de otras IAs: no verificada. No se ejecutaron `npm run check` ni `coordinator:test`, ni commit/push.

## Pendiente para QA independiente

1. Abrir sesión nueva de Claude en este proyecto y confirmar que `graphify` conecta y que `mcp__graphify__graph_stats` responde (esperado: 21.510 nodos / 24.557 aristas, según el registro previo).
2. Confirmar que `MCP_TIMEOUT` en `env` del proyecto surte efecto (por ejemplo, un fallo ya no aparece a los 30000 ms).
