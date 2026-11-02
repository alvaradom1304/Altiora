# Verificación de conexiones entre IAs · 02/11/2026

Comprobación en vivo de lo que comparten Claude Code, Codex y Antigravity en esta PC. Un archivo de configuración no es una conexión: cada celda indica la prueba que la respalda.

## Qué se corrigió

1. **`altiora-shared` en Claude exponía carpetas equivocadas.** La entrada de `.mcp.json` (`npx @modelcontextprotocol/server-filesystem`, versión 2.x) tapaba la de usuario en `~/.claude.json`. Esa versión sustituye las carpetas configuradas por las *roots* que anuncia el cliente. En la prueba devolvió el repo `la-central-del-queso` y worktrees de otras sesiones, no `shared/`. Además apuntaba a la copia `2026-10-30`, 94 commits por detrás de `main`. **Arreglo:** se quitó la entrada del proyecto. Claude usa ahora la de usuario: `fixed-shared.mjs` sobre `shared/`, la misma definición que Codex (`~/.codex/config.toml`) y Antigravity (`~/.gemini/config/mcp_config.json`). `fixed-shared.mjs` ignora las *roots* del cliente.
2. **`altiora-graphify` no arrancaba.** El proceso terminaba a los 1,8 s con `ImportError: mcp not installed` (al paquete `graphifyy` 0.9.100 le falta el extra `[mcp]`). **Arreglo:** se retiró de `.mcp.json`. Graphify se usa por CLI, que funciona igual en las tres IAs y no requiere instalar nada.
3. **Grafo desactualizado.** El grafo estaba construido desde `31435a1a`, 28 commits por detrás de `main`. Se regeneró desde la copia canónica en `83853a4` con `GRAPHIFY_BACKEND=none graphify extract … --code-only` y luego `graphify cluster-only … --no-viz`. Resultado: 21.353 nodos, 24.193 aristas, 782 comunidades, 125 archivos reextraídos. `GRAPH_REPORT.md` indica `83853a4c`. El anterior, con su `graph.html`, quedó en `graphify-out.old-2026-11-02`.

## Matriz final

`ACTIVO` = probado en vivo · `CONFIGURADO_SIN_PROBAR` = presente, sin prueba en una sesión del cliente · `NOT_RUN` = no se ejecutó, con su motivo.

| Capa | Claude Code | Codex | Antigravity |
|---|---|---|---|
| Reglas | ACTIVO: `CLAUDE.md` cargado en la sesión | CONFIGURADO_SIN_PROBAR: `AGENTS.md` (remite a `team/ROUTING.md`) | CONFIGURADO_SIN_PROBAR: `GEMINI.md` (remite a `team/ROUTING.md`) |
| Agentes generados | ACTIVO: 32 en `.claude/agents`, visibles como subagentes; `build-agents --check` PASS | CONFIGURADO_SIN_PROBAR: 8 adaptadores en `.codex/agents` | CONFIGURADO_SIN_PROBAR: 22 subagentes en `.agents/agents`; `build-antigravity --check` PASS. `agy agents` solo lista agentes principales, así que no prueba nada sobre los subagentes |
| Skills | ACTIVO: skills del repo descubiertas en la sesión | CONFIGURADO_SIN_PROBAR: `.agents/skills` | CONFIGURADO_SIN_PROBAR: `.agents/skills` |
| `altiora-shared` | ACTIVO: `claude mcp get altiora-shared` → `Scope: User config`, `✔ Connected`, `fixed-shared.mjs` | Servidor ACTIVO (sonda: 14 herramientas, solo `shared/` aunque el cliente anuncie *roots*). `codex mcp list` → `enabled`. Sesión NOT_RUN: sin cuota hasta el 05/11 | Servidor ACTIVO (misma sonda). `agy mcp list` → `enabled`. Sesión NOT_RUN: gastaría créditos de Gemini |
| Graphify | ACTIVO por CLI (`graphify query`, salida 0) | Mismo CLI disponible por shell en esta PC | Mismo CLI disponible por shell en esta PC |
| `altiora-after-effects` | ACTIVO: `after_effects_preflight` respondió (`aerender` no instalado: `ENOENT`) | Configurado y desactivado a propósito (`enabled = false`) | No configurado. No aporta mientras After Effects no esté instalado |

## Cómo volver a comprobarlo

Desde la raíz del repo canónico:

```bash
claude mcp get altiora-shared   # Scope: User config · ✔ Connected · fixed-shared.mjs
codex mcp list                  # altiora-shared enabled
agy mcp list                    # altiora-shared enabled
GRAPHIFY_BACKEND=none C:/Users/Usuario/.altiora-tools/graphify/Scripts/graphify query "orca dispatch" --graph C:/Users/Usuario/.altiora-tools/graphs/altiora/graphify-out/graph.json
```

Dentro de una sesión de cualquier IA, la herramienta `list_allowed_directories` de `altiora-shared` debe devolver solo `…\altiora-connection\shared`. Si devuelve otras carpetas, alguna entrada de proyecto vuelve a tapar la de usuario.

## Pendiente fuera del repo

- **Usuario, Claude Desktop:** los presets `altiora` y `altiora2` abren `C:\Users\Usuario\OneDrive\Desktop\altiora`, que es el repo `alvaradom1304/la-central-del-queso`. Hay que apuntarlos a `C:\Users\Usuario\orca\workspaces\Altiora-Immersive-Web-Lab\altiora-unificado`.
- **Sin probar en sesión real:** Codex hasta que vuelva la cuota y Antigravity cuando se decida gastar créditos. La prueba es la misma llamada a `list_allowed_directories`.
- **Observado, fuera de este alcance:** en Claude, `chrome-devtools` y `playwright` (`npx …@latest`) superan el límite de 30 s al arrancar; los `dak-*` de Google Cloud necesitan `gcloud auth application-default login`.

## Anexo: MCP de navegador (02/11/2026)

`chrome-devtools` y `playwright` no llegaban a conectar en Claude en el límite de 30 s. Los servidores arrancan en 2–4 s, pero `npx …@latest` añadía entre 19 y 85 s en cada arranque, aunque el paquete estuviera en caché. Ahora se arrancan con `node` desde `C:/Users/Usuario/.altiora-tools/mcp-browser`, con versiones fijadas y lockfile: `chrome-devtools-mcp` 1.12.0 y `@playwright/mcp` 0.0.84, ambos con licencia Apache-2.0. Se instalaron con `--ignore-scripts` desde la caché. Sonda en vivo: `chrome-devtools` responde con 32 herramientas en 4,6 s y `playwright` con 25 herramientas en 1,9 s.

Para recrear la carpeta en otra PC: crear `package.json` con esas dos dependencias exactas y ejecutar `npm install --ignore-scripts --no-audit --no-fund`. Las actualizaciones de versión pasan por Visual Tech Scout, nunca por `@latest`.
