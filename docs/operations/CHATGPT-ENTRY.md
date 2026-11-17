# Entrada de ChatGPT a PREAMBRA / Altiora multi-IA

**ChatGPT también es un miembro informado del equipo**, no un actor que ignore la existencia de Codex, Claude Code, Antigravity y Orca. Esta es una instrucción de trabajo del repositorio; la sesión real de ChatGPT solo la observa si puede acceder al repo o si se le aporta este archivo. No altera instrucciones del producto ni concede acceso a Orca desde el móvil.

## Primer minuto
1. Identificar el objetivo empresarial y el caso de cliente; PREAMBRA es la marca, Altiora el núcleo técnico.
2. Leer `AGENTS.md`, `team/ROUTING.md` y `docs/operations/MULTI-AI-CAPABILITY-ROUTING.md`; para continuar un hito, consultar `continuity/checkpoint.json`.
3. Reconocer otras IAs disponibles **en el ecosistema**, pero no afirmar que son ejecutables o están autenticadas en esta conversación. Orca es transporte entre agentes, no inteligencia adicional. Usar conectores autorizados cuando estén presentes; de lo contrario preparar handoff verificable.
4. Seleccionar el esfuerzo mínimo suficiente para el trabajo actual; recomendar otro modelo/plataforma si aporta ventajas técnicas, sin atribuirle acceso ni cuota que no comprobó.
5. Elegir un solo responsable de ejecución, salvo división realmente independiente. ChatGPT hace consultoría, investigación y dirección; cuando tenga permisos de GitHub puede preparar PR y pruebas, no lanzar automáticamente CLIs del PC.
6. Cuando se necesite Orca local, preparar un encargo `job_id` y un plan reproducible. Nunca escribir `DONE` o `RUNNING` sobre un worker sin identificador real de tarea/terminal y evidencia.

## Contrato reutilizable de handoff

```json
{
  "job_id": "PMO-ORCA-001",
  "brand": "PREAMBRA",
  "technical_system": "Altiora",
  "objective": "Verificar routing de una tarea multi-IA con Orca sin lanzar agentes de forma involuntaria",
  "owner": "codex",
  "candidate_model": "segun la lista del ejecutor en el momento",
  "reasoning_effort": "medium",
  "transport": "orca-if-authorized",
  "tool_access": {"github": "VERIFY_IN_SESSION", "orca_desktop": "UNKNOWN", "claude_cli": "UNKNOWN", "antigravity": "UNKNOWN"},
  "owned_paths": [],
  "dependencies": [],
  "acceptance": ["routing JSON valido", "autorizacion exigida para dispatch", "CI aprobado"],
  "evidence": [],
  "status": "DESIGNED"
}
```

El encargo se traslada como JSON y enlaces de Git/PR, no como transcripción completa ni secreto de cuentas. Para ejecutarlo en una PC en la que Orca se haya probado: generar plan con `npm run orca:dispatch -- --router heuristic --json "encargo"` y **solo después**, con permiso expreso para ese lanzamiento, elegir el worker en Orca o habilitar el despacho; revisar tareas, outputs y CI.

## Guía para respuestas al director
En lugar de decir «no se puede» o fingir conexiones, responder «yo puedo hacer X ahora; para Y, usaría Z (modelo/esfuerzo y motivo), estado de acceso: desconocido hasta prueba». Priorizar primera venta y solución empresarial real sobre agregar más infraestructura.
