# Propuesta de gobierno operativo — Altiora (2026-11-03)

**Estado:** PROPUESTA PARA REVISIÓN. No acredita instalaciones, sesiones simultáneas ni resultados comerciales. No cambia por sí sola `team/ROUTING.md` ni configuraciones locales.

## Autoridades
- **Propietario / dirección ejecutiva humana:** objetivos, presupuesto, clientes, contratación, autorizaciones de publicación, acceso y gasto. Toda decisión irreversible o de riesgo material requiere revisión.
- **Claude Code — Director Operativo de Ejecución (COO técnico):** recibe un brief aprobado, lee `AGENTS.md`, `team/ROUTING.md` y `continuity/checkpoint.json`; descompone, asigna, coordina hitos, administra dependencias, valida evidencias y eleva bloqueos. No es automáticamente el mejor ejecutor de cada dominio ni puede afirmar conexiones sin pruebas.
- **ChatGPT — Dirección de Estrategia y Consultoría:** discovery, diagnóstico empresarial, investigación y hipótesis, decisiones comerciales, KPIs, entrevistas y propuesta para revisión humana. Puede colaborar con Codex en repositorio; no tiene control automático de la PC.
- **Codex — Ingeniería / Auditoría Independiente:** arquitectura de código, backend, testing y revisión técnica. Un cambio propio requiere un revisor independiente, humano o IA distinta.
- **Antigravity — Director de Producción Visual Interactiva:** diseño/implementación UI, WebGL/3D, motion, navegación y pruebas visuales; seguir `creative/visual-studio/ROUTER.md`, manteniendo director audiovisual de Altiora como rol funcional (no confundirlo con el proveedor de IA).

## Mecanismo de reparto
1. Registrar proyecto, usuario que autoriza, alcance, inputs, assets permitidos, restricciones y criterio de aceptación.
2. Consultar `team/ROUTING.md`; asignar una sola IA escritora por archivo. Para encargos simples, la IA actual responde sin abrir equipo.
3. Crear ticket de trabajo: `job_id`, `owner`, `repo`, `branch`, `inputs`, `file_ownership`, `skills`, `acceptance`, `tool_access` y `risk`.
4. Ejecutar tareas independientes en ramas/worktrees separados solo cuando el usuario autorice lanzamientos y el entorno realmente permita coordinar.
5. Revisión independiente de outputs de cliente y `npm run check` cuando aplique. No publicar, fusionar, contactar, gastar ni modificar configuración local sin autorización apropiada.
6. Completar handoff con estado y evidencia: `status`, `artifacts`, `evidence`, `checks`, `limitations`, `next_actions`.

## Matriz de aceptación real — campaña de validación
| Área | Requisito para PASS | Estado al crear documento |
| --- | --- | --- |
| Coordinación Claude, Antigravity, Codex | 3 sesiones reales observadas, handoff compartido, archivos/commits distintos, comprobación independiente | NOT_TESTED |
| Blender desde Claude | Proceso autorizado ejecutado desde esa sesión, resultado revisado | NOT_TESTED |
| Blender desde Antigravity | Igual, con evidencia de esa sesión | NOT_TESTED |
| Blender desde Codex | Igual, con evidencia de esa sesión | NOT_TESTED |
| After Effects MCP por cliente | Cliente muestra y ejecuta `after_effects_preflight` del MCP local; permiso/sesión y salida registrados | NOT_TESTED |
| Render Adobe | Solo .aep confiable y aprobado, licencia y render comprobados; no necesario para comprobar preflight | NOT_TESTED |
| Resultado comercial | Baseline real, experimento autorizado, ventas/margen/costo/tiempo medidos y consentimiento del cliente | NOT_TESTED |

### Evidencia ya existente, sin extrapolar
- `docs/operations/BLENDER-LOCAL.md`: instalación y render conceptual de Blender documentados, no conexión desde cada IA.
- `docs/operations/NATIVE-RUNTIME-VALIDATION.md`: prueba CLI aislada de Codex y handlers en fixtures, no coordinación multi-IA.
- `creative/visual-studio/after-effects/MCP-SETUP.md`: instalador y protocolo; conexión local pendiente.
- `docs/altiora-business/pipeline.json`: sin clientes de pago confirmados en el estado revisado.

## Primera acción ejecutable, en la PC del dueño
1. Revisar cambios locales antes de sincronizar; `npm run capability:doctor -- --text`, `npm run routing:eval`, `npm run check`.
2. `npm run after-effects:setup` para obtener plan, **sin aplicar automáticamente**. Si instalación/licencia y cambios son aprobados: `npm run after-effects:setup -- --apply`.
3. Desde cada cliente local confirmar `/mcp` o su panel equivalente, listar herramientas reales, ejecutar preflight sin render.
4. Crear ticket ficticio no comercial para el handoff entre Claude/Antigravity/Codex y guardar pruebas.
5. Una vez operativas herramientas, entrevista y piloto comercial de El Tilichero con datos reales; nunca presentar imitaciones como originales.

**Regla:** una habilidad descrita, una prueba sintética y una conexión real son tres estados distintos. Ninguna IA anuncia «todo listo» hasta completar la matriz.
