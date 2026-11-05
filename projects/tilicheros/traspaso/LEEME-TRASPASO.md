# El Tilichero CR · traspaso de trabajo (2026-11-04)

Escrito por Claude para quien siga (Antigravity, Codex u otro). Nada de esto está en un commit. Las reglas del dueño mandan sobre cualquier suposición.

## Reglas vigentes del dueño (no cambiar sin su orden)
- No publicar precios reales: lo cargado en Vintta usa **₡999 y stock 0** como provisional; el dueño corrige después.
- No contactar clientes, no gastar, no crear cuentas, no pedir contraseñas. Usar solo sesiones ya abiertas por el dueño.
- Marcas y réplicas: el dueño las autorizó («validadas por él»; no verificado). Títulos genéricos; no llamar «original» a nada sin factura del fabricante.
- Cada acción en Vintta se hace a petición expresa. Descargar archivos requiere permiso (se dio para los 10 PDF de Techno Go y el PDF 1HORA).

## Estado real
**Vintta (tienda ElTilicheroCR): 40 productos míos publicados a ₡999, stock 0 (Agotado).** Lotes 1, 2, 3 y 4 (carpetas `../vintta/lote-1`, `../vintta/navidad/...`). Títulos ≤60 caracteres (límite del formulario). Textos finales en `../vintta/textos-v2.md` y `../vintta/lote1_v2.json`. Verificados uno por uno en el panel.

Pendiente en Vintta (lo decide el dueño): precios reales, stock, fotos originales, categoría de juguetes (hoy en «Fiestas»/subcategoría «Juguetes»), descripciones del lote 4 (solo datos visibles de las fichas de MyTechnologyCR).

**Documentos entregados** (en `../proveedores/`): `ESTUDIO-COSTA-RICA-CON-VIRALES-EL-TILICHERO-2026-11-04.pdf` (el más reciente y el que debe usarse), `PROVEEDORES.md`, CSV de catálogo unificado (755 productos), `analisis-todos-los-productos.csv`, ranking `estudio-mercado-costa-rica-virales-ranking.csv`. Los PDF anteriores quedaron superados por el estudio de Costa Rica.

## Fuentes de datos de mercado (reproducibles)
- **Walmart Costa Rica**: API pública `walmart.co.cr/api/catalog_system/pub/products/search?ft=...&O=OrderByTopSaleDESC` (los espacios se codifican con `%20`). Scripts: `scripts/walmart_cr.py`, `walmart_marcas.py`, `walmart_desc.py`. Datos: `datos/walmart_*.json`. Es **un solo minorista**; el orden «más vendidos» no da unidades.
- **Google Trends y YouTube de Costa Rica**: se obtuvo ejecutando `fetch` en una pestaña de trends.google.com (API `explore` + `widgetdata/multiline`, `geo=CR`, 12 meses, ancla «audifonos»=56). Datos: `datos/trends_cr.json` (cada valor = [media 12 m, últimas 8 semanas, 8 anteriores]).
- **No accesibles**: Mercado Libre Costa Rica (pide iniciar sesión), TikTok Creative Center (sin datos sin sesión). No hay datos de TikTok ni Instagram; los «virales» son Google/YouTube de Costa Rica.

## Cómo regenerar (rutas)
Los scripts reciben rutas por argumentos; varios esperan una carpeta de trabajo con `thumbs/mapa.json`, `agotados.json`, `walmart_cr.json`, `trends_cr.json` y los PDF de Techno Go (no incluidos: pesan 203 MB; carpeta de Drive «Catálogos PDF» `1i6tsGlCZ0y9g6yDGr08huJa9hmGY0OoV`, requiere permiso para descargar). Esta carpeta trae `datos/` listo; `datos/mapa-fotos-relativo.json` es el mapa de fotos con rutas relativas al proyecto (`thumbs/mapa.json` conserva rutas absolutas de la sesión anterior, no sirven).
- Estudio final: `scripts/estudio_cr2.py` (usa `analisis_total.py` como base; argumentos: carpeta `proveedores`, salida html, carpeta de datos, salida csv). PDF: Edge headless con `--allow-file-access-from-files --print-to-pdf`.
- Requiere `pip install --user pymupdf` (instalado en la máquina del dueño).

## Errores que encontré y conviene no repetir
1. **MyTechnologyCR «Pulso Ultra/Pulso Liso» son correas de reloj, no relojes.** La categoría «Relojes» de ese proveedor está sobrestimada en el análisis. Ya corregido en Vintta.
2. Al editar en Vintta por título, **títulos con el mismo prefijo se confunden** (dos «Audífonos de diadema» se pisaron). Buscar por título completo exacto.
3. Los recortes de fotos de Techno Go (marcas ORIGINAL) son «la imagen más cercana»; pueden mostrar productos vecinos. 18 productos no tienen foto.
4. Sellos AGOTADO detectados por color rojo: 19 productos; puede haber más.
5. Los pesos del puntaje (demanda, margen, video, foto) son criterio mío, no una fórmula validada. «Ganador» = candidato prioritario, no venta asegurada.

## Cómo se carga en Vintta (panel de proveedor)
- Mi Cuenta → «Panel de proveedor» → pestaña Publicar. Campos obligatorios: título (máx. 60), estado, precio, inventario, categoría. **No hay borrador: «Publicar» publica ya.** Una sola foto por la vía usada; categorías existentes: Vintage, Flores, Fiestas, Electrónicos, Moda, Hogar, Animales.
- Las fotos se pasaron con un servidor local temporal (CORS) y `DataTransfer` sobre el input de archivo; no hay carga masiva.
- Edición: Inventario → clic en el producto → «Editar» → «Guardar cambios».

## Siguiente paso sugerido (valor para vender)
El cuello de botella ya no son los datos: es que el dueño ponga **precios reales y stock** a los 40 productos (comisión de Vintta y envío definen el mínimo) y consiga fotos originales. Después medir ventas por producto y ajustar el ranking con esos números.
