# ALT-TRIAD-001 · Revision independiente (QA)

## Quien revisa
- Cliente: Claude Code, subagente `altiora-os-qa` (instancia Claude aislada, sesion nueva, sin contexto del brief ni de las correcciones).
- Modelo: Claude Sonnet 5.5, el mismo que escribio el brief (`ALT-TRIAD-001-brief.md`) y corrigio los ratios de `ui.md`.
- **Independencia: PARCIAL.** Sesion y contexto separados, pero mismo modelo y misma familia que el autor del brief y del corrector. No equivale a la revision de Codex. No sustituye una revision humana ni de otro proveedor.
- Fecha: 2026-11-03. Rama: `claude/certificacion-operativa`, worktree `wt-cert`.
- Alcance respetado: solo lectura salvo este archivo. Sin red, sin instalar, sin credenciales, sin navegador.

## Que ejecute (comandos y salida real)
1. `python tests/triad/contrast-check.py` -> 11 pares, los 11 `PASS`, exit=0. Reales: 13.94, 14.64, 8.21, 8.62, 7.36, 7.73, 11.13, 7.49, 7.86, 7.33, 12.36.
2. Recalculo independiente (script propio en `/tmp/c.py`, no reutiliza `lum()` del autor; umbral sRGB 0.04045 en vez de 0.03928; luminancias lineales impresas):

| Par | L(fg) / L(bg) | Ratio | Declarado en ui.md | Coincide |
|---|---|---|---|---|
| #FFFFFF / #1E5E3A | 1.0 / 0.08587 | 1.05/0.13587 = 7.728 | 7.73:1 | si |
| #2D5438 / #FFFFFF | 0.07184 / 1.0 | 1.05/0.12184 = 8.618 | 8.62:1 | si |
| #B00020 / #FFFFFF | 0.09334 / 1.0 | 1.05/0.14334 = 7.325 | 7.33:1 | si |
| #132E1B / #E3EFE4 | 0.02172 / 0.83665 | 12.363 | 12.36:1 | si |
| #0E5E35 / #F8FAF6 | 0.08356 / 0.94981 | 7.486 | 7.49:1 | si |

   Pares que el script no cubre, recalculados por mi: #7D9C86 / #FFFFFF = 3.012 (ui.md: 3.01, correcto); #D2DDD3 / #F8FAF6 = 1.331 (ui.md: 1.33, correcto); #FFFFFF / #F8FAF6 = 1.05 (correcto). Los 14 valores de la tabla de la seccion 2 coinciden con mi calculo.
   Verifique a mano el primer par: 1.05 / (0.08587 + 0.05) = 7.728.
3. `git diff e1d774f -- tests/triad/ALT-TRIAD-001-ui.md` -> 5 hunks: (a) nota de revision insertada; (b) 13 filas de la tabla, solo la columna "Ratio calculado"; (c) texto de hover (7.6 -> 11.13); (d) texto de disabled (3.2 -> 3.01 y aclaracion de exencion 1.4.3); (e) texto de borde de input (7.3 -> 8.62) y fila 4 de la seccion 8 (rango 4.8-14.7 -> 7.36-14.64). Las columnas "Criterio WCAG AA" y "Veredicto" no cambian en ninguna fila; ningun color HEX cambia.
4. `git log --name-only --format='%h|%an|%s' -- tests/triad` -> commits `4090e64`, `cf59a1f` (ambos tocan ui.md, qa-request, report, status/brief/contrast-check) y `6436709`, `e1d774f`, `3c8efc2`. Todos con autor git "Altiora"; el autor git no distingue entre IAs.
5. Lectura completa de brief.md, ui.md, qa-request.md y contrast-check.py.

## Resultado por verificacion

### V1 Cumplimiento del brief: PASS
- Evidencia: criterio 1 (CTA "Pedir mi planta" en `#cta-principal`, hero), 2 (secciones 1-5: heroe, 3 plantas con precio marcado `[PRECIO FICTICIO]`, 3 pasos, FAQ, pedido), 3 (`<details>`, `<form>` nativo, bloque `prefers-reduced-motion`, 360 px), 4 (tokens + foco 3px). Sin 3D (el unico "WebGL/Canvas" es la afirmacion "0"). Sin datos reales identificables; telefono y nombre de placeholder son de ejemplo.
- Limite: es un esquema textual, no una pagina construida; "cumplido" significa "especificado".
- Hallazgo menor F5: la seccion 8 enumera 5 "criterios del brief", pero el brief tiene 4 criterios mas una lista de riesgos. Cosmetico.

### V2 Contraste y no-alteracion de veredictos: PASS
- Los 11 pares del script y los 3 pares extra pasan AA/3:1. Los numeros vigentes en ui.md coinciden con la columna `real` y con mi calculo independiente (error <= 0.005).
- El diff confirma que solo cambian cifras y la nota; los veredictos no cambian. La nota de revision es honesta (declara que la correccion no es aprobacion).
- Observacion (F1, bajo): la nota dice "9 de 11 inexactos"; el criterio del script es |real - declarado| > 0.3. Los otros dos tambien cambiaron (13.8->13.94, 14.7->14.64) por redondeo; consistente con la nota.
- Observacion (F2, bajo): `contrast-check.py` conserva en el codigo los valores ORIGINALES como "declarado", por lo que hoy el script marca "(declarado inexacto)" para filas que ya estan corregidas en ui.md. Es confuso para quien lo ejecute despues. No compara contra el ui.md vigente; el cotejo "ui.md == real" es manual (hecho aqui). Sugerencia: leer los ratios del propio ui.md.
- Observacion (F3, bajo): el script usa el umbral 0.03928 (WCAG 2.0 literal); el actual es 0.04045. Resultados identicos al redondear a 2 decimales en estos pares.
- Sin cubrir en ui.md: contraste del texto del enlace `.btn-card-select`, del color de placeholder y de `#0E331B` (estado active); no hay valores declarados, por tanto no se pueden certificar (F4, medio, ver V5).

### V3 Medida "sin scroll en 360x640": NOT_RUN
- No se maqueto ni se midio en navegador (sin navegador disponible: MCP playwright y chrome-devtools no conectan en esta sesion; ademas esta fuera de alcance).
- Lo observado en el texto: la suma 32 + 96 + 60 + 52 + 64 = 304 px es aritmeticamente correcta, pero es una estimacion. Inferencia (no medida): H1 de 51 caracteres a 32 px bold en 328 px de ancho probablemente ocupe 3 lineas (~115 px, no 96); subtitulo y alturas del CTA son estimadas (52 aqui, `min-height` 48 y 50 en otras secciones: inconsistente). Aun con +50 px de desviacion, hay holgura frente a ~580 px; la conclusion probablemente se sostiene, pero NO esta verificada. El "580 px visibles" tambien es un supuesto sobre la chrome del navegador.

### V4 Solape de rutas / un escritor por archivo: CONDITIONAL
- Observado: el brief, ui.md y qa.md tienen escritores distintos en el reparto. Pero en git, `ui.md` fue modificado en `4090e64` y `cf59a1f` (autor "Altiora", mismo para todos), ademas de `e1d774f` (Antigravity). Es decir, ui.md tuvo al menos dos escritores; la correccion de ratios la hizo Claude Code. Esta documentado en la nota de revision, por lo que no es oculto, pero incumple literalmente la regla "un escritor por archivo".
- Ningun commit de esta rama mezcla qa.md; este archivo es el unico escritor de qa.md.
- No se puede acreditar por git quien escribio cada archivo (autor git unico). La atribucion descansa en las cabeceras de los documentos y en el mensaje de commit.
- Nota: `e1d774f` vive en las ramas `tests/triad/ui` y `tests/triad/qa`; no verifique si esta en la ancestria de la rama actual (el diff funciona porque el objeto existe).

### V5 Claridad (puede construir un desarrollador solo con ui.md?): CONDITIONAL
Si en estructura, textos, HTML y estados; ambiguedades reales:
1. (medio) Enlaces `href="#pedido?planta=monstera"`: una consulta tras un fragmento no se interpreta como parametro; no preselecciona el `<select>` y puede no hacer scroll. Sin JS no hay forma documentada de preseleccionar.
2. (medio) `aria-label` de "Elegir esta planta" no contiene el texto visible ("Elegir Monstera..." no incluye "Elegir esta planta"): riesgo frente a WCAG 2.5.3 (Label in Name). Ademas el ficus se llama "Ficus Lyrata Compacto" en pantalla y "Ficus Lyrata" en el aria-label.
3. (medio) Contraste no especificado para: texto y estados del enlace `.btn-card-select`, color de placeholder, texto de `.faq-question`/`.faq-answer`, y fondo `#F0F6F1` (hover FAQ). Para un criterio 4 declarado "cumplido", faltan esos pares.
4. (bajo) Alturas del CTA inconsistentes: 48 px (min-height seccion 5), 50 px (seccion 7), 52 px (calculo del heroe).
5. (bajo) Hover de inputs: "aumento de grosor perceptible o contraste" es una alternativa, no una especificacion.
6. (bajo) Mensajes de error: `role="alert"` y `aria-describedby` requieren JS o validacion servidora; sin JS solo hay validacion nativa del navegador. No esta definido el comportamiento sin JS tras un POST fallido.
7. (bajo) Estado disabled: `opacity: 0.75` sobre `#7D9C86` reduce aun mas el contraste real (el 3.01:1 se calculo sin opacidad); esta exento de 1.4.3 pero el numero declarado no refleja el render.
8. (bajo) `body { overflow-x: hidden }` puede ocultar desbordes en lugar de evitarlos; no hay breakpoint concreto para pasar de 1 a 3 columnas.
9. (bajo) La FAQ menciona "Calathea" como alternativa que no existe en el catalogo; y "pago contra entrega" en un ejercicio no transaccional (todo marcado FICTICIO, sin impacto).
10. (bajo) Metadatos de ui.md: el campo "Commit" es un mensaje, no un hash; "Gemini 3.8 Flash High" y la sesion no son verificables desde el repo.

## Resumen de veredictos
| Verificacion | Veredicto |
|---|---|
| V1 Cumplimiento del brief | PASS |
| V2 Contraste y veredictos intactos | PASS |
| V3 Sin scroll 360x640 | NOT_RUN |
| V4 Un escritor por archivo | CONDITIONAL |
| V5 Claridad / construibilidad | CONDITIONAL |

## Limites
- No declaro la triada aprobada globalmente. Independencia PARCIAL (mismo modelo que el autor del brief). No se uso navegador ni se construyo la pagina. La aprobacion del issue #65 corresponde al fundador/coordinador, idealmente tras una revision con otro modelo o humana y la medicion en navegador de V3.
- Para pasar V4 a PASS: aceptar formalmente la correccion de Claude como excepcion documentada, o devolver la correccion a Antigravity.
- Para pasar V5 a PASS: resolver al menos los items 1-3.
- Archivos tocados: solo este (`tests/triad/ALT-TRIAD-001-qa.md`). Commit: ninguno (no autorizado).
