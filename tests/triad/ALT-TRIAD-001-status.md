# ALT-TRIAD-001 · Estado de conexiones (2026-11-03, comprobado en esta sesión)
| Herramienta | Estado | Evidencia |
|---|---|---|
| Claude Code | PASS | `claude --version` → 2.1.317; esta sesión ejecuta |
| Orca | PASS (runtime) | `orca --version` 1.4.247; `orca status`: appRunning, runtimeReachable, connected; `worktree list` y `terminal list` responden. Agentes lanzados: NOT_TESTED |
| Codex | PARCIAL | `codex --version` 0.166.0-alpha.5.1; `codex login status` → ChatGPT. Ejecución de un encargo: NOT_TESTED |
| Antigravity | PARCIAL | `agy` en PATH, versión 1.4.12 (IDE). Sesión/login y ejecución de encargo: NOT_TESTED |
| MCP altiora-shared / playwright / chrome-devtools | FAIL | CONNECT_TIMEOUT 30 s en esta sesión |
| MCP dak-* (BigQuery, CloudSQL, Firestore, GCS) | FAIL | sin credenciales ADC |
| Conectores claude.ai (Gmail, Slack, Notion, Vercel, Ahrefs, Figma, HubSpot) | NO USADOS | listados; autorización no probada |
