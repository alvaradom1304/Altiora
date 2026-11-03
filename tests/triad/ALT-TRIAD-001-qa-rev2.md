# ALT-TRIAD-001 · Revisión independiente rev.2 (versión corregida)

## Identificación
- Revisor: Claude Code, subagente `altiora-os-qa`, instancia Claude aislada (Claude Sonnet 5.5). No escribió brief, UI, maqueta ni correcciones.
- **Independencia: PARCIAL.** Mismo modelo y familia que el autor de la maqueta y de la rev.2 de `ui.md`. No sustituye revisión humana ni de otro proveedor.
- Fecha: 2026-11-03. Rama `claude/certificacion-operativa`, worktree `wt-cert`. HEAD: `0d0df6f7eb0029821a5f3f7a83fa9a574f114b6e` ("maqueta aislada + Playwright 14/14, ...").
- Alcance: solo lectura salvo este archivo. Sin red, sin instalar, sin credenciales. Nota: `playwright-check.mjs` reescribe `mockup/playwright-result.json` (archivo versionado); lo restauré con `git checkout -- tests/triad/mockup/playwright-result.json`. Árbol de `tests/` sin cambios salvo este informe.
- Entorno: Chrome del sistema vía Playwright local (`%USERPROFILE%\.altiora-tools\mcp-browser`). Los MCP playwright y chrome-devtools de la sesión no conectaron; no se usaron.

## Comandos y salidas reales
1. `python tests/triad/contrast-check.py` → exit 0. 15 pares, todos PASS (13.94, 14.64, 8.21, 8.62, 7.36, 7.73, 11.13, 7.49, 7.86, 7.33, 12.36, 7.73, 7.73, 5.66, 13.36). Persiste la etiqueta "(declarado inexacto)" en filas ya corregidas en `ui.md` (el script conserva los valores originales; ver H8).
2. `node tests/triad/mockup/playwright-check.mjs` → exit 0, **14 PASS / 0 FAIL** (M1, M2, A1, A2, K1, K2, K3, P1, P2, F1, F2, C1, R1, R2). M1: CTA y=276.4, alto 56, borde inferior 332.4 de 640.
3. Inspección manual de `mockup/index.html` y `ui.md` (rev.2) + sondas propias (script en el scratchpad de la sesión, no en el repo) con Chrome real. Resultados abajo.

## Verificado a mano en index.html (OBSERVADO)
- Hrefs de fichas: `?planta=monstera#pedido`, `?planta=sansevieria#pedido`, `?planta=ficus#pedido`. Query antes del fragmento: válido. El hallazgo P1 de ChatGPT queda corregido.
- `aria-label` de las 3 fichas empieza por «Elegir esta planta» (texto visible exacto). WCAG 2.5.3 cumplido; nombre completo incluye planta y precio.
- Preselección: por URL (`?planta=ficus#pedido` → select = ficus; valor inválido → vacío) y por clic/Enter en ficha (valor + foco al select; `history.replaceState` actualiza la URL). Comprobado con clic: URL final `index.html?planta=ficus#pedido`, foco en `campo-planta`.
- Foco: anillo `outline 3px solid #0E5E35` + offset 3 en enlaces, botones, summary y controles. Primer Tab = `cta-principal`.
- Desbordamiento: 0 elementos fuera del viewport a 360 y a 320 px (sondas).
- Contraste adicional que no medía la suite: estado `:active` `#FFFFFF/#0E331B` = 13.93; borde de error `#B00020/#FFF` = 7.33; `#2D5438` sobre badge `#E3EFE4` = 7.28.

## Hallazgos (prioridad descendente)

**H1 · Medio · Sin JS el formulario hace POST a un endpoint inexistente y sin validación.** `<form method="POST" action="/api/pedido-ficticio" novalidate>`. Reproducción: Chrome con JS desactivado, 360×640, clic en «Confirmar mi pedido» con el formulario vacío → petición real `POST file:///C:/api/pedido-ficticio` (observado). `novalidate` desactiva la validación nativa, por lo que se envía un pedido vacío. En un servidor real sería 404 (el endpoint no existe, por diseño de la prueba). El criterio del brief «operable sin JS» se cumple para lectura y navegación, **no** para el envío. Además `ui.md` §4 especifica el `<form>` **sin** `novalidate` (0 apariciones en ui.md, 1 en la maqueta): maqueta y especificación divergen. Remedio mínimo: quitar `novalidate` y dejar que el JS lo añada (`form.noValidate = true`), o documentar que sin JS el envío no está soportado en la maqueta.

**H2 · Medio · `ui.md` rev.2 no coincide con la maqueta (deriva spec/implementación).** Observado por conteo y lectura:
- `ui.md` declara `<img src="/img/ficticio/...">` ×4 (héroe + 3 fichas); la maqueta usa un SVG inline en el héroe y ninguna imagen en las fichas.
- `ui.md` §4/§8 siguen diciendo «~304 px < 580 px»; medido: 332.4 px. No es incorrecto como cota, pero es la cifra estimada que el propio QA previo marcó NOT_RUN y rev.2 no la reemplazó por la medida.
- `ui.md` define estado Loading (`aria-busy`, «Enviando pedido...»), Disabled y `details[open] .faq-answer { animation:none }`; la maqueta no los implementa (0 apariciones). Foco de campos con `border-color:#1E5E3A` y estado `:invalid:not(:placeholder-shown)`: tampoco implementados.
- `ui.md` §8 sigue marcando «CUMPLIDO» los 5 criterios, lenguaje que choca con «Esto no aprueba la triada» de la nota rev.2. Cumplimiento = especificado, no certificado.
Efecto: la prueba 14/14 certifica la maqueta, no todo lo que describe `ui.md`.

**H3 · Bajo-Medio · La prueba de CTA 360×640 es robusta a fuentes en las condiciones razonables, pero no al texto ampliado.** El CSS usa `system-ui` (sin webfonts; `document.fonts.ready` es redundante). Sondas con mutación: Courier New forzado → borde inferior 414 px; `html{font-size:20px}` → 433.5 px; 320 px de ancho → 325 px; alturas de viewport 568 y 500 → 332.4 (invariante). Todas dentro de 640. Con raíz 32 px (texto al 200 %) → 892.8 px: el CTA queda fuera de la primera pantalla. Es un límite esperable (WCAG no exige above-the-fold con zoom), pero M1 solo vale a tamaño de fuente por defecto. Resultado en un único motor (Chrome); Safari/Firefox y fuentes del SO móvil no probados.

**H4 · Bajo · Foco y mensajes tras errores (funciona; observaciones).**
- Observado OK: tras envío vacío el foco va al primer inválido (`campo-planta`), 4 errores, `aria-invalid` + `aria-describedby` correctos; el segundo envío (select corregido) mueve el foco a `campo-nombre` y quedan 3 errores; nombre con solo espacios se rechaza; el orden de Tab tras los errores es nombre → dirección → teléfono → notas → enviar (los `<span role="alert">` no son focalizables).
- Inferencia (no probado con lector de pantalla): 4 `role="alert"` inyectados a la vez pueden leerse en tropel; el `#resultado` pasa de `hidden` a visible con texto simultáneo, patrón que algunos lectores no anuncian de forma fiable. No se movió el foco al resultado tras éxito (el resultado queda visible en 360×640, verificado, pero el foco permanece en el botón).

**H5 · Bajo · Teléfono sin validación de formato.** «abc» se acepta en el envío simulado (observado). Es una maqueta; no hay criterio del brief que lo exija. Se anota para cualquier reutilización.

**H6 · Bajo · Sin enlace de salto ni landmark `banner`.** El `<header>` está dentro de `<main>` (no es `banner`). Hay un solo CTA y pocos controles previos, impacto práctico mínimo. No se incumple ningún criterio del brief.

**H7 · Bajo · Estados no medidos por la suite.** Contraste del estado `:active` (13.93 por cálculo mío) y del borde de error (7.33) no están en `playwright-check.mjs` ni en `ui.md` §2.1; ambos pasan. El botón deshabilitado (`ui.md` §5A, 3.01:1 y `opacity:.75`) no existe en la maqueta, así que el número no se ha podido comprobar renderizado. Exento de 1.4.3. Borde de tarjeta `#D2DDD3` sobre blanco = 1.40:1 (sobre `#F8FAF6` = 1.33): no es control; WCAG 1.4.11 no aplica a bordes decorativos de tarjetas.

**H8 · Bajo · `contrast-check.py` sigue marcando «(declarado inexacto)»** en 9 filas que `ui.md` ya corrigió, porque conserva en el código los valores originales (hallazgo F2 de `qa.md`, no resuelto). El cotejo ui.md == real sigue siendo manual. Los números vigentes de `ui.md` coinciden con la columna `real` (verificado con mis valores y con la salida del script).

**H9 · Informativo · Un solo escritor por archivo.** `ui.md` rev.2 **declara expresamente** la excepción («EXCEPCIÓN al principio de un escritor por archivo»), el motivo (reasignación a Antigravity intentada por Orca, falló por permisos en modo headless; la alternativa sin permisos no estaba autorizada) y exige que Antigravity «ratifique o revierta». La maqueta lleva cabecera «Escritor: Claude Code (archivo nuevo)». Estado: documentado, **no ratificado**. El autor git es siempre «Altiora», así que git no acredita la atribución; descansa en las cabeceras.

## Veredicto por criterio
| Criterio | Veredicto | Base |
|---|---|---|
| CTA sin scroll 360×640 | **PASS** (condicionado a tamaño de fuente por defecto, solo Chrome) | M1 332.4/640 medido; sondas con fuentes forzadas y 320 px dentro de 640; falla solo con texto al 200 % (H3) |
| Sin desbordamiento horizontal | **PASS** | M2 + sondas a 360 y 320 px, 0 elementos fuera |
| Teclado | **PASS** | K1–K3; orden de Tab y foco tras errores verificados (H4) |
| Nombres accesibles | **PASS** | A1/A2 + lectura de `aria-label`; 2.5.3 cumplido |
| Formulario | **CONDITIONAL** | Con JS funciona (F1/F2 + sondas); sin JS hace POST vacío a endpoint inexistente (H1); sin validar formato de teléfono (H5) |
| Contraste | **PASS** (alcance medido) | 15 pares del script + C1 renderizado (11 pares, incl. hover) + active/error por cálculo; estados Loading/Disabled no implementados, no medibles (H7) |
| Un escritor por archivo | **CONDITIONAL** | Excepción declarada en `ui.md` rev.2, falta ratificación de Antigravity (H9) |
| Preselección | **PASS** | P1, P2, K3 + clic real; sin JS degrada a elegir en el select (documentado, R1) |
| Fidelidad `ui.md` ↔ maqueta | **CONDITIONAL** | Deriva en imágenes, `novalidate`, estados y cifra 304 px (H1, H2) |

## Estado global
**CONDITIONAL. No es PASS global.**
Hallazgos P1 de ChatGPT (href inválido, label-in-name, CTA sin medir): **resueltos y reproducidos**. Pendientes para cerrar: (a) ratificación o reversión de `ui.md` rev.2 por Antigravity; (b) resolver H1 y alinear `ui.md` con la maqueta (H2), o declarar que `ui.md` §8 describe la especificación y no la maqueta; (c) revisión de otro proveedor o humana (esta es de independencia parcial) y prueba en otros motores/dispositivos reales; (d) lector de pantalla real (no ejecutado). La decisión sobre el issue #65 corresponde al fundador/coordinador.

## No ejecutado / límites
Lector de pantalla, Safari/Firefox, dispositivos reales, auditoría automatizada tipo axe (no instalada), zoom del navegador real (simulado con tamaño de fuente raíz), envío real al endpoint (no existe), commit (no autorizado).

Archivos: este informe (`tests/triad/ALT-TRIAD-001-qa-rev2.md`). Sin otros cambios.
