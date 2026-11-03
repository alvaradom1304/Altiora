# ALT-TRIAD-001 · Brief (Claude Code) — ejercicio FICTICIO
Autor: Claude Code 2.1.317 (Sonnet 5.5) · 2026-11-03 · rama altiora-enterprise-os · commit: pendiente

> Cliente y datos inventados para la prueba. No es un proyecto real ni una oferta.

## Encargo
Landing de una tienda ficticia de plantas de interior ("Verdía") que vende por pedido en línea.

## Éxito (medible en la prueba, no en negocio)
1. Una sola acción principal visible sin scroll: "Pedir mi planta".
2. Secciones: héroe, 3 plantas destacadas con precio ficticio, cuidado en 3 pasos, preguntas frecuentes, pedido.
3. Contenido legible sin JS ni animación (DOM completo, movimiento reducido, móvil 360 px).
4. Contraste AA y foco visible descritos en el esquema visual.

## Riesgos
- Inventar precios o testimonios → todo marcado FICTICIO.
- Que el esquema visual dependa de 3D → prohibido; solo estructura y jerarquía.
- Solape de archivos entre IAs → un escritor por archivo.

## Reparto (un escritor por archivo)
| Archivo | Escritor | Estado |
|---|---|---|
| tests/triad/ALT-TRIAD-001-brief.md | Claude Code | HECHO |
| tests/triad/ALT-TRIAD-001-ui.md | Antigravity | NOT_TESTED |
| tests/triad/ALT-TRIAD-001-qa.md | Codex | NOT_TESTED |
