# Registro de grietas de Altiora OS

Corte: 2026-11-03 sobre `main` @ `17b9fb4` (fusión del PR #71). Lo mantiene el COO (Claude Code). Una grieta solo pasa a CERRADA con una prueba real citada; redactar la solución no basta. Para hallazgos de seguridad y cierres, ver también [ALTIORA-REAL-INTEGRATION-STATUS.md](ALTIORA-REAL-INTEGRATION-STATUS.md).

Severidad: **P0** seguridad, pérdida de datos o imposibilidad de prestar el servicio · **P1** defecto funcional, falta de QA o riesgo para un entregable · **P2** automatización o conector incompleto · **P3** mejora menor.
Estado: ABIERTA · BLOQUEADA (depende de permiso, dinero o dato externo) · CERRADA (con prueba).

**P0 abiertos: ninguno detectado.** No se afirma que no existan: solo que no se encontró evidencia en lo revisado.

## Resumen
| ID | Sev | Componente | Estado |
|---|---|---|---|
| G-01 | P1 | Revisión independiente (ALT-TRIAD-001) | BLOQUEADA |
| G-02 | P1 | El Tilichero · G1 | BLOQUEADA |
| G-03 | P1 | Ciclo G1–G8 con cliente real | BLOQUEADA |
| G-04 | P1 | El Tilichero · autenticidad del producto | BLOQUEADA |
| G-05 | P1 | Firewall: reglas Node.js en perfil Public | BLOQUEADA |
| G-06 | P2 | MCP de navegador y `altiora-shared` | ABIERTA |
| G-07 | P2 | OmniRoute: fallo de inicio tras reiniciar (clave no persistente) | ABIERTA |
| G-08 | P2 | Backlog de PRs abiertos | ABIERTA |
| G-09 | P2 | Archivo local sin versionar | ABIERTA |
| G-10 | P3 | `.pyc` versionados y rutas absolutas en `.mcp.json` | ABIERTA |
| G-11 | P3 | Headroom, Palacio Mental, Claude Red | ABIERTA (no bloquea) |
| G-12 | P3 | Tarea de arranque apuntaba a un worktree | CERRADA |

## Detalle
### G-01 · P1 · Revisión independiente de ALT-TRIAD-001
- **Evidencia:** `tests/triad/ALT-TRIAD-001-qa-rev2.md` (revisor Claude aislado, mismo modelo que el autor del brief); `…-chatgpt-independent-review.md` (estática, no ejecutó nada); Codex agotado hasta 2026-11-05 según `ALTIORA-REAL-INTEGRATION-STATUS.md` §12.2.
- **Impacto:** `team/ROUTING.md` exige revisión de otro modelo antes de entregar a un cliente. Sin ella no hay PASS global.
- **Causa raíz:** el único revisor de otro modelo con ejecución depende de créditos.
- **Solución:** relanzar el QA con Codex desde 2026-11-05 sobre la versión final (`tests/triad/ALT-TRIAD-001-qa-request.md`); si no, un humano o ChatGPT con ejecución.
- **Responsable:** Codex (QA técnico); decide el fundador.
- **Riesgo:** declarar PASS sin ejecución independiente.
- **Prueba de aceptación:** informe de un revisor distinto de Claude con pruebas ejecutadas sobre el commit final, y el issue #65 actualizado.
- **Estado:** BLOQUEADA. Triada: CONDITIONAL.

### G-02 · P1 · El Tilichero · G1 en HOLD
- **Evidencia:** `projects/tilicheros/FICHA-ENCAJE-G1.md`: sin problema cuantificado por el comprador, sin decisor identificado, sin presupuesto declarado.
- **Impacto:** no se puede proponer ni cobrar; cualquier cifra sería inventada.
- **Causa raíz:** no ha habido conversación con el responsable del negocio.
- **Solución:** entrevista con el dueño ([ENTREVISTA-DUENO.md](../../projects/tilicheros/ENTREVISTA-DUENO.md), fusionada en #61, + [ENTREVISTA-DISCOVERY-G1.md](../../projects/tilicheros/ENTREVISTA-DISCOVERY-G1.md)). Contacta el fundador; Claude no contacta.
- **Responsable:** fundador (conversación); `altiora-os-strategy` (diagnóstico posterior).
- **Riesgo:** presionar para cerrar sin datos.
- **Prueba de aceptación:** la ficha G1 con los tres campos llenos con cita textual y fecha.
- **Estado:** BLOQUEADA por información externa.

### G-03 · P1 · Ciclo G1–G8 nunca probado con un cliente
- **Evidencia:** `ALTIORA-REAL-INTEGRATION-STATUS.md` §12.7: Fase 7 NOT_RUN; cero clientes de pago.
- **Impacto:** el sistema de entrega es hipotético hasta completarse una vez.
- **Solución:** usar El Tilichero como primer ciclo real al pasar G1.
- **Responsable:** `altiora-project-director`.
- **Prueba de aceptación:** compuertas G1–G8 registradas con evidencia en un proyecto real.
- **Estado:** BLOQUEADA por G-02.

### G-04 · P1 · El Tilichero · autenticidad del producto
- **Evidencia:** `projects/tilicheros/ENTREVISTA-DUENO.md` §3 (PR #61): el audífono aparece como Airbuds, AirPods 3, AirPods Pro y réplica; hay 3 videos aprobados que dicen «AirPods». Sin verificar el serial no está demostrado que sean originales.
- **Impacto:** publicidad engañosa y riesgo de marca y legal para el cliente.
- **Causa raíz:** el material se aprobó antes de verificar el producto.
- **Solución:** pedir captura del serial en `checkcoverage.apple.com`; mientras tanto, no publicar piezas que nombren marca.
- **Responsable:** dueño del negocio (dato); `altiora-os-qa` (revisión de piezas).
- **Prueba de aceptación:** ficha de producto con verificación fechada, o piezas sin nombre de marca.
- **Estado:** BLOQUEADA por dato del cliente. NO VERIFICADO si el producto es original.

### G-05 · P1 · Firewall Node.js (perfil Public)
- **Evidencia:** hoy `Get-NetFirewallRule -DisplayName 'Node.js*'` → 2 reglas Public, Enabled=True. Respaldo en `C:\Users\Usuario\.altiora-backups\firewall-node-public-2026-11-03.json`.
- **Impacto:** cualquier servidor Node ligado a 0.0.0.0 sería alcanzable desde redes públicas. OmniRoute no se ve afectado (loopback).
- **Causa raíz:** reglas creadas por el instalador de Node.
- **Solución aprobada por el fundador, no aplicada:** en PowerShell **como administrador**, `Set-NetFirewallRule -Name '<Name de cada regla>' -Enabled False` (revertir con `-Enabled True`); comando exacto en la matriz §13.5.
- **Responsable:** fundador (sesión de administrador).
- **Riesgo:** bajo y reversible.
- **Prueba de aceptación:** `Get-NetFirewallRule` con Enabled=False y OmniRoute respondiendo en 127.0.0.1.
- **Estado:** BLOQUEADA por permisos de administrador.

### G-06 · P2 · MCP de navegador y `altiora-shared`
- **Evidencia:** en la sesión, `playwright`, `chrome-devtools`, `altiora-shared` y `dak-notebook` dieron CONNECT_TIMEOUT de 30 s. `claude mcp list` (2026-11-03) muestra `playwright`, `chrome-devtools` y los seis `dak-*` en *Pending approval*; los `dak-*` de nube además no tienen credenciales ADC. `altiora-shared` apunta a una carpeta del 2026-10-18.
- **Causa raíz:** aprobación pendiente en `claude` (decisión de configuración del fundador) más credenciales ausentes en los `dak-*`.
- **Impacto:** las pruebas de navegador no pueden hacerse por MCP en sesión. **Cubierto por alternativa:** Playwright CLI 1.64.1 (`npx playwright`) y `tests/triad/mockup/playwright-check.mjs` (15/15).
- **Solución:** aprobar solo playwright y chrome-devtools si hacen falta; no aprobar `dak-*`.
- **Prueba de aceptación:** `browser_navigate` desde una sesión nueva.
- **Estado:** ABIERTA, no bloquea el trabajo comercial.

### G-07 · P2 · OmniRoute no arranca tras reiniciar (fallo de inicio)
- **Evidencia (2026-11-03):** el equipo arrancó a las 12:52:09 y la tarea corrió a las 12:52:30 con `LastTaskResult` 267014 (`0x41306`, tarea terminada). `omniroute-safe-start.ps1 -CheckOnly` → `NO_RUNNING`. Ejecutado a mano, el script terminó en 51 s con FAIL y OmniRoute informó `STORAGE_ENCRYPTION_KEY is not set but a database already exists`. Los secretos del `.env` del paquete tienen valor vacío (solo se midió la longitud) y no hay variable de entorno de usuario ni de máquina.
- **Clasificación:** fallo de inicio por configuración; no es una detención normal. La causa del 267014 (p. ej. límite de 5 min si el demonio retiene la tubería) es HIPÓTESIS: no se puede probar hasta que arranque. El registro operativo del Programador de tareas está desactivado.
- **Causa raíz:** la instancia anterior usaba claves inyectadas en esa sesión; ninguna está en una ubicación persistente.
- **Impacto:** ninguno para El Tilichero; OmniRoute es optimización y no hay proveedor autorizado. Ahorro de tokens NOT_MEASURED.
- **Solución (credenciales: decide el fundador):** persistir la clave existente (el respaldo `~/.altiora-backups/omniroute-2026-11-03_pre-intervencion/` existe; NO VERIFICADO que contenga la clave) o aceptar una base nueva (hoy 0 proveedores). No se hizo ninguna. Luego repetir el reinicio controlado.
- **Prueba de aceptación:** tras un reinicio, `-CheckOnly` PASS y `LastTaskResult` 0 con escucha solo en 127.0.0.1.
- **Estado:** ABIERTA, no bloquea.

### G-08 · P2 · Backlog de PRs abiertos
- **Evidencia:** `gh pr list`: al menos 9 PRs abiertos (#57–#64, #67, #72), varios con CI verde y sin revisión. El #72 registra el estado posterior a la fusión.
- **Impacto:** divergencia entre ramas y dos fuentes de verdad.
- **Solución:** el fundador decide cuáles fusionar; no se fusiona ninguno sin autorización expresa.
- **Prueba de aceptación:** cada PR cerrado o fusionado con motivo.
- **Estado:** ABIERTA.

### G-09 · P2 · Archivo sin versionar en el checkout canónico
- **Evidencia:** `git status` de `altiora-unificado`: `scripts/test-omniroute.mjs` sin seguimiento (más `.agents/mcp_config.json`, `.altiora/catalog.local.json`, `.references/`).
- **Impacto:** si existe una prueba que solo vive en disco, se pierde con un `git clean`.
- **Solución:** revisar su contenido y decidir si se versiona o se descarta; no se borró ni movió nada.
- **Estado:** ABIERTA. NO VERIFICADO qué contiene.

### G-10 · P3 · Higiene
- Cuatro `.pyc` versionados aparecen modificados en cada ejecución (visto en `git status` de la rama `altiora-enterprise-os`). El `.gitignore` debería excluirlos.
- `.mcp.json` contiene rutas absolutas de usuario (matriz §4.6): no portable.

### G-11 · P3 · Headroom, Palacio Mental, Claude Red
- Headroom está solo REFERENCED; los otros dos sin identidad (matriz §3). Ninguno es necesario para entregar un proyecto. No bloquean el inicio comercial.

### G-12 · P3 · Tarea de arranque apuntaba a un worktree temporal — CERRADA
- **Evidencia:** hoy `omniroute-task-repoint.ps1` en modo simulacro: acción actual = acción nueva, ambas con `…\altiora-unificado\scripts\omniroute-safe-start.ps1`; los dos scripts existen en el checkout canónico, que está en `17b9fb4` sin retraso respecto de `origin/main`.
- **Prueba:** salida del simulacro (exit 0) y `Test-Path` verdadero. Cierra solo el apuntado de la ruta; el arranque tras reinicio falla por otra causa (G-07).
