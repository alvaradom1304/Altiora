# Altiora OS — Operación OmniRoute y auditoría de componentes (2026-11-03)

## Estado y límites
- **OmniRoute local: NOT_TESTED**. Un repositorio o un puerto HTTP disponible no demuestra acceso a un proveedor de inferencia.
- **Frontend Design: NOT_TESTED**. Skill, plugin, conector MCP y servicio runtime son categorías distintas.
- **Orca de Altiora:** `scripts/orca-dispatch.py` y `team/ROUTING.md` son el mecanismo de reparto de trabajos; **OmniRoute** es un gateway de peticiones a modelos. No reemplazar uno por el otro.
- **PR #67, PR #68:** revisión abierta; no asumir cambios en main hasta que estén fusionados.
- Referencia oficial: https://github.com/cheaper-inference/OmniRoute. Configuración publicada: dashboard en http://localhost:20128 y API http://localhost:20128/v1. Comprobar versión del README antes de instalar.

## Diagnóstico seguro desde la PC
Desde la raíz del repositorio:
```bash
node scripts/omniroute-preflight.mjs --json
npm run capability:doctor -- --text
npm run skills:audit
npm run routing:eval
npm run check
```
El primer comando hace **solo GET locales**, sin autenticación, salvo que el propietario disponga explícitamente de `OMNIROUTE_API_KEY` en su entorno. La clave nunca debe imprimirse, subirse ni introducirse en issues. Si el endpoint de modelos responde, verificar que el contenido sea de OmniRoute y que haya al menos un proveedor habilitado y permitido.

**NO instalar desde fuentes no verificadas. NO habilitar acceso desde Internet a 127.0.0.1:20128. NO copiar la URL de endpoint que contiene claves en la ruta a repositorios.**

## Activación en etapas (Claude Code como COO)
1. **Detectar:** instalación, proceso, puerto, versión, cliente, arquitectura y estado de proveedores. Si falta, **BLOCKED_INSTALLATION**. Solicitar aprobación antes de instalar o activar un proveedor de pago.
2. **Configurar:** únicamente el cliente de prueba y en una rama/copia con respaldo; preferir URL local y autenticación por encabezado. No sustituir silenciosamente la configuración principal de Claude, Codex o Antigravity.
3. **Validar:** primero GET `/v1/models` autorizado, luego exactamente una solicitud de inferencia sencilla con un límite de costo previamente aprobado. Registrar modelo, proveedor, latencia, tokens de entrada/salida, errores y calidad; nunca contenido sensible o clave.
4. **Comparar:** misma tarea, rubric y presupuesto con ruta directa y con OmniRoute. Registrar calidad y costo observados. El gateway puede añadir latencia o costo; no prometer porcentaje fijo de ahorro.
5. **Prompts:** evaluar una transformación opcional que preserve intención, hechos, restricciones, accesibilidad, aspectos legales y criterios de aceptación. Comparar contra baseline; desactivarla si reduce calidad.
6. **FrontEnd Design y MCP:** inventariar configuración de Claude, Codex y Antigravity; validar invocación real de una operación segura (por ejemplo enumeración de herramientas), y hacer pruebas de componente visual en carpeta temporal aislada.
7. **Coordinar:** ejecutar ALT-TRIAD-001 de `docs/operations/SKILLS-DEDUP-TRIAD-2026-11-03.md` **solo si PR #68 se encuentra incorporado o se tiene la rama local**. Tres sesiones reales: Claude brief, Antigravity prototipo, Codex QA independiente. No simular sesiones.
8. **Entregar:** matriz de componentes con `NOT_INSTALLED`, `CONFIGURED_NOT_TESTED`, `INSTALLED_NOT_CONNECTED`, `VERIFIED_ACTIVE`, `FAILED`, `BLOCKED` y `NOT_TESTED`; incluir evidencia, fecha, entorno, versión y siguiente acción.

## Inventario mínimo de capacidades
| Componente | Estado sustentado ahora | Prueba pendiente |
|---|---|---|
| Claude Code / Codex / Antigravity | Reglas en repo | Sessions reales y handoff |
| OmniRoute | NOT_TESTED local | Puerto, proveedor, inferencia aprobada |
| Orca | Dispatcher en repo | CLI local y despacho real |
| Frontend Design | NOT_TESTED local | Enumeración de skill/plugin y ejecución visual |
| After Effects | Script de setup en repo | MCP preflight por cliente |
| Blender | Preflight implementado | Operación desde cada IA |
| Skills activas | Catálogo en repo | Validar dependencias, ejecutar QA y deduplicación segura |
| Plugins y conectores | Política de ahorro disponible | Estado conectado por cliente; conectar solo lo requerido |

## Prompt compacto para ejecutar en Claude
> Actúa como COO de Altiora. Lee `team/ROUTING.md`, `docs/operations/CONECTORES-Y-AHORRO.md` y este documento. Ejecuta los diagnósticos de solo lectura de OmniRoute, skills, Frontend Design, MCP y clientes IA. Verifica identidad/versiones y documenta estados con evidencia. Solicita autorización antes de instalar software, reconfigurar clientes, usar proveedores con consumo o abrir sesiones multiagente; una vez autorizado, sigue las fases de activación, benchmark y prueba ALT-TRIAD-001. Evita imprimir secretos y no anuncies como activo algo sin pruebas. Entrega informe verificable y PR con cambios reversibles.

## Seguridad
No encender conectores pesados permanentemente. No desplegar ni enviar campañas. No activar rutas con cuentas o claves obtenidas de terceros. Revisar políticas de proveedores antes de utilizarlos. Mantener sesiones cortas, contexto mínimo y revisión independiente.
