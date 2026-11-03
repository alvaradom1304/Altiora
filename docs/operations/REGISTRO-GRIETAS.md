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
| G-07 | P2 | OmniRoute: arranque por tarea no fiable (causa del 267014 indeterminada) | ABIERTA |
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
- **Solución:** guion maestro [ENTREVISTA-MAESTRA-TILICHERO-G1.md](../../projects/tilicheros/ENTREVISTA-MAESTRA-TILICHERO-G1.md) (consolida: [ENTREVISTA-DUENO.md](../../projects/tilicheros/ENTREVISTA-DUENO.md), fusionada en #61, + [ENTREVISTA-DISCOVERY-G1.md](../../projects/tilicheros/ENTREVISTA-DISCOVERY-G1.md)). Contacta el fundador; Claude no contacta.
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
- **Solución:** aplicar [PROTOCOLO-AUTENTICIDAD-AIRPODS.md](../../projects/tilicheros/PROTOCOLO-AUTENTICIDAD-AIRPODS.md) (documentos del proveedor + correspondencia de la unidad; el serial solo no basta); mientras tanto, no publicar piezas que nombren marca.
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

### G-07 · P2 · OmniRoute: el servidor funciona, pero el arranque por tarea no es fiable
- **Corrección (2026-11-03, tarde):** una versión anterior de este registro lo clasificó como «fallo de inicio por clave no persistente». La evidencia posterior lo desmiente en parte: ejecutado a mano con el script aprobado, OmniRoute **arrancó** (PID 6188, 13:16:42) y quedó solo en `127.0.0.1:20128` con `/api/health` 200, rutas administrativas y `/v1/models` sin credencial → 401, y la IP de la red sin respuesta. El aviso `STORAGE_ENCRYPTION_KEY is not set but a database already exists` es una advertencia, no detiene el servidor.
- **Defecto real del script:** el servidor tarda unos 70 s en estar listo; `omniroute-safe-start.ps1` solo espera a que aparezca la escucha y sondea de inmediato, así que informó un FAIL falso a los 51 s. Debería sondear `/api/health` hasta 120 s.
- **Resultado 267014 (`0x41306`, tarea terminada) tras el reinicio de las 12:52:** causa **indeterminada**. Hipótesis más probable, sin probar: el Programador mantiene la tarea «en ejecución» mientras viva el demonio hijo y, al cumplirse el límite de 5 min, termina el árbol y mata a OmniRoute. La hipótesis de la batería (la tarea tiene «detener si pasa a batería») no tiene respaldo: el registro de energía no muestra cambio de fuente en esa ventana.
- **Clave de cifrado:** no está en el `.env` del paquete ni en su respaldo (ambos con valor vacío), ni en variables de usuario o de máquina, y `~/.omniroute/.env` no existe. NO VERIFICADO dónde estuvo. La copia de respaldo de la base (abierta de solo lectura, sin leer valores) tiene **0 conexiones de proveedor**, `supporter_key_encrypted` vacío y las claves de `version_manager` vacías: ningún secreto de proveedor depende de esa clave. Lo único posiblemente afectado es 1 clave API local de pruebas, reemplazable.
- **Impacto:** ninguno para El Tilichero; sin proveedor no hay generación ni ahorro medible (NOT_MEASURED).
- **Solución pendiente de aprobación del fundador:** ver «Opciones para OmniRoute» en la sección 15.7 de la matriz. No se modificó ningún secreto, base de datos ni tarea.
- **Prueba de aceptación:** reinicio controlado con `-CheckOnly` PASS y `LastTaskResult` 0, con el proceso vivo más de 10 min.
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
