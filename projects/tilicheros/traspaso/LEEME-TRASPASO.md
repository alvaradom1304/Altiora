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

## Imágenes de producto · lote 1 (Codex, 2026-11-05)

- 40 imágenes nuevas con imagegen integrado, cuatro de cada uno de los diez primeros productos publicados que coinciden con el orden del ranking. Guardadas en `projects/tilicheros/imagenes/<producto>/`, PNG 1080×1080, con `indice-lote-1.csv`.
- Revisión: `imagenes/revision-lote-1.html`; método, fuentes, prompts y límites en `imagenes/ENTREGA-LOTE-1.md` y `manifest-produccion-lote-1.json`. Verificación técnica PASS: 40 archivos únicos, diez referencias locales intactas y enlaces de galería existentes. Revisión visual secuencial; sin cotejo físico ni revisión independiente.
- SUPUESTO: fidelidad fina, medidas y variantes disponibles; especial atención al 895B (foto ambigua) y Lovely Baby (múltiples variantes). Son recreaciones de IA, no prueba de autenticidad ni de ausencia de marcas en el producto físico.
- Se generaron escenas nuevas; no se borraron logos de las fotos del proveedor. Borrador para solicitar fotos y permiso de uso en `imagenes/mensaje-proveedor-fotos.md`, NO enviado.
- No hubo descargas, compras, contactos, cambios/publicación en Vintta, push, PR ni merge. La capacidad multifoto del panel sigue sin verificar.
- Los otros 30 productos quedan pendientes del visto bueno del dueño al lote 1. No continuar su generación sin esa aprobación.
- Control común del repositorio: `npm run check` PASS (salida 0); log en `imagenes/npm-check-lote-1.log`. El lote sigue pendiente de visto bueno humano.

## Reemplazo selectivo de fotos con proveedor · Codex, 2026-11-06

- Nuevo criterio del dueño: conservar fotos sin información del distribuidor; generar una sola foto nueva para las que sí la muestran. Marcas validadas por el dueño (sin verificación independiente de autenticidad). No afirmar originalidad.
- Auditoría visual de las 40 fotos archivadas de lo publicado: 29 se conservan; 11 muestran información del proveedor (TCR-029 y TCR-031 a TCR-040). El estado actual en el panel no se comprobó.
- Se crearon dos nuevas escenas con imagegen integrado para TCR-038 y TCR-039, PNG 1080x1080. Guardadas en sus carpetas de producto como principal-reemplazo-selectivo-2026-11-06.png; versiones anteriores y 40 fuentes intactas, comprobadas por SHA-256.
- Comparación anterior/nueva y apartados de cuatro lotes en imagenes/reemplazo-selectivo-2026-11-06/index.html. Fotos incrustadas; ampliación interna sin depender de OneDrive. PDF de dos comparaciones, CSV de 40 decisiones, índice de nuevas, prompts y evidencia en la misma carpeta. Prueba de visor con Edge: PASS, 42 imágenes cargadas, 4 lotes de 10, teclado/móvil/ampliación, cero solicitudes remotas ni errores de página.
- VERIFICADO: no se ve información del proveedor en las dos nuevas imágenes. SUPUESTO: fidelidad fina de malla, goma, emblema y moldes; la variante roja debe validarse contra unidad física. NO SÉ: inventario, autenticidad independiente ni publicación actual. Revisión secuencial; no hubo revisor independiente.
- Pendientes 9 reemplazos después del visto bueno al lote 1. Los 8 restantes del lote 1 se conservan por el criterio de proveedor; eso no equivale a aprobar toda su fidelidad. La referencia archivada GM201 sigue mezclando modelos y no se cambió en esta tarea.
- Sin cambios en Vintta, descargas remotas, contactos, compras, API de pago alternativa, push, PR ni merge. La reparación anterior de enlaces en Google Sheets sigue incompleta; no se retomó con este encargo.
- Control general de este reemplazo selectivo: npm run check PASS (salida 0); log en imagenes/reemplazo-selectivo-2026-11-06/npm-check.log.

## Carga completa de imágenes del lote 1 en Vintta · Codex, 2026-11-06

- El dueño autorizó explícitamente subir las 40 imágenes IA existentes del lote de producción 1 (cuatro para cada uno de sus diez productos) y aplazar los ajustes de fidelidad. No se generaron imágenes adicionales.
- VERIFICADO: 40 imágenes añadidas a los 10 productos. Se conservó la foto principal que ya tenía cada uno: cinco fotos por producto, 50 fotos en sus galerías. Las principales nuevas de TCR-038 y TCR-039 se conservaron. El panel admite hasta seis fotos y la primera es principal, comprobado en el formulario y con cargas múltiples reales.
- Guardado mediante el formulario normal del panel de proveedor, cuenta ElTilicheroCR. Los títulos completos se contrastaron con el registro. Campos ajenos a fotos idénticos antes de guardar: título, precio, stock, descripción, estado y clasificación. No se editaron los demás productos.
- VERIFICADO: tras recargar la tienda se abrieron las diez fichas públicas; cada una mostró las cinco URL de imagen guardadas, en el mismo orden. Evidencia: imagenes/carga-lote-1-vintta-2026-11-06/resultado-final.json, verificacion-publica.json, resumen.csv y tres capturas.
- Los fallos de fidelidad siguen pendientes de ajuste por instrucción del dueño. En especial TCR-027: las imágenes IA previas muestran BT03 aunque el producto es GM201. Esta carga no convierte la fidelidad en aprobada. Marcas validadas por el dueño; autenticidad independiente sin verificar.
- El visor selectivo muestra el estado actualizado y acceso a las 40 vistas. No hubo compras, contactos, descargas remotas, push, PR ni merge. Los lotes de producción 2, 3 y 4 no se cargaron con este encargo.
- Control de repositorio de esta carga: npm run check se ejecutó y falló por TIMEOUT en runtime:test, antigravity invalid_json; no se modificaron adaptadores. La carga en Vintta y las 10 galerías sí quedaron verificadas. Log guardado con la evidencia de carga.

## Recreación fiel y reemplazo del lote 1 · Codex, 2026-11-06

- Alcance vigente del dueño: UNA principal por cada uno de los diez productos del lote de producción 1; variantes aplazadas. Publicación y cambio de títulos con marca/modelo expresamente autorizados. Este estado sustituye la carga anterior de cinco fotos por producto.
- VERIFICADO: 10 principales nuevas y 10 títulos guardados en los productos exactos de ElTilicheroCR; diez fichas públicas comprobadas tras recargar, con una imagen 1080x1080 cada una. Se retiraron las galerías anteriores; archivos y URLs respaldados. Precio ₡999, stock 0, descripciones, estado y clasificación idénticos antes de guardar. Otros 30 productos sin editar.
- Fuentes nativas de catálogos exactos y ocho referencias oficiales de 1HORA (12.374.198 bytes), descargadas solo después del permiso del dueño. Lovely Baby 2623: pelo largo, vestido floral multicolor, variante inferior izquierda elegida explícitamente. GM201 reconstruido desde el artículo exacto; ya no se usa la imagen BT03. No atribuir Apple a 895B ni Pro 5S.
- Marcas documentadas: JBL Go 4, JBL Clip 5, 1HORA BOC062/BOC243/AUT119, Langsfit V11 Pro y Lovely Baby 2623. Títulos de los genéricos conservan solo modelo. No afirmar originalidad ni autenticidad independiente.
- Evidencia y comparador: imagenes/lote-1-fiel-v3/index.html; productos.json; indice-principales.csv; publicacion-vintta/resultado-final.json, verificacion-publica.json, resumen.csv y cuatro capturas. Principales en imagenes/<producto>/fiel-v3/01-principal.png; maestros 1254x1254 conservados. Visor de cuatro lotes actualizado.
- Revisión visual secuencial; corregidos control BOC243 y posición de auricular AUT119. SUPUESTO: detalle fino reconstruido por IA. NO SÉ: cotejo físico y autenticidad independiente. Tres variantes BOC062 anteriores al cambio de alcance archivadas y no publicadas. No continuar variaciones sin nuevo encargo.
- No hubo contactos, compras, cuentas, API de pago alternativa, push, PR ni merge. Los lotes 2, 3 y 4 no se modificaron.

- Registro maestro local JSON/CSV actualizado para los diez productos: título actual, ruta de principal, corrección aplicada y publicación verificada; otros treinta registros intactos. No se actualizaron documentos de Drive con este encargo.
- Control final de esta recreación: npm run check PASS (salida 0); log y qa-final.json en imagenes/lote-1-fiel-v3/. Comparador: 20 imágenes incrustadas íntegras por SHA256, visor de 40 productos en cuatro lotes. No se repitió prueba interactiva del visor en esta actualización; publicación de las diez fichas sí verificada en navegador.

## Lote 2 · diez principales fieles creadas · Codex, 2026-11-06

- Encargo: repetir el criterio final del lote 1, UNA principal por producto y sin variaciones adicionales. Se crearon TCR-030, 028, 008, 007, 002, 006, 034, 019, 031 y 032, en ese orden de ranking. NO se modificó ni subió nada en Vintta: petición actual de creación, publicación pendiente de indicación expresa.
- El dueño autorizó seis fotos oficiales de 1HORA (336.683 bytes) y pidió que la principal del control PS4 reúna los CINCO diseños del catálogo. No generar un PS5 liso por confundir productos de la misma página. La composición de cinco opciones no certifica un paquete de cinco unidades.
- VERIFICADO: diez principales PNG1080x1080, diez maestros1254x1254, archivos distintos; 61 referencias extraídas nativas y seis descargas autorizadas íntegras por SHA256. Revisión visual secuencial. Una primera versión KMP-171 con sello de originalidad en caja fue descartada; versión seleccionada solo micrófono, sin ese sello. No se llamó original a los productos.
- Diferencias: GAR152N del proveedor dice20W; foto web negra actual diceGaN20W. Se conserva revisión/rotulación del proveedor. Título propuesto KMP-171 neutro porque cable/inalámbrico no se determina por fotografía. Touchdayu figura en el maletín de156piezas; se muestra cerrado. Apple/Samsung según marca documentada y validación del dueño; autenticidad independiente NO SÉ.
- Archivos: imagenes/<slug>/fiel-v1/01-principal.png y maestro; informe/comparador en imagenes/lote-2-fiel-v1/index.html, productos.json, indice-principales.csv, generaciones.json y qa-final.json. Visor general de cuatro lotes actualizado. Registro maestro local JSON/CSV: diez registros de creación actualizados; nombres propuestos, sin cambiar los títulos publicados ni los otros treinta registros.
- SUPUESTO: detalle fino y estampados reconstruidos por IA. NOT_RUN: cotejo físico, revisión independiente, autenticidad e inventario actual. Sin contactos, compras, cuentas, API de pago alternativa, push, PR ni merge. Lotes3–4 sin producir.

- Control final lote2: npm run check PASS, salida0; log y qa-final.json en imagenes/lote-2-fiel-v1/. Comparador de20 imágenes íntegras por SHA256, cuatro lotes y40 productos. Se documentaron Touchdayu/Apple en marca_indicada según rotulación visible. Sin prueba interactiva nueva del visor ni cambios en Vintta.

## Lote2 publicado tras nueva auditoría de proveedor · Codex, 2026-11-06

- El dueño autorizó subir las imágenes del lote2 y exigió cotejarlas con los catálogos originales por duda sobre réplicas/Earbuds. VERIFICADO: diez principales y títulos guardados y comprobados en diez fichas públicas tras recarga, una foto1080x1080 cada una. Precio999, stock0, descripción, estado y clasificación conservados. Otros treinta productos sin editar.
- Cadena CSV→proveedor/SKU/página→PDF completo→imagen nativa cotejada para nueve productos; Touchdayu SKU37010248 confirmado en datos originales web de Canguro id4167 y su CSV. Consulta web actual no accesible, stock/surtido sin comprobar. Nueve páginas renderizadas en auditoria-previa-carga/.
- DADU DT055 Stereo Earbuds (DADU p12) y SE-ONE Smart TWS Earbuds Phone (INNOVACIÓN p35) son modelos distintos de TCR031/032, registrados desde MyTechnologyCR p51/52. No reemplazarlos por imágenes DADU solo por parecido. TCR034 proviene de MyTechnologyCR p57.
- Corrección material: los nombres propuestos Apple/Samsung no acreditaban fabricante. Se publicaron tipo AirPods3, tipo AirPods4 y tipo Galaxy Buds3 Pro. Tres recreaciones corregidas sin sus cajas, en fiel-v2/, versiones anteriores conservadas. Marca física SAMSUNG de la tapa se mantiene según foto. No se determinó autenticidad ni condición de réplica solo por imagen. TCR031/032/034 estaban sin URL de foto en panel; otros siete tenían una anterior respaldada.
- Evidencia: imagenes/lote-2-fiel-v1/publicacion-vintta/resultado-final.json, verificacion-publica.json, resumen.csv y cuatro capturas; auditoria-previa-carga/auditoria-catalogos.json; comparador y registro maestro actualizados. Revisión secuencial; sin cotejo físico ni revisor independiente. Sin compras, contactos, nuevas descargas, push, PR ni merge.

- Control final de publicación lote2: npm run check PASS (salida0). Log en imagenes/lote-2-fiel-v1/publicacion-vintta/npm-check-publicacion.log; qa-final.json actualizado. Comparador20 imágenes íntegras y enlaces a nueve páginas completas de los catálogos PDF; Canguro por SKU web archivado. No se repitió prueba interactiva del visor; diez fichas públicas sí verificadas tras recarga.

## Lotes3 y4 publicados · Codex, 2026-11-06

# Lotes 3 y 4 · veinte principales

VERIFICADO: veinte principales distintas, una por producto; maestros1254x1254, exportaciones1080x1080. Revisión visual secuencial de modelos, color y componentes frente a fuentes originales; no hay revisor independiente. Se usó imagegen integrado y dirección de fotografía de producto; sin API alternativa de pago ni agentes.

Referencias: imágenes nativas extraídas de PDF locales, páginas completas renderizadas para ubicación de modelos, y ocho fotos web archivadas de Canguro cotejadas con sus SKU y datos originales. Cuatro fotos externas descargadas con permiso expreso: CAB265, AUT123, DPA002 e iM.Master8054; total667.787bytes, SHA256 registrados. No se afirma acceso vigente al inventario de Canguro.

Diferencias materiales: AUT123 oficial actual tiene otra cabeza: se preservó la carcasa cilíndrica del proveedor y la foto web solo apoyó el conector. iM.Master8054 conserva la forma dragón documentada; se omite conteo de piezas porque proveedor646 y fabricante408 discrepan. Y9 es kit de cámara/reloj3en1; no se inventó un smartwatch genérico. FS2606 es el aro RGB con ventilador, no los modelos vecinos. Correa es un repuesto sin reloj. Control compatible PS5 y diadema tipo Max muestran nueve opciones de color cada uno, no un paquete de nueve. Carro MD807B muestra dos configuraciones de la misma unidad, no dos unidades.

SUPUESTO: detalle fino, textura, estampados y molde reconstruidos por IA, especialmente referencias pequeñas de Canguro y AUT123. NO SÉ: autenticidad, funciones técnicas anunciadas, conteo real, stock actual y coincidencia con unidad física. No se llama original a nada ni se acredita Apple/Sony como fabricantes por parecido. El comparador incluye imágenes para evitar depender de enlaces externos.

Estado: veinte principales y títulos PUBLICADOS Y VERIFICADOS en fichas públicas tras recarga. Otros campos conservados. Evidencias en publicacion-vintta/resultado-final.json y capturas.

Comprobación final: npm run check PASS (exit0). Registro maestro: veinte filas actualizadas, las otras veinte intactas. Visor general: cuarenta productos, diez por lote, ochenta imágenes incluidas; las veinte recreaciones nuevas coinciden por SHA256 con los PNG publicados. Seis capturas guardadas. Interacción del visor no repetida en esta actualización; estructura y archivos comprobados.

Las descripciones previas se conservaron: todavía pueden contener afirmaciones técnicas sin comprobar, incluido el conteo646 del robot. No se verificó ese conteo ni se corrigieron las descripciones dentro del encargo de foto y título.
