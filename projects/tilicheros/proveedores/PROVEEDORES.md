# El Tilichero CR · proveedores (incorporados 2026-11-04)

Estado: **VERIFICADO en fuente, sin pedidos ni stock confirmados.** Se leyeron las tres fuentes que entregó el dueño. No se contactó a ningún proveedor ni se publicó nada en Vintta o Instagram. Reemplaza como fuente de datos a la Master V3 (`../master-v3/`), cuyos costos y puntajes no tenían respaldo.

| Proveedor | Fuente | Qué contiene | Precios | Archivo en el proyecto |
|---|---|---|---|---|
| **MyTechnologyCR** («Mayorista de la tecnología») | `Catalogo_sin_precios.pdf` (Descargas, 128 MB, 154 páginas) | 151 fichas de producto: fundas, cargadores, cables, audio, relojes, soportes, creadores, cámaras, juguetes, hogar | **No trae precios**: hay que pedirlos por WhatsApp (7136 7615 / 7286 8940) | `mytechnologycr-indice.csv`: página, producto, categoría, riesgo de marca, imagen |
| **Canguro Panamá** | Catálogo privado qvix (enlace del dueño) | 75 productos: carros RC, scooters, drones, kits de dibujo, patines, lanzadores de gel | Un precio por producto, en colones (₡500–₡165 000). **NO SÉ** si es mayorista o de venta | `canguro-catalogo.csv` |
| **Techno Go** (@technogocr) | Carpeta de Drive «Catálogos PDF», 14 PDFs (≈260 MB) | 1HORA, TUQIN/VIDVIE y 12 marcas «ORIGINAL» (XO, ONIKUMA, DADU, FENGQI, HOPESTAR, JORTAN, KOOSDA, MIKUSO, UMIPRO, adaptadores, cargadores de laptop, innovación variada) | **Mayoreo con IVA + PVP sugerido** en 1HORA y TUQIN/VIDVIE; **«Precios mayoristas con IVA incluido»** (portada de cada PDF) en las marcas ORIGINAL | `technogo-1hora.csv` (162 SKU) y `technogo-marcas-original.csv` (367 fichas de 10 catálogos) |

**Todo junto:** `catalogo-proveedores-unificado.csv`, con 755 productos (529 con costo mayorista real, 162 con PVP sugerido, 43 de riesgo de marca ALTO y 58 MEDIO).

## 1. MyTechnologyCR
- **VERIFICADO:** el índice sale del texto del PDF (124 páginas) y de una revisión visual de las 29 páginas sin texto y de 16 títulos ambiguos.
- **Corrige a la Master V3:** el «ganador n.º 1» HK11 Ultra 3 está en la **página 152**, no en la 150. Las fotos de página de `master-v3/imagenes/mytechnologycr/` coinciden con la numeración del PDF.
- **Riesgo de marca (12 fichas ALTO):** el catálogo vende réplicas. La pág. 53 dice literalmente «AirPods Pro 3 Calidad Premium 1:1». También aparecen «AirPods 4», «AirPods 3.ª generación», EarPods con logo de Apple, «Galaxy Buds3 Pro» con logo de Samsung, «JBL Go 4 / Clip 5», «Control PS5» y «Pencil segunda». Otras 18 fichas (cargadores «SAM/IPH», memorias Kingston, Lightning) son riesgo MEDIO. No se anuncian como originales ni con el nombre de la marca (ver `../PROTOCOLO-AUTENTICIDAD-AIRPODS.md`).
- **Sin riesgo de marca y con buen potencial en video:** parlantes aibimy (págs. 111–116, marca propia), relojes Keqiwear KW88/KW89/KW93/KW95 (148–151), cámara 4K tipo gimbal (78), aro de luz (96), bombillo LED musical (95), hidrolavadora 48V (102), consola X50 (122), cámara instantánea infantil (132), scooters (124, 126).

## 2. Canguro Panamá
- 75 productos en 5 categorías: juguete (59), scooter (9), lanzador (4), gadgets (2), consolas (1).
- Llena el hueco de **juguetes, bebés y niños** que el dueño declaró y que hoy no tiene productos en Vintta: kits de dibujo (₡2 000–4 900), scooters infantiles (₡10 900–16 900), drone P30 con cámara (₡29 900), robots armables (₡16 500), carros RC a escala (₡26 900).
- **Riesgo:** «Transformer Bumblebee» y carros con nombres de Lamborghini, Maserati o McLaren. Hay que confirmar que tengan licencia oficial (muchos RC a escala la tienen) antes de usar esos nombres en anuncios.

## 3. Techno Go
| Catálogo | Leído | Productos | Margen sugerido por el proveedor |
|---|---|---|---|
| 1HORA | Completo (22 págs.) | 162 SKU, 147 modelos | 43 % a 86 %, mediana 55 % |
| TUQIN / VIDVIE | Completo (9 págs.) | 61 SKU | 50 % en los principales |
| XO ORIGINAL | 14 págs., resumen | 35 modelos | Precio único con IVA, ₡1 865 a ₡51 980 |
| ONIKUMA ORIGINAL | 12 págs., resumen | Audífonos gaming (T35, B3, G69…) | Precio único con IVA, ₡5 085 a ₡36 160 |
| INNOVACIÓN VARIADA | Completo (46 págs.) | 129 fichas | Solo costo mayorista |
| DADU | Completo (27 págs.) | 75 fichas | Solo costo mayorista |
| MIKUSO | Completo (16 págs.) | 34 fichas | Solo costo mayorista |
| ADAPTADORES · HOPESTAR · KOOSDA · CARGADORES LAPTOP · JORTAN · FENGQI · UMIPRO | Completos | 28 · 24 · 22 · 19 · 18 · 11 · 7 fichas | Solo costo mayorista |

**Cómo se extrajeron (2026-11-04):** los 10 PDFs se descargaron con permiso del dueño a una carpeta temporal fuera del repositorio. El texto se sacó con `pdftotext`; cada ficha termina en «(IVA incluido)» y el precio es el último monto con «₡» de la ficha. Las 367 fichas tienen precio; 113 no traen código de modelo (el modelo suele ir al inicio de la descripción). **Verificación:** se comparó la posición de precio y modelo con `pdftotext -layout` en INNOVACIÓN p. 27 (8 de 8 coinciden), DADU p. 19 (3 de 3) y KOOSDA p. 3 (2 de 2). No es una revisión ficha por ficha: antes de pedir, confirmar el precio con el proveedor.

**Todavía resumidos** (no se pidió descargarlos): XO, ONIKUMA y TUQIN/VIDVIE. Con permiso se completan con el mismo proceso.

Candidatos sin riesgo de marca de las marcas ORIGINAL (costo mayorista con IVA; el PVP lo define el dueño):

| Producto | Catálogo, página | Costo |
|---|---|---|
| Cámara Wi-Fi doble lente (fija + giratoria) JT-9695 / JT-9696 / JT-8292 | JORTAN p. 2, 6, 7 | ₡12 430–12 995 |
| Cámara Wi-Fi + Bluetooth JT-9680 | JORTAN p. 4 | ₡24 860 |
| Dash cam de 3 canales Y106 | INNOVACIÓN p. 42 | ₡15 820 |
| Parlantes BASS-30 / BASS-31 | INNOVACIÓN p. 32 | ₡23 730–24 295 |
| Reloj infantil 3 en 1 con cámara Y9 | INNOVACIÓN p. 6 | ₡22 600 |
| Kit de luces LED para creadores | INNOVACIÓN p. 27 | ₡20 340 |
| Aros de luz LJJ 33–56 cm | INNOVACIÓN p. 27 | ₡5 650–18 080 |
| Micrófono inalámbrico RGB KMP-171 | KOOSDA p. 9 | ₡15 255 |
| Kit trípode + luz + micrófono KSD-T50 | KOOSDA p. 6 | ₡12 995 |
| Base enfriadora para laptop 6 ventiladores NCP-786 | MIKUSO p. 7 | ₡15 255 |
| Kit teclado y mouse inalámbrico | MIKUSO p. 10, 15 | ₡10 170 |
| Control compatible PS4 «sin logo» | INNOVACIÓN p. 16 | ₡9 605 |
| Power bank 50 000 mAh con linterna CC58 | FENGQI p. 6 | ₡19 210 |

Comparación con Vintta (INFERIDO, sin confirmar que sea el mismo modelo): la «Cámara de seguridad WiFi doble lente» se vende allí a ₡28 900. Si es una JORTAN de ₡12 995, el margen bruto sería de ≈55 %.

Ojo: INNOVACIÓN p. 2 ofrece un «cargador Tipo-C a Lightning 35 W ORIGINAL CON LOGO» a ₡2 375. A ese costo no puede ser un Apple original: riesgo ALTO. El cargador de laptop «MAGSAFE 3» usa una marca de Apple: anunciarlo como «compatible», no como MagSafe.

Techno Go es el único proveedor con **costo y precio sugerido escritos**. Ejemplos (mayoreo → PVP sugerido):

| Producto | Código | Costo | PVP sugerido | Margen bruto |
|---|---|---|---|---|
| Dispensador de agua automático | DPA002B | ₡5 500 | ₡25 500 | 78 % |
| Cepillo de dientes sónico | CEP001B | ₡9 900 | ₡20 900 | 53 % |
| Batería portátil 10 000 mAh PD 22,5 W | GAR264N | ₡11 500 | ₡23 000 | 50 % |
| Batería portátil 10 000 mAh con 4 cables | GAR148N | ₡9 200 | ₡18 500 | 50 % |
| Diadema inalámbrica AUT250 | AUT250N | ₡10 300 | ₡22 000 | 53 % |
| Audífonos ANC AUT211 | AUT211N | ₡8 500 | ₡18 000 | 53 % |
| Bocina inalámbrica 20 W | BOC250N | ₡12 500 | ₡25 000 | 50 % |
| Regleta 10 enchufes + USB/C | MCT002N | ₡8 500 | ₡19 900 | 57 % |
| Diadema gamer cable/BT con micrófono (VIDVIE) | BBH2119 | ₡17 500 | ₡35 000 | 50 % |
| Smartwatch SW1624 (VIDVIE) | SW1624 | ₡13 900 | ₡27 900 | 50 % |
| Cargador inalámbrico 3 en 1 (TUQIN) | QWC01 | ₡10 900 | ₡21 800 | 50 % |

El margen bruto no descuenta envío, comisión de Vintta (NO SÉ si cobra), garantía ni devoluciones. VIDVIE vende audífonos «estilo AirPods 4 / Pro / 2»: riesgo ALTO si se anuncian con ese nombre.

## 4. Cruce con lo publicado en Vintta (INFERIDO por nombre y precio, sin factura)
| En Vintta hoy | Precio | Probable origen | Riesgo |
|---|---|---|---|
| Audífonos AirBuds Pro 3 | ₡14 900 | MyTechnologyCR pág. 53 («AirPods Pro 3 1:1») | ALTO |
| Apple Pencil (2.ª generación) | ₡19 900 | MyTechnologyCR pág. 107 («Pencil segunda») | ALTO: el nombre «Apple Pencil» no puede usarse si no es original |
| Batería inalámbrica para iPhone | ₡14 900 | MyTechnologyCR pág. 73 (Power bank MagSafe) | MEDIO a ALTO si lleva logo de Apple |
| Mando DualSense PS5 «ORIGINAL» | ₡35 900 | MyTechnologyCR pág. 121 («Control PS5») | ALTO: «ORIGINAL» solo con factura de Sony o distribuidor |
| Cable y cargador Samsung 45 W | ₡3 900 / ₡5 900 | MyTechnologyCR págs. 33 y 41 | MEDIO: precio muy bajo para original |

Recomendación: cambiar esos títulos a nombres genéricos («Audífonos inalámbricos con estuche», «Lápiz óptico para iPad», «Control inalámbrico compatible con PS5») o retirarlos hasta tener factura. Lo decide el dueño; Claude no edita Vintta sin aprobación.

## 5. Candidatos a productos estrella con margen calculable
Criterios (`product-winner-scorecard`): costo conocido, sin riesgo de marca, demostrable en video, ticket ₡15 000–35 000. **Siguen siendo potenciales**: falta confirmar stock con el proveedor y probar la demanda.

1. **Dispensador de agua automático** (Techno Go, ₡5 500 → ₡25 500): demostración en 3 segundos.
2. **Batería portátil 10 000 mAh con 4 cables** (₡9 200 → ₡18 500): resuelve el «¿me prestás cargador?».
3. **Diadema gamer con micrófono VIDVIE** (₡17 500 → ₡35 000): encaja con gaming.
4. **Bocina 20 W** (₡12 500 → ₡25 000) o **parlantes aibimy RGB** (MyTechnologyCR, precio por pedir): luces y prueba de agua.
5. **Smartwatch VIDVIE SW1624** (₡13 900 → ₡27 900) o **Keqiwear KW93 Max con audífonos** (MyTechnologyCR): combo regalo.
6. **Cepillo dental sónico** (₡9 900 → ₡20 900): categoría hogar, poca competencia en el feed.
7. **Drone P30 con cámara** (Canguro, ₡29 900 de catálogo): necesita saber el costo real.
8. **Kits de dibujo infantiles** (Canguro, ₡2 000–4 900): abre la línea niños con ticket bajo.

## 6. Pendientes
| Falta | Quién | Para qué |
|---|---|---|
| Permiso para descargar XO, ONIKUMA y TUQIN/VIDVIE | Dueño | Completar los 3 catálogos de Techno Go que siguen resumidos |
| PVP de las marcas ORIGINAL | Dueño | Esos catálogos traen solo el costo |
| Lista de precios de MyTechnologyCR | Dueño (pedirla al proveedor) | Calcular margen de 151 productos |
| Confirmar si el precio de Canguro es mayorista | Dueño | Saber el margen real |
| Comisión y costos de Vintta para el vendedor | Dueño | Margen neto |
| Facturas de los productos con marca en Vintta | Dueño | Mantener o renombrar esas publicaciones |

## 7. Productos con riesgo de marca (agregados 2026-11-04)

Los 101 productos con riesgo ALTO o MEDIO están en `productos-riesgo-marca.csv` con una **decisión sugerida** (clasificación automática por palabras clave, sin revisar ficha por ficha). Siguen en el catálogo unificado.

| Decisión sugerida | Productos | Qué significa |
|---|---|---|
| Vender como compatible, sin nombre ni logo de marca | 45 | Cables, cargadores y soportes «para iPhone/PS4». Se listan como «compatible con…», sin usar «Apple», «original» ni el logo |
| Revisar | 17 + 16 | 16 son falsos positivos probables (mouse «estilo ergonómico»). Los otros 17 mencionan una marca solo por compatibilidad |
| NO VENDER: réplica | 16 | Audífonos «estilo AirPods/Galaxy Buds», parlantes «estilo JBL», Pencil, control «estilo PS5». Imitan marcas registradas |
| NO VENDER sin factura | 7 | «Original con logo» a ₡2 095–4 520 (cubos, cables y EarPods): a ese precio no son originales de Apple |

**Límite:** vender réplicas con el nombre o el logo de otra marca puede implicar infracción de marca registrada y retiro del anuncio o la cuenta en Vintta e Instagram. La decisión final es del dueño; no es asesoría legal (`[REVISIÓN PROFESIONAL]`). No preparo fichas de publicación para los grupos «NO VENDER».
