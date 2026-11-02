# Piloto de `claude plugin eval` (NOT_RUN)

Casos para la herramienta oficial de Claude Code que compara con y sin skill (`--ablation with-without`) y comprueba la activación: `descubrimiento-b2b` debe activar `spin-selling`; `casi-anuncio-instagram` y `casi-feria-bajo-ticket` son casi aciertos que no deben activarla.

Estado: **NOT_RUN**, sin validar. El grader `casi-feria-bajo-ticket/graders/criterio.md` es de tipo regex y su esquema no está comprobado; si falla, sustituirlo por un grader de tipo llm. Ejecutar siempre con `--no-publish` (por defecto el informe se publica en claude.ai). Documentación: https://code.claude.com/docs/en/plugin-evals
