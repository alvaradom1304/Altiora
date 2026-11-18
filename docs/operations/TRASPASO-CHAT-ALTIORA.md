# Traspaso del chat «Altiora» (Claude Code) a otra IA

Fecha: 2026-11-01. Pegar el bloque siguiente como primer mensaje en Antigravity o Codex. Nota: Antigravity tenía la cuota individual agotada hasta unas 80 h después del 2026-11-01; si sigue sin cuota, usar Codex.

```text
Continúas el trabajo de Altiora que llevaba Claude Code en el chat «Altiora». Responde en español y separa lo verificado de lo supuesto.

Repositorio: github.com/alvaradom1304/Altiora. Copia de trabajo: C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado (rama altiora-unificado). Antes de nada: `git pull`, lee team/ROUTING.md (punto de entrada único: decide si lo haces tú, un subagente u otra IA, y fija el formato de entrega y la puerta de calidad) y AGENTS.md. No toques configuración global ni instales nada sin permiso del dueño.

Estado verificado:
- main contiene la unificación (PR #43 fusionado, commit fc1c56e): núcleo de skills, agentes fusionados (21), skills de ventas, ROUTING, economía de razonamiento en Orca, Tilicheros (projects/tilicheros/SISTEMA_CAPTACION_2026-11-01.md) y system prompt del Orquestador (docs/operations/orquestador-system-prompt-2026-11-01.md).
- Graphify: CLI graphifyy 0.9.100 instalado en C:/Users/Usuario/.altiora-tools/graphify; skill propia en skills/graphify/SKILL.md (en main desde el PR #45, commit 1cd2400; ROUTING §1 indica consultarlo). REGLA: ejecutar siempre con GRAPHIFY_BACKEND=none (sin ella usa `claude -p` en silencio). Revisión: docs/security/reviews/graphify-2026-11-01.md.

Pendiente, en este orden:
1. Triage de 12 PRs abiertos (#1, #6, #8, #9, #11–#18). Recomendación de la revisión: cerrar #17, #16, #15 (cubiertos por #18), #13 y #12 (router paralelo a ROUTING), #9 (Tilicheros superado), #6 (Altiora OS ya en main) y #1 (economía de IA ya en main). Decisión del dueño: #14 (motor de variación) y #18 (dividirlo; build-codex para generar .codex/agents de los 21 roles). Rebasar y revisar: #11 (llevar el endurecimiento a scripts/skill-security-gate.mjs) y #8 (regenerar INDEX.md, .claude/ y quality/). NO cerrar ni fusionar nada sin la aprobación expresa del dueño.
2. HECHO (2026-11-01): grafo regenerado con .graphifyignore y GRAPHIFY_BACKEND=none desde el commit 31435a1 (21.281 nodos, 24.105 relaciones, 780 comunidades «Community N», coste 0 tokens). Tras cambios de código, regenerar siempre con la ruta explícita del repo, no con `graphify update .`, que escanea la carpeta desde la que se ejecuta (el 02/11 el grafo quedó construido desde el clon de la-central-del-queso): `GRAPHIFY_BACKEND=none C:/Users/Usuario/.altiora-tools/graphify/Scripts/graphify extract C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado --code-only --out C:/Users/Usuario/.altiora-tools/graphs/altiora` y después `GRAPHIFY_BACKEND=none C:/Users/Usuario/.altiora-tools/graphify/Scripts/graphify cluster-only C:/Users/Usuario/.altiora-tools/graphs/altiora --no-label`. Comprobar en `GRAPH_REPORT.md` que el commit de origen coincide con `main` (regenerado así el 2026-11-10 desde e438b3a).
3. HECHO: PR #45 fusionado en main (Graphify).
4. Tilicheros: espera datos del negocio (SKU, precio, stock, responsable de WhatsApp); no inventar.

Reglas: tras cambiar skills, agentes o documentos, ejecutar `npm run agents:build` y `npm run check` (tarda ~10 min). Skills externas solo por el gate (docs/security/third-party-skill-gate.md; SkillSpector en C:/Users/Usuario/.altiora-tools/skillspector). No publicar, enviar mensajes ni gastar sin aprobación. Entregar con el formato de ROUTING §5: Resultado, Evidencia, Verificado/supuesto, Pendiente y bloqueos, Siguiente paso.
```
