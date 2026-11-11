# Contrato común de reporte IA · Altiora

Aplicar a Codex, Claude y Antigravity. Leer esta fuente local vigente al iniciar cada encargo y antes de informar resultados; prevalecen el encargo vigente y sus permisos. No se impone un JSON a la conversación: responder corto y natural. Usar campos estructurados solo cuando un handoff o una herramienta los necesite.

## Modelo y evidencia

- `modelo_planeado`: preferencia solicitada por usuario/router/configuración; nunca equivale a ejecución. Haiku, Sonnet, Codex o Gemini en un plan no prueban el modelo usado.
- `modelo_efectivo`: `null` mientras no exista evidencia efectiva del proceso exacto. En ese caso, `estado_modelo: no_observado` y `procedencia_modelo: null`. No completar desde requested, plan, metadata, modelo del chat padre o selector/UI actual.
- Con evidencia efectiva, indicar `estado_modelo: observado` y su procedencia precisa: comando/recibo conservado, proceso o IDs del worker, ruta de campo y fecha cuando estén disponibles. Un recibo válido solo acredita el proceso que identifica; la UI del coordinador no prueba un subagente.
- El router acepta como efectivo únicamente `result.worker.startOptions.launch.effective.model` y `.effort` del recibo Orca verificado. `requested.model`, `agent.model`, `metadata.model`, campos superiores llamados model y planes quedan fuera. Si effective falta o es null, mantener no_observado; ante contradicción con el plan, informar ambos sin sustituir el efectivo.
- No inferir cuota, créditos, ahorro o consumo a partir de modelos, archivos, catálogo, instalación o un resultado aislado. Separar CLI instalado, transporte conectado y prueba funcional actual.

## Workspace e identidad

Informar `workspace` como raíz Git efectiva del encargo y `repositorio` como identidad saneada (host/propietario/repositorio, sin credenciales, query ni fragmentos) cuando resulte relevante o en handoffs. Comprobar raíz con `git rev-parse --show-toplevel`; comprobar origin localmente y sanearlo antes de mostrarlo. Si no se verificó, indicar desconocido: no inventar identidad a partir del nombre de carpeta.

La carpeta principal confirmada `C:/Users/Usuario/OneDrive/Desktop/altiora` conserva su condición de entrada del usuario; su identidad Git es `github.com/alvaradom1304/la-central-del-queso`. La copia canónica de empresa `C:/Users/Usuario/orca/workspaces/Altiora-Immersive-Web-Lab/altiora-unificado` corresponde a `github.com/alvaradom1304/Altiora`. Confirmar siempre en la sesión: un nombre de carpeta no cambia el repositorio. Para trabajo de empresa usar su checkout/worktree asignado, sin forzar la raíz cliente; no mover/copiar clientes, cambiar origin, pull/reset o publicar como efecto lateral.

## Contexto vivo y gates

Usar el `AGENTS.md` y este contrato de la raíz efectiva. Consultar `docs/operations/ESTADO-ACTUAL.md`, `.altiora/coordinator.json` y el adaptador de la IA solo si existen y corresponden al encargo; su ausencia no prueba una conexión ni autoriza copiar el contexto cliente a empresa. Ambas raíces contienen esta misma regla de reporte, referenciada por sus instrucciones locales. No tomar snapshots de otro chat como estado actual.

Conservar propiedad de archivos, permisos, ausencia de publicación/gasto implícitos, revisión independiente y prohibición de autoaprobación. No se instalan herramientas ni se activan agentes/servicios por leer este contrato. Una sesión ya abierta debe releer las fuentes: un archivo actualizado no demuestra recarga de su contexto.
