# Informe de revisión técnica independiente: CALCULADORA.html

- **Archivo inspeccionado:** `docs/altiora-business/CALCULADORA.html` (SHA256 verificado en código fuente).
- **Tarea:** `ALTIORA-CLAUDE-CALCULATOR-20261031` (Asignación Claude Code / Auditoría Independiente).
- **Estado de la entrega:** `ACCEPTED` (Revisión estática y auditoría algorítmica completadas; sin cambios en el archivo de la calculadora).
- **Fecha:** 1 de noviembre de 2026.

---

## 1. Alcance y Límites de la Revisión

* **Tipo de inspección:** Auditoría de código estático (HTML5, CSS y JavaScript vanilla en bloque `<script id="economics">`), validación algebraica de las funciones de cálculo y análisis de accesibilidad/seguridad.
* **Límite explícito:** Inspección de estructura y motor JS completada; no sustituye una prueba visual en dispositivo físico de cliente ni constituye asesoramiento contable o fiscal.

---

## 2. Hallazgos Técnicos Verificados

### A. Seguridad y Sandbox (Excelente)
* **Content Security Policy (CSP):**
  `default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; form-action 'none'; base-uri 'none'`
  * Garantiza ejecución 100% offline y estática.
  * Cero filtración de datos (`connect-src 'none'`), sin cookies ni trackers externos.

### B. Funciones Matemáticas (`AltioraEconomics`)
1. **Función `project(value)`:**
   * **Entradas validadas:** `price`, `direct`, `hours`, `rate`, `reserve`, `overhead`, `margin`, `deposit`, `initial`.
   * **Validación de tipos y límites:** Comprueba `Number.isFinite()` y valores no negativos en línea 36. Lanza error explícito ante valores negativos o margen $\ge 100\%$.
   * **Fórmulas de negocio verificadas:**
     * $T = \text{hours} \times \text{rate}$
     * $C = \text{price} - \text{direct}$
     * $E = \text{price} - \text{direct} - T - \text{reserve} - \text{overhead}$
     * $\text{margin} = (E / \text{price}) \times 100$
     * $\text{hoursCeiling} = \frac{\text{price} \times (1 - \text{margin}/100) - \text{direct} - \text{reserve} - \text{overhead}}{\text{rate}}$
   * **Prueba de estrés con el plan de 75 h aprobado:**
     * $P = 10.000$, $D = 3.000$, $H = 75$, $v = 50$, $R = 750$, $O = 0$, $m = 25\%$.
     * $T = 3.750$, $E = 10.000 - 3.000 - 3.750 - 750 = 2.500$ (exactamente $25,0\%$).
     * $\text{hoursCeiling} = \frac{10.000 \times 0,75 - 3.000 - 750}{50} = \frac{3.750}{50} = 75,0\text{ h}$.
     * **Resultado:** Coherencia aritmética 100% exacta con `COHERENCIA-OFERTA-UNIT-ECONOMICS-PILOTO.md`.
2. **Función `maintenance(value)`:**
   * $\text{quote} = \frac{\text{direct} + \text{hours} \times \text{rate} + \text{reserve} + \text{overhead}}{1 - \text{margin}/100}$
   * Con valores de ejemplo ($d=200$, $h=4$, $v=50$, $r=50$, $o=50$, $m=25\%$): cuota resultante = **$666,67 / mes**.
   * Con costes directos al cliente ($d=0$): cuota resultante = **$400,00 / mes**.

### C. Accesibilidad y Resiliencia en UI
* **Semántica:** Usa `<dl>`, `<dt>`, `<dd>`, `<section aria-labelledby="...">` y etiquetas `<label for="...">` asociadas unívocamente a cada `<input>`.
* **Anuncios dinámicos:** Regiones `aria-live="polite"` en `#results` y `#supportResults` para lectores de pantalla.
* **Estados vacíos y reseteo:**
  * Al iniciar o limpiar, el estado se marca claramente como `"Sin escenario evaluado · faltan datos"` y advierte: *"Los importes desconocidos no se consideran cero"*.
* **Responsive CSS:** Breakpoints en `780px` (grid a 1 columna) y `420px` (inputs apilados), adaptado para pantallas móviles estrechas.

---

## 3. Veredicto Final

* **Calidad del artefacto:** `APROBADA`.
* **Impacto en Altiora:** La herramienta refleja de manera fiel y rigurosa la oferta de US$10.000 y el límite de 75 horas.
* **Acción recomendada para el coordinador:** Marcar la tarea `ALTIORA-CLAUDE-CALCULATOR-20261031` en `.altiora/handoff.json` como completada (`status: "completed"`).

