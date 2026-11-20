# Runtime local del orquestador · empresa Altiora



Raíz propia: `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado`, repo empresa `alvaradom1304/Altiora`. La entrada del usuario con nombre de carpeta altiora y repo cliente conserva su identidad independiente. No se trasladan clientes ni se cambia origin.



Fuentes locales vigentes: `AGENTS.md`, `docs/operations/AI-REPORT-CONTRACT.md`, `.altiora/coordinator.json` y scripts del orquestador en esta raíz. Se incorporaron únicamente los cuatro scripts genéricos ya revisados del runtime principal, con copia exacta, y política adaptada a la raíz empresa. El registro `.altiora/active-ownership.json` será propio: no se copió ni creó un registro cliente, secretos o `.env`. Los scripts npm previos, incluido `check`, permanecen intactos.



```powershell

npm run coordinator:test

npm run altiora:ready

# Desde la sesion coordinadora propia de empresa, antes de ejecutar un encargo:

node scripts/orca-coordinator.mjs preflight

```



Claude, Codex y Antigravity tienen pruebas de transporte fechadas 2026-11-10 en el mismo host, realizadas en la raíz cliente; los IDs y límites se conservan en la política. Eso no acredita un lanzamiento desde empresa. Antes de cualquier lanzamiento se requiere el preflight de la propia sesión empresa, raíz Git correcta y terminal propio conectado/escribible, además del encargo autorizado y su propiedad de archivos. `altiora:ready` es diagnóstico de configuración/registro/elegibilidad y HTTP loopback; no sustituye ese preflight, la inferencia ni la revisión independiente.



Los modelos siguen siendo preferencias hasta el recibo efectivo del proceso exacto según el contrato local. Se preserva el respaldo por dominio y la prohibición de autoaprobación. No se añaden lanzamientos, agentes, cron, servicios ni instalaciones. La inferencia explícita OmniRoute cuenta ahora con `scripts/omniroute-client.py` y `.altiora/omniroute.json` locales, copiados byte a byte desde las fuentes revisadas. El JSON se validó estrictamente con lista cerrada de claves y valores públicos esperados: solo configuración loopback, modelo preferido y referencia de credencial; ningún token. El cliente consulta la credencial autorizada del mismo usuario en memoria mediante SQLite de solo lectura, sin copiar bases, tokens o `.env`, crear claves o seguir redirects. Sintaxis Python comprobada con AST, sin ejecutar el cliente. Smoke real desde empresa: NOT_RUN por este implementador, a cargo del coordinador; la configuración disponible no acredita todavía esa inferencia. Las pruebas previas del transporte de inferencia usaron fixtures.



Validaciones ejecutadas en empresa: `npm run coordinator:test` **51/51 PASS**; `npm run altiora:ready` **exit 0 / LISTO**, raíz local correcta, registro ausente interpretado como cero claims (no creado), tres transportes elegibles y ambos endpoints HTTP 200. `npm run check` global y cualquier lanzamiento: NOT_RUN por esta implementación. Entrega pendiente de QA independiente.


## QA independiente del coordinador

Codex root verificó hashes de los seis archivos genéricos: copias exactas; comparó política completa, cuyas únicas diferencias son root y nota de procedencia. La primera aserción esperaba solo root y detectó también note; la inspección verificó que no hay otros cambios de política. Registro cliente no copiado. Readiness empresa repetido independientemente: LISTO, ambos HTTP 200, tres workers elegibles, cero claims. `npm run check` original de empresa terminó exit 0 / PASSED. Smoke real desde empresa: `python scripts/omniroute-client.py --smoke --timeout 60`, PASS HTTP 200, respuesta `ALTIORA_RUNTIME_OK`, reported_model `gpt-6-luna-low`. No se atribuye a workers el modelo de OmniRoute.
