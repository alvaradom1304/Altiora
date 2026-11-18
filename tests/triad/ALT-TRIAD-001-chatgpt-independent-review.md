# ALT-TRIAD-001 — Revisión externa de ChatGPT (estática)
Fecha: 2026-11-03
Revisor: ChatGPT (GPT-6), distinto del modelo Claude Sonnet y del agente Antigravity.
Estado: **CONDITIONAL / NO APROBADO INTEGRALMENTE**.

## Alcance y evidencia
Leídos directamente desde la rama `claude/certificacion-operativa` los archivos:
- `tests/triad/ALT-TRIAD-001-brief.md`
- `tests/triad/ALT-TRIAD-001-ui.md` (lectura de sección inicial y especificaciones relevantes)
- `tests/triad/ALT-TRIAD-001-qa.md` (revisión anterior de Claude)
- `tests/triad/ALT-TRIAD-001-qa-request.md`

Es una evaluación documental independiente de proveedor, **no** una ejecución de Codex ni una prueba de navegador o accesibilidad automatizada. No ejecuté comandos, scripts, QA local, ni inspeccioné un render. No sustituye la validación funcional ni prueba que otros modelos tienen acceso a archivos locales.

## Hallazgos reproducibles por inspección
1. **P1 — Enlace de preselección inválido:** las fichas contienen `href="#pedido?planta=monstera"` (y variantes). La porción `?planta=...` forma parte del fragmento, no de la query; la ancla `id="pedido"` no coincide con `pedido?planta=monstera`. Sin JavaScript, la selección automática tampoco sucede. Corregir con `href="#pedido"` y selección manual o especificar una implementación funcional y accesible de preselección.
2. **P1 — WCAG 2.5.3 Label in Name:** el enlace muestra `Elegir esta planta`, pero sus `aria-label` actuales empiezan por `Elegir Monstera...` / `Elegir Sansevieria...`. El nombre accesible debe contener la etiqueta visible, preferiblemente al principio. Ej.: `aria-label="Elegir esta planta: Monstera Deliciosa"`.
3. **P1 — CTA visible sin scroll no demostrado:** el brief exige resultado a 360x640, pero el UI solo contiene estimación aritmética de altura sin página implementada. Estado **NOT_RUN** hasta crear maqueta y medir con Playwright, con fuentes cargadas y viewport 360×640.
4. **P2 — Consistencia de claims:** la especificación menciona garantía de adaptación, 24–48h y pago contra entrega, pero son ficticios. La marcación [FICTICIO] evita confundirlos en esta prueba; nunca trasladarlos a un cliente real sin validación.
5. **P2 — Política de propiedad de archivos:** la corrección posterior de Claude sobre `ui.md`, inicialmente propiedad de Antigravity, es una excepción que debe registrarse y aprobarse formalmente, o reenviar la corrección a Antigravity para restablecer la regla de un escritor.
6. **P2 — Contraste:** la revisión anterior declara 11/11 pares correctos, pero no ejecuté ni reproduje aquí el cálculo. Tratar ese resultado como evidencia del revisor anterior, no como una segunda comprobación matemática.
7. **P2 — Especificación vs producto:** los criterios de contenido/semántica se documentan, no hay evidencia de landing realmente construida; no confundir un esquema con una prueba de comportamiento.

## Veredicto por gate
| Gate | Resultado | Comentario |
|---|---|---|
| Revisor distinto de Claude | PASS (para esta revisión documental) | GPT-6, no Claude |
| Cumplimiento documental del brief | CONDITIONAL | Estructura presente, funcionalidad real ausente |
| Contrast ratios | NOT_RUN por este revisor | Resultado heredado de la revisión previa, no nueva prueba |
| CTA sin scroll móvil | NOT_RUN | Requiere prueba en navegador |
| Selector de planta | FAIL en especificación | Links con fragmentos inválidos |
| WCAG Label in Name | FAIL en especificación | aria-label no incluye etiqueta visible |
| Un escritor por archivo | CONDITIONAL | Excepción documentada, pendiente aprobación |
| Certificación triada final | **NO PASS** | Requiere correcciones + pruebas |

## Corrección y pruebas mínimas para cierre
1. Antigravity corrige o aprueba expresamente las especificaciones de enlaces y `aria-label`, dejando rastro de quién es el escritor autorizado.
2. Generar landing de prueba en aislamiento sin datos reales.
3. Ejecutar Playwright a 360×640: verificar CTA visible sin scroll, sin desbordamiento horizontal; navegación por teclado y semántica básica.
4. Ejecutar cálculo de contraste sobre colores realmente renderizados (incluyendo opacidad y estados) y una auditoría accesible.
5. Un revisor independiente inspecciona la **versión corregida** y publica su veredicto con fecha, versión, comandos y resultados.
6. No cerrar issue #65 como PASS antes de superar estos puntos.

Sin gastos, publicación, cambios en producción, credenciales, ni contactos con clientes.
