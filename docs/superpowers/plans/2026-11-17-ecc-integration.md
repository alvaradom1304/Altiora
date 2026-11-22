# ECC selective integration Implementation Plan

> For agentic workers: execute sequentially with verification; independent review before accepting. No automatic merge, external plugin install, observer, telemetry or service.

**Goal:** Make ECC adaptations inspectable and usable in Altiora/PREAMBRA without duplicating its library.
**Architecture:** Keep the PR81 secret guard, add a read-only integration doctor and worktree-scoped hook installer; extend existing review and learning skills through short references.
**Tech Stack:** Node.js 20+, Git, existing SkillSpector 2.12.0; no new packages.
**Spec:** User request 2026-11-17: compare ECC and add missing relevant capabilities. Source affaan-m/ECC pinned to 3f14a103a8694e51c1df9a806217a6d0b5f7a6f7.

## Global Constraints
- Preserve PREAMBRA, client separation, local edits, permissions and independent QA.
- Imported guidance must pass static SkillSpector and manual review; no external scripts copied or executed.
- Do not read transcripts, credentials or client assets; no background observers or automatic promotion of instructions.
- Keep the full ECC plugin uninstalled; map existing equivalents instead of creating duplicate agents.

## Review Focus
- A configured hooksPath with a missing file must not count as active protection.
- Custom hooks must not be overwritten; installation in one worktree must not redirect others.
- Configuration presence is distinct from functional verification.
- Lessons stay project-scoped, with evidence and counterexamples; never claim a numeric confidence without data.
- Verification reports distinguish failed, not run and not applicable; no secrets in outputs.

## Tasks
- [x] Add failing fixture tests for missing integration, custom hooks, linked worktree isolation and actual commit rejection.
- [x] Implement doctor/installer and a versioned adoption matrix; wire tests into existing check.
- [x] Extend review/learning references, record pinned source/license and run static scans.
- [x] Run generation, focused tests, full check and independent review; fix findings.
- [x] Prepare PR81 evidence and activate the reviewed local integration in the canonical enterprise checkout without overwriting other changes. Remote publication is verified separately in the PR.

## Economía del encargo

| Paso | IA/modelo planeado | Conectores | Contexto | Riesgo y verificación |
|---|---|---|---|---|
| Comparación | Codex de esta sesión; efectivo no observado | GitHub en lectura | seis capacidades pertinentes y fuentes locales | Pin/licencia y matriz |
| Implementación | misma sesión | ninguno adicional | archivos propios | pruebas de fixtures y check completo |
| Revisión | altiora-review independiente; efectivo no observado | ninguno adicional | delta acotado | hallazgos reproducibles y revalidación |

No se midieron tokens ni ahorro; no se cambió el modelo ni se conectaron servicios.
