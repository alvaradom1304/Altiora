---
trigger: always_on
description: "Mantener sincronizados agentes, skills y reglas de Altiora entre Claude Code y Google Antigravity."
---

# Sincronización de Altiora
- Las fuentes originales son `team/agents.json`, `team/roles/` y `skills/`; nunca editar los archivos generados en `.claude/` y `.agents/` como fuente.
- Cuando cambien las fuentes, ejecutar `npm run agents:build` y `npm run check`. Cualquier diferencia debe corregirse antes de integrar a main.
- Leer AGENTS.md, GEMINI.md y el brief. Los roles son configuraciones; no equivalen a sesiones autónomas abiertas.
- Solicitar aprobación específica antes de gastar, publicar, contactar clientes, cambiar cuentas o permisos.
- Para cualquier migración, optimización, integración o escalamiento, aplicar la política canónica en docs/operations/ALTIORA-SCALE-ZERO-LOSS-V4.md: preservar primero, loops acotados, QA y Revenue Engine.
- No declarar «todo activo»: verificar cada conector en la sesión local y registrar estados distintos de configuración, conexión y pruebas.
