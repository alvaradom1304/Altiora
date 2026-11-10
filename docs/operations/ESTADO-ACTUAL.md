# Estado operativo actual de Altiora

Verificación: 2026-11-10. Esta es la entrada vigente; los informes anteriores conservan el historial.

## Elegir la raíz correcta

- Empresa Altiora: `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado`, remoto `alvaradom1304/Altiora`.
- Carpeta de entrada confirmada por el usuario: `C:/Users/Usuario/OneDrive/Desktop/altiora`, remoto `alvaradom1304/la-central-del-queso`. Contiene contexto histórico de empresa y web cliente: comprobar siempre raíz, rama y remoto antes de escribir o publicar.

No se movieron archivos de cliente ni se cambiaron remotos, ramas o conversaciones. Cada raíz usa su propia configuración y registro de propiedad; las sesiones abiertas deben releer AGENTS y el contrato local de reporte.

## Preferencia de cuota vigente

Por instrucción del usuario al cerrar esta tarea: Claude como primera opción, Antigravity para su especialidad o respaldo; Codex reservado hasta indicación expresa. Sus transportes worker y QA externo quedan pausados por cuota, conservando las pruebas técnicas anteriores. Una pausa no equivale a avería. Mantener revisor independiente y no autoaprobar cuando falte un segundo revisor.

## Organización (2026-11-10)

Entrada única de navegación: [MAPA-ALTIORA](MAPA-ALTIORA.md) (raíces empresa/cliente, cuatro áreas, guía de encargo y traspaso). Informe: [ORGANIZACION-ALTIORA-20261110](ORGANIZACION-ALTIORA-20261110.md). QA independiente de esta organización: **PASS 6/6, alcance limitado** ([informe del revisor Antigravity](ORGANIZACION-ALTIORA-QA-20261110.md); run `run_6cf90154847a`, dispatch `ctx_774871cc073a`, succeeded/settled). Graphify MCP: ajustado `MCP_TIMEOUT=60000` (60 s) en `.claude/settings.json` ([ajuste](GRAPHIFY-ESTABILIDAD-20261110.md)) y validado en frío en sesión nueva de Claude (`ctx_72f05aa613b1`, [prueba en frío](GRAPHIFY-ARRANQUE-FRIO-20261110.md)) con `MCP_TIMEOUT=60000`, descubrimiento nativo y llamada `mcp__graphify__graph_stats` exitosa (21.510 nodos / 24.557 aristas); QA independiente **PASS** ([informe QA](GRAPHIFY-ESTABILIDAD-QA-20261110.md)), con límite de una sola observación sin tiempo de conexión medido ni atribución causal al timeout y cobertura del grafo parcial (solo código). Todo el trabajo sigue local sin commit; Codex continúa pausado por cuota.

## Uso

Pide el encargo con proyecto y resultado. Se aplican skills pertinentes, router por dominio, propiedad de archivos y QA independiente. Desde la raíz elegida: `npm run altiora:ready`. El coordinador Orca debe ejecutar además `node scripts/orca-coordinator.mjs preflight` desde su propia sesión antes de delegar. Un diagnóstico LISTO no acredita retorno, cuota ni autenticación futura.

Claude y Antigravity quedan como opciones de trabajo; Codex se pausa por la preferencia de cuota anterior. Las tres IAs conservan pruebas técnicas del mismo host. Pruebas nativas con retorno realizadas desde la carpeta de entrada:

| IA | Evidencia |
| --- | --- |
| Claude | `ctx_242e7b2d505a`, `worker_done msg_e292cbe5f6c4`; encargo real posterior `ctx_cf396c1385bc` succeeded/settled, revisado por Codex |
| Antigravity | `ctx_75f89804a7bf`, `worker_done msg_2b423889a14f`, `ALTIORA_AGY_SYNC_OK` |
| Codex | `ctx_105a19a1e59a`, `worker_done msg_954bd261dd12`, `ALTIORA_CODEX_RETURN_OK`, succeeded/settled |

Codex necesitó recuperar la entrega al MISMO dispatch mediante `orchestration send msg_7fe105a29e42`; ready/input_accepted inicial no inició turno. No se duplicó el worker. No se garantiza que cualquier lanzamiento futuro inicie solo: conservar IDs y comprobar retorno. Pruebas posteriores desde empresa: Claude `ctx_8642b462f020`, Codex `ctx_82cc43611140` y Antigravity `ctx_abd6d59d622f`, todos succeeded/settled. Antigravity tuvo timeout inicial `ctx_aac501bf6ca8`; un envío al terminal existente creó automáticamente un follow-up con nueva Task/Dispatch, conservando el fallo original. Claude registró una escalación de correo de seguimiento que no invalida su retorno original ni prueba ese seguimiento. Ver `EMPRESA-ORCA-20261110.md` en empresa. Cada nuevo coordinador requiere preflight propio. El implementador nunca se autoaprueba.

Modelo planeado y efectivo se separan en [AI-REPORT-CONTRACT.md](AI-REPORT-CONTRACT.md). El recibo real Codex expuso modelo/esfuerzo null; no se atribuye modelo desde la interfaz. Las tres IAs leen fuentes locales vigentes por encargo; no existe un sincronizador automático de GitHub ni de chats antiguos.

## Comprobado

- Carpeta de entrada: 51/51 pruebas + TypeScript PASS. Readiness antes de la pausa por cuota: true, cero claims, tres workers elegibles, ambos endpoints locales HTTP 200. Tras la pausa, Codex deja de ser elegible por decisión del usuario.
- Empresa: `npm run check` original PASS. Runtime genérico propio incorporado, sin copiar clientes, registros ni secretos; 51/51 pruebas del runtime PASS, hashes de seis archivos genéricos idénticos a fuentes revisadas, política equivalente salvo raíz y nota de procedencia; controles propios en [ORQUESTADOR-LOCAL.md](ORQUESTADOR-LOCAL.md) cuando se lea desde empresa.
- OmniRoute: servicios locales 20128/20129, inferencia sin herramientas con clave local ya autorizada. Pruebas previas HTTP 200 y `ALTIORA_RUNTIME_OK`; prueba posterior desde empresa HTTP 200, reported_model `gpt-6-luna-low` y `ALTIORA_RUNTIME_OK`. Readiness no prueba cuota futura.
- Arranque frío PASS (81 s); un proceso por servicio. Inicio HKCU configurado. Login real de Windows: NOT_RUN; no se cerró sesión ni reinició el equipo.
- Hook Graphify `hook-check`: retirado únicamente de la carpeta de entrada con autorización específica y respaldo. La implementación instalada es no-op (exit 0). Hook Orca conservado, SHA-256 `4B197D9264D1C38416E456BC5CAA2AF73B5C600EB2B4B5E60F4A0AE2E53419FE`. No se confiaron otros hooks. Los guards de seguridad de empresa se conservan.
- PR [#85](https://github.com/alvaradom1304/Altiora/pull/85): squash autorizado, merge `36187beabe3e53e464dbf79565e200d12efe8c1c`. Los demás PRs no se fusionaron. El checkout empresa no se reseteó ni actualizó mediante pull por sus cambios locales.
- WhatsApp cliente: fuentes locales centralizadas con el número oficial; TypeScript PASS. Ese ajuste no se recompiló ni desplegó. Build/QA anteriores no acreditan el número en un servidor que conserve el build previo.
- Gemini: sesión Google autorizada. Única clave activa del proyecto identificado comparada en memoria: NO coincide con el valor histórico. Sin mostrar/guardar valores ni revocar claves. La comparación no acredita la fecha o mecanismo de revocación histórica.

Límites: la web conserva seis avisos moderados de herramientas de desarrollo y 18 de lint del control anterior; producción auditada sin vulnerabilidades. No se inventaron ventas, oportunidades ni correos enviados. No se activaron conectores ajenos ni se cerraron otros PRs. Las pruebas son evidencia fechada, no garantía universal de que todo conector funciona.

Evidencias de transporte y arranque conservadas en `C:/Users/Usuario/OneDrive/Desktop/altiora/docs/operations` y su `out/operations`. Las rutas no se copian como si fueran pruebas de lanzamiento desde empresa. [Runtime propio](ORQUESTADOR-LOCAL.md) · [Contrato común](AI-REPORT-CONTRACT.md).

Revisión tras la reserva de cuota: Claude puede implementar y Antigravity revisar independientemente, o viceversa; Codex no se invoca automáticamente. Un revisor disponible no equivale a un veredicto emitido.
