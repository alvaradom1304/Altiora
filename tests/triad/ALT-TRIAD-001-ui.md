# ALT-TRIAD-001 · Esquema Visual UI (Antigravity) — ejercicio FICTICIO

> **Metadatos de la sesión y ejecución**
> - **Cliente**: Antigravity (IDE / CLI)
> - **Versión**: 1.4.12 (Gemini 3.8 Flash High)
> - **Sesión**: `e32db730-28bd-46b4-bee5-189a0e1bb051`
> - **Rama**: `tests/triad/ui`
> - **Commit**: `test(triad): ALT-TRIAD-001 ui (Antigravity)`
> - **Fecha**: 2026-11-03
> - **Aviso**: Ejercicio puramente FICTICIO. Marca, productos, precios, testimonios y servicios son ficticios para prueba de triada.


> **Nota de revisión (2026-11-03, Claude Code como director operativo):** los ratios de la sección 2 y menciones asociadas se recalcularon con `tests/triad/contrast-check.py` (fórmula WCAG 2.x). 9 de 11 valores originales eran inexactos (siempre por debajo del real, sin cambiar el veredicto AA). El botón deshabilitado pasa de 3.2:1 a 3.01:1 (exento de AA). Versión original: commit `e1d774f` (Antigravity). **Este archivo debe ser revisado por un revisor independiente; la corrección no equivale a aprobación.**

---

## 1. Resumen Ejecutivo y Criterios del Brief

Este documento define el esquema visual y de interacción verificable para la landing page de la tienda ficticia de plantas de interior **"Verdía"**, dando cumplimiento estricto a los 4 criterios de éxito de `tests/triad/ALT-TRIAD-001-brief.md`:

1. **Acción principal única above-the-fold**: Botón "Pedir mi planta" visible sin scroll en pantalla móvil de 360×640 px y desktop.
2. **5 Secciones estructuradas**: Héroe, 3 plantas destacadas (con precio ficticio), Cuidado en 3 pasos, Preguntas frecuentes y Formulario de pedido.
3. **Resiliencia técnica**: 100% legible y operable en DOM completo sin JavaScript ni WebGL/3D (CSS puro, elementos semánticos nativos `<details>` y `<form>`). Soporte completo de `@media (prefers-reduced-motion: reduce)` y ancho móvil mínimo de 360 px.
4. **Accesibilidad WCAG 2.2 AA**: Contraste de texto y componentes con ratios superiores a 4.5:1 (texto normal) y 3:1 (texto grande e interfaz), con indicador de foco visible en todo control interactivo.

---

## 2. Tokens de Color y Matriz de Contraste WCAG 2.2 AA

Todos los valores de color han sido seleccionados para superar el nivel AA de WCAG 2.2:

| Token / Rol | Valor HEX | Uso principal | Fondo contrastante | Ratio calculado | Criterio WCAG AA | Veredicto |
|---|---|---|---|---|---|---|
| `--color-bg-canvas` | `#F8FAF6` | Fondo general de la página | N/A | N/A | N/A | Base |
| `--color-bg-surface` | `#FFFFFF` | Fondo de tarjetas y formulario | `#F8FAF6` | 1.05:1 | Delimitado por borde | Base |
| `--color-text-primary` | `#132E1B` | Títulos (H1-H3), etiquetas y cuerpo | `#F8FAF6` | **13.94:1** | Mínimo 4.5:1 (3:1 grande) | **PASS (AAA)** |
| `--color-text-primary` | `#132E1B` | Títulos y cuerpo sobre tarjeta | `#FFFFFF` | **14.64:1** | Mínimo 4.5:1 | **PASS (AAA)** |
| `--color-text-muted` | `#2D5438` | Metadatos, subtítulos secundarios | `#F8FAF6` | **8.21:1** | Mínimo 4.5:1 | **PASS (AA)** |
| `--color-text-muted` | `#2D5438` | Metadatos sobre tarjeta blanca | `#FFFFFF` | **8.62:1** | Mínimo 4.5:1 | **PASS (AA)** |
| `--color-cta-bg` | `#1E5E3A` | Fondo botón "Pedir mi planta" | `#F8FAF6` | **7.36:1** (borde/botón) | Mínimo 3:1 (UI component) | **PASS (AA)** |
| `--color-cta-text` | `#FFFFFF` | Texto botón "Pedir mi planta" | `#1E5E3A` | **7.73:1** | Mínimo 4.5:1 (texto normal) | **PASS (AA)** |
| `--color-cta-hover` | `#144428` | Fondo botón en hover/active | `#FFFFFF` | **11.13:1** | Mínimo 4.5:1 | **PASS (AA)** |
| `--color-focus-ring` | `#0E5E35` | Contorno de foco visible (3px solid) | `#F8FAF6` / `#FFFFFF` | **7.49:1 / 7.86:1** | Mínimo 3:1 (focus indicator) | **PASS (AA)** |
| `--color-border-card` | `#D2DDD3` | Borde de tarjetas y separadores | `#F8FAF6` | **1.33:1** (no textual) | Borde visual estructural | **PASS** |
| `--color-border-input`| `#2D5438` | Borde de campos de formulario | `#FFFFFF` | **8.62:1** | Mínimo 3:1 (form boundary) | **PASS (AA)** |
| `--color-error` | `#B00020` | Mensaje de validación / error | `#FFFFFF` | **7.33:1** | Mínimo 4.5:1 | **PASS (AA)** |
| `--color-badge-bg` | `#E3EFE4` | Fondo de insignia precio ficticio | `#132E1B` (texto) | **12.36:1** | Mínimo 4.5:1 | **PASS (AAA)** |

---

## 3. Jerarquía Tipográfica y Espaciado

Escala fluida mediante `clamp()` con tamaño base de 16 px (1rem) para evitar zoom automático no deseado en dispositivos táctiles iOS/Android:

- **H1 (Título Héroe)**: `clamp(2rem, 5vw + 1rem, 2.75rem)` (32 px – 44 px), `font-weight: 700`, `line-height: 1.2`. Color: `#132E1B`.
- **H2 (Títulos de Sección)**: `clamp(1.5rem, 3vw + 0.75rem, 2rem)` (24 px – 32 px), `font-weight: 600`, `line-height: 1.25`. Color: `#132E1B`.
- **H3 (Títulos de Tarjetas / Pasos)**: `1.25rem` (20 px), `font-weight: 600`, `line-height: 1.3`. Color: `#132E1B`.
- **P / Body (Párrafos y labels)**: `1rem` (16 px), `font-weight: 400`, `line-height: 1.5`. Color: `#132E1B`.
- **Caption / Metadata**: `0.875rem` (14 px), `font-weight: 500`, `line-height: 1.4`. Color: `#2D5438`.
- **Espaciado vertical entre secciones**: `48px` en móvil 360 px / `80px` en desktop (5rem).

---

## 4. Estructura de Secciones y Jerarquía DOM

### Sección 1: Héroe (`#heroe`) — Above the Fold
- **Contenedor**: `<header class="hero-section" id="heroe">`
- **Jerarquía visual y DOM**:
  1. **Logotipo / Marca**: `<span class="brand-logo">Verdía [FICTICIO]</span>` (20 px, semi-bold).
  2. **Encabezado principal (H1)**: `<h1>Plantas de interior cuidadas para durar en tu hogar</h1>`
  3. **Subtítulo descriptivo**: `<p class="hero-subtext">Seleccionadas según tu nivel de luz y entregadas en maceta lista en 24-48 horas. [FICTICIO]</p>`
  4. **Acción Principal Única (CTA Above the Fold)**:
     ```html
     <div class="hero-actions">
       <a href="#pedido" class="btn-cta-primary" id="cta-principal">
         Pedir mi planta
       </a>
     </div>
     ```
  5. **Insignia de confianza**: `<p class="hero-trust">Garantía de adaptación de 30 días · Guía física de riego incluida [FICTICIO]</p>`
  6. **Imagen descriptiva semántica**:
     `<img src="/img/ficticio/hero-plantas.jpg" alt="Mesa de madera con una monstera y una sansevieria en macetas de cerámica verde" width="600" height="400" loading="eager" />`
- **Comprobación de visibilidad 360 px**:
  - En viewport de 360×640 px, el bloque completo (Logo: 32px + H1: 96px + Subtítulo: 60px + CTA: 52px + Márgenes: 64px = 304 px) se ubica holgadamente antes de los 580 px visibles, garantizando que el usuario ve el botón "Pedir mi planta" sin hacer scroll.

---

### Sección 2: 3 Plantas Destacadas con Precio Ficticio (`#catalogo`)
- **Contenedor**: `<section class="catalog-section" id="catalogo" aria-labelledby="catalog-heading">`
- **Encabezado (H2)**: `<h2 id="catalog-heading">Plantas destacadas para empezar [FICTICIO]</h2>`
- **Subtítulo**: `<p class="section-lead">Variedades resistentes, adaptadas a departamentos y casas con luz natural. [FICTICIO]</p>`
- **Estructura de Tarjetas (Grid 1 columna en móvil 360px, 3 columnas en desktop)**:

  1. **Tarjeta 1: Monstera Deliciosa [FICTICIO]**
     - Imagen: `<img src="/img/ficticio/monstera.jpg" alt="Monstera Deliciosa en maceta blanca" width="320" height="240" loading="lazy" />`
     - Título (H3): `<h3>Monstera Deliciosa</h3>`
     - Insignia de cuidado: `<span class="badge-tag">Luz indirecta media · Riego semanal</span>`
     - Descripción: `<p>Hojas amplias y porte selvático para salas de estar.</p>`
     - Precio ficticio destacado: `<p class="price-tag"><span class="price-value">$24 USD</span> <span class="price-fictitious">[PRECIO FICTICIO]</span></p>`
     - Enlace de selección accesible: `<a href="#pedido?planta=monstera" class="btn-card-select" aria-label="Elegir Monstera Deliciosa por $24 USD ficticios">Elegir esta planta</a>`

  2. **Tarjeta 2: Sansevieria Trifasciata [FICTICIO]**
     - Imagen: `<img src="/img/ficticio/sansevieria.jpg" alt="Sansevieria en maceta cilíndrica de gres" width="320" height="240" loading="lazy" />`
     - Título (H3): `<h3>Sansevieria Trifasciata</h3>`
     - Insignia de cuidado: `<span class="badge-tag">Cualquier nivel de luz · Riego cada 15 días</span>`
     - Descripción: `<p>Extremadamente resistente a olvidos de riego y espacios sombreados.</p>`
     - Precio ficticio destacado: `<p class="price-tag"><span class="price-value">$19 USD</span> <span class="price-fictitious">[PRECIO FICTICIO]</span></p>`
     - Enlace de selección accesible: `<a href="#pedido?planta=sansevieria" class="btn-card-select" aria-label="Elegir Sansevieria Trifasciata por $19 USD ficticios">Elegir esta planta</a>`

  3. **Tarjeta 3: Ficus Lyrata Compacto [FICTICIO]**
     - Imagen: `<img src="/img/ficticio/ficus.jpg" alt="Ficus Lyrata en maceta de arcilla verde" width="320" height="240" loading="lazy" />`
     - Título (H3): `<h3>Ficus Lyrata Compacto</h3>`
     - Insignia de cuidado: `<span class="badge-tag">Luz brillante sin sol directo · Riego moderado</span>`
     - Descripción: `<p>Hojas tipo violín de porte erguido y elegante.</p>`
     - Precio ficticio destacado: `<p class="price-tag"><span class="price-value">$29 USD</span> <span class="price-fictitious">[PRECIO FICTICIO]</span></p>`
     - Enlace de selección accesible: `<a href="#pedido?planta=ficus" class="btn-card-select" aria-label="Elegir Ficus Lyrata por $29 USD ficticios">Elegir esta planta</a>`

---

### Sección 3: Cuidado en 3 Pasos (`#cuidado`)
- **Contenedor**: `<section class="care-section" id="cuidado" aria-labelledby="care-heading">`
- **Encabezado (H2)**: `<h2 id="care-heading">Cuidado sin complicaciones en 3 pasos [FICTICIO]</h2>`
- **Lista ordenada semántica (`<ol class="care-steps">`)**:
  1. **Paso 1: Ubica según su etiqueta**
     - Encabezado (H3): `<h3>1. Ubicación con luz adecuada</h3>`
     - Texto: `<p>Coloca la maceta cerca de ventanas sin sol directo del mediodía para evitar quemar sus hojas.</p>`
  2. **Paso 2: Riega solo con sustrato seco**
     - Encabezado (H3): `<h3>2. Riego por comprobación</h3>`
     - Texto: `<p>Introduce un dedo 3 cm en la tierra. Si notas humedad, espera 3 días más antes de regar.</p>`
  3. **Paso 3: Ficha de seguimiento físico**
     - Encabezado (H3): `<h3>3. Calendario incluido</h3>`
     - Texto: `<p>Cada planta llega con una tarjeta de cuidados ilustrada y personalizada para tu zona climática. [FICTICIO]</p>`

---

### Sección 4: Preguntas Frecuentes (`#faq`)
- **Contenedor**: `<section class="faq-section" id="faq" aria-labelledby="faq-heading">`
- **Encabezado (H2)**: `<h2 id="faq-heading">Preguntas frecuentes [FICTICIO]</h2>`
- **Resiliencia sin JavaScript**: Implementado con componentes nativos `<details>` y `<summary>`:
  - `<details class="faq-item">`
    - `<summary class="faq-question">¿Cómo viajan las plantas sin dañarse en el camino? [FICTICIO]</summary>`
    - `<div class="faq-answer"><p>Viajan en cajas térmicas reforzadas con soporte de raíz anti-vuelco y sustrato humidificado para soportar trayectos de hasta 72 horas sin marchitarse.</p></div>`
  - `<details class="faq-item">`
    - `<summary class="faq-question">¿Qué cubre la garantía de 30 días si mi planta se marchita? [FICTICIO]</summary>`
    - `<div class="faq-answer"><p>Si tu planta muestra signos de daño irreversible durante el primer mes siguiendo la guía, te enviamos una nueva planta sin coste adicional o te devolvemos el dinero.</p></div>`
  - `<details class="faq-item">`
    - `<summary class="faq-question">¿Son seguras para convivir con gatos y perros? [FICTICIO]</summary>`
    - `<div class="faq-answer"><p>En la ficha de cada planta señalamos claramente su nivel de toxicidad. La Sansevieria y Monstera deben ubicarse fuera del alcance de mascotas mordedoras; ofrecemos alternativas 100% no tóxicas como la Calathea.</p></div>`
  - `<details class="faq-item">`
    - `<summary class="faq-question">¿Cuáles son los medios de pago aceptados? [FICTICIO]</summary>`
    - `<div class="faq-answer"><p>Aceptamos tarjetas de débito, crédito y pago contra entrega al momento de recibir la planta en tu domicilio. [FICTICIO]</p></div>`

---

### Sección 5: Pedido en Línea (`#pedido`)
- **Contenedor**: `<section class="order-section" id="pedido" aria-labelledby="order-heading">`
- **Encabezado (H2)**: `<h2 id="order-heading">Pide tu planta en línea [FICTICIO]</h2>`
- **Subtítulo**: `<p>Formulario de pedido directo. Sin registro obligatorio ni pasos innecesarios. [FICTICIO]</p>`
- **Formulario accesible y nativo (`<form method="POST" action="/api/pedido-ficticio" class="order-form">`)**:
  1. **Selección de planta**:
     ```html
     <div class="form-group">
       <label for="campo-planta">Elige tu planta [FICTICIO] <span aria-hidden="true">*</span></label>
       <select id="campo-planta" name="planta" required class="form-control">
         <option value="">-- Selecciona una variedad --</option>
         <option value="monstera">Monstera Deliciosa — $24 USD [FICTICIO]</option>
         <option value="sansevieria">Sansevieria Trifasciata — $19 USD [FICTICIO]</option>
         <option value="ficus">Ficus Lyrata Compacto — $29 USD [FICTICIO]</option>
       </select>
     </div>
     ```
  2. **Nombre completo**:
     ```html
     <div class="form-group">
       <label for="campo-nombre">Nombre y apellido <span aria-hidden="true">*</span></label>
       <input type="text" id="campo-nombre" name="nombre" required autocomplete="name" class="form-control" placeholder="Ej. Mariana Soto" />
     </div>
     ```
  3. **Dirección de entrega**:
     ```html
     <div class="form-group">
       <label for="campo-direccion">Dirección completa de entrega <span aria-hidden="true">*</span></label>
       <input type="text" id="campo-direccion" name="direccion" required autocomplete="street-address" class="form-control" placeholder="Calle, número, depto y ciudad" />
     </div>
     ```
  4. **Teléfono de contacto**:
     ```html
     <div class="form-group">
       <label for="campo-telefono">Teléfono móvil para aviso de entrega <span aria-hidden="true">*</span></label>
       <input type="tel" id="campo-telefono" name="telefono" required autocomplete="tel" class="form-control" placeholder="Ej. +57 300 123 4567" />
     </div>
     ```
  5. **Instrucciones opcionales**:
     ```html
     <div class="form-group">
       <label for="campo-notas">Instrucciones para el repartidor (opcional)</label>
       <textarea id="campo-notas" name="notas" rows="2" class="form-control" placeholder="Ej. Timbre 4B o dejar en conserjería"></textarea>
     </div>
     ```
  6. **Botón de Envío (CTA de Formulario)**:
     ```html
     <div class="form-group">
       <button type="submit" class="btn-cta-submit">
         Confirmar mi pedido [FICTICIO]
       </button>
     </div>
     ```
  7. **Texto legal y de privacidad**:
     `<p class="form-disclaimer">Tus datos se usan únicamente para coordinar la entrega ficticia. Ejercicio de prueba no transaccional.</p>`

---

## 5. Especificación de Estados de Interacción

Para garantizar accesibilidad y feedback claro al usuario, todos los componentes interactivos definen sus 6 estados:

### A. Botón Principal CTA (`.btn-cta-primary` y `.btn-cta-submit`)
- **Default**:
  - `background-color: #1E5E3A`
  - `color: #FFFFFF`
  - `padding: 14px 28px`
  - `min-height: 48px` (Touch target >= 44 px)
  - `font-size: 1rem` (16 px), `font-weight: 600`
  - `border: 2px solid transparent`
  - `border-radius: 8px`
  - `display: inline-flex; align-items: center; justify-content: center`
- **Hover**:
  - `background-color: #144428` (oscurecimiento visible, ratio 11.13:1)
  - `transform: translateY(-1px)` (solo cuando no hay reduced motion)
- **Focus-visible (Navegación por teclado)**:
  - `outline: 3px solid #0E5E35`
  - `outline-offset: 3px`
  - `box-shadow: 0 0 0 2px #FFFFFF` (anillo doble para contraste garantizado contra fondos oscuros y claros)
- **Active (Click / Tap)**:
  - `background-color: #0E331B`
  - `transform: translateY(1px)`
- **Disabled (`:disabled` o `[aria-disabled="true"]`)**:
  - `background-color: #7D9C86` (contraste real 3.01:1 con texto blanco; los controles deshabilitados están exentos de WCAG 1.4.3, pero no depender solo del color)
  - `cursor: not-allowed`
  - `opacity: 0.75`
- **Loading / Submitting**:
  - Contenedor con `aria-busy="true"`
  - Texto sustituido por mensaje accesible: "Enviando pedido..." y spinner animado en SVG (reemplazado por texto estático en reduced motion).

### B. Campos de Entrada (`.form-control`: input, select, textarea)
- **Default**:
  - `background-color: #FFFFFF`
  - `color: #132E1B`
  - `border: 2px solid #2D5438` (contraste de borde 8.62:1 con el fondo blanco)
  - `border-radius: 6px`
  - `min-height: 48px` (en inputs y selects)
  - `font-size: 1rem` (16 px)
- **Hover**:
  - `border-color: #132E1B` (aumento de grosor perceptible o contraste)
- **Focus-visible**:
  - `border-color: #1E5E3A`
  - `outline: 3px solid #0E5E35`
  - `outline-offset: 2px`
- **Error / Estado Inválido (`:invalid:not(:placeholder-shown)` o `.has-error`)**:
  - `border-color: #B00020`
  - `outline-color: #B00020`
  - Mensaje de error vinculado: `<span id="err-[id]" class="error-text" role="alert">Este campo es obligatorio</span>`
  - Asociación semántica: `aria-invalid="true" aria-describedby="err-[id]"`

### C. Desplegables de FAQ (`details.faq-item > summary`)
- **Default**:
  - `padding: 16px 20px`
  - `background-color: #FFFFFF`
  - `border: 1px solid #D2DDD3`
  - `border-radius: 8px`
  - `cursor: pointer`
  - `min-height: 48px`
  - `font-weight: 600`
- **Hover**:
  - `background-color: #F0F6F1`
- **Focus-visible**:
  - `outline: 3px solid #0E5E35`
  - `outline-offset: 2px`
- **Open (`details[open]`)**:
  - `border-color: #2D5438`
  - Borde inferior en el summary para separar pregunta y respuesta.

---

## 6. Soporte de Movimiento Reducido (`prefers-reduced-motion`)

Para cumplir con WCAG 2.2 Criterio 2.3.3 (Animation from Interactions) y el criterio de resiliencia del brief:

```css
/* Soporte nativo de movimiento reducido */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }

  /* Desactivación de elevaciones transform en hover */
  .btn-cta-primary:hover,
  .btn-card-select:hover,
  .catalog-card:hover {
    transform: none !important;
  }

  /* Despliegue instantáneo de FAQ */
  details[open] .faq-answer {
    animation: none !important;
  }
}
```

- **Sin animación obligatoria**: Ninguna información depende de transiciones, banners móviles ni sliders. Todo el contenido está desplegado o es accesible mediante pulsación directa.

---

## 7. Adaptación Móvil Extrema (Viewport 360 px)

El diseño está concebido bajo metodología **Mobile-First** con prueba obligatoria en **360×640 px**:

- **Viewport meta tag**:
  `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">`
- **Restricción de desbordamiento horizontal**:
  - `body, main { max-width: 100%; overflow-x: hidden; }`
  - `* { box-sizing: border-box; }`
  - `img { max-width: 100%; height: auto; display: block; }`
- **Márgenes y contenido útil en 360 px**:
  - Padding lateral de contenedor: `16px` a cada lado.
  - Ancho disponible para contenido: `360px - 32px = 328px`.
  - Tarjetas de catálogo: Ancho del 100% (`328px`), con disposición vertical de imagen, texto y botón.
- **Tamaño de objetivos táctiles (Touch Targets WCAG 2.5.8)**:
  - Botón CTA Héroe: `min-height: 50px`, ancho completo `100%` en móvil.
  - Botones de tarjetas: `min-height: 48px`, ancho completo `100%`.
  - Separación vertical mínima entre botones adyacentes: `16px`.
  - Summary de FAQ: `min-height: 48px`, padding vertical de `16px`.
  - Inputs de formulario: `min-height: 48px`, tipografía a 16 px (evita auto-zoom).

---

## 8. Verificación de Conformidad contra Criterios del Brief

| Criterio del Brief | Requisito de Éxito | Implementación en Esquema Visual | Estado |
|---|---|---|---|
| **1. Acción principal única** | Visible sin scroll: "Pedir mi planta" | Botón `#cta-principal` dentro del primer bloque visible (altura total ~304 px < 580 px en móvil 360 px) | **CUMPLIDO** |
| **2. Secciones obligatorias** | Héroe, 3 plantas con precio ficticio, 3 pasos de cuidado, FAQ, Pedido | Secciones 1 a 5 detalladas con semántica HTML5 (`header`, `section`, `ol`, `details`, `form`) | **CUMPLIDO** |
| **3. Resiliencia y DOM completo** | Legible sin JS, movimiento reducido, móvil 360 px | CSS puro, sin dependencias 3D/JS, media query de reduced motion, layout fluido 328 px utilizables en 360 px | **CUMPLIDO** |
| **4. Contraste y Accesibilidad** | Contraste AA y foco visible | Tabla de 14 tokens de color con ratios de 7.36:1 a 14.64:1 en texto y componentes activos (todos superan WCAG AA), foco `3px solid #0E5E35` con offset | **CUMPLIDO** |
| **5. Prevención de riesgos** | Sin invención de datos comerciales, todo ficticio, sin 3D | Marca "Verdía", precios y garantías etiquetados explícitamente como `[FICTICIO]`; 0 WebGL / 0 Canvas | **CUMPLIDO** |

---

## 9. Próximo Paso en el Flujo de la Triada

Con este entregable completado por **Antigravity**, el archivo `tests/triad/ALT-TRIAD-001-ui.md` queda listo para la revisión independiente de calidad y accesibilidad por parte del rol **Codex** en `tests/triad/ALT-TRIAD-001-qa.md`, conforme al reparto definido en `tests/triad/ALT-TRIAD-001-brief.md`.
