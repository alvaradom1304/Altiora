import csv, re, sys, json, html, statistics
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
nov = {'|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']]): x['decision_sugerida'] for x in csv.DictReader((P / 'productos-riesgo-marca.csv').open(encoding='utf-8'))}
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def img(x, h=70):
    f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + f'" height={h}>') if f else ''
e = html.escape
def money(v): return '' if v in ('', None) else '₡' + f"{int(v):,}".replace(',', ' ')
CATS = [('Hogar y cuidado personal', r'DISPENSADOR|CEPILLO|REGLETA|LICUADORA|FREIDORA|PLANCHA|SECADOR|AFEITADORA|MASAJEADOR|HUMIDIFICADOR|VENTILADOR|LAMPARA|LÁMPARA|COCINA|HOGAR|AGUA|MASCOTA'),
        ('Cámaras y seguridad', r'CAMARA|CÁMARA|DASH|TIMBRE'),
        ('Cargadores, cables y energía', r'CARGADOR|CABLE|POWER ?BANK|BATERIA|BATERÍA|CUBO|ADAPTADOR|COMBO CARG'),
        ('Audio', r'AUDIF|AURICUL|PARLANTE|BOCINA|BASS|MICROF|DIADEMA'),
        ('Gaming', r'CONSOLA|CONTROL |GAMER|TECLADO|MAUSE|MOUSE'),
        ('Smartwatch', r'RELOJ|WATCH|SMART ?BAND'),
        ('Auto y luces LED', r'\bLED\b|\bAUTO\b|AROS|FARO|LUCES'),
        ('Computación y accesorios', r'LAPTOP|USB|HUB|SOPORTE|BASE|WEBCAM|FUNDA|PROTECTOR|MEMORIA|TRIPODE|TRÍPODE')]
def cat(x):
    t = (x['producto'] + ' ' + x['catalogo']).upper()
    for n, rx in CATS:
        if re.search(rx, t): return n
    return 'Otros'
DEMO = {'Cámaras y seguridad': 1, 'Audio': 1, 'Gaming': 1, 'Auto y luces LED': 1, 'Smartwatch': 1, 'Hogar y cuidado personal': .9, 'Cargadores, cables y energía': .7, 'Computación y accesorios': .7, 'Otros': .5}
def num(v): return int(v) if v else None
pool = []
for x in rows:
    c, p = num(x['costo_mayorista_crc']), num(x['pvp_sugerido_proveedor_crc'])
    if not (c and p) or k(x) in AGO: continue
    d = nov.get(k(x), '')
    if d.startswith('NO VENDER'): continue
    m = p - c; mp = m / p; tk = 1 if 15000 <= p <= 35000 else (.6 if 8000 <= p < 15000 else .3)
    sc = .45 * min(mp / .6, 1) + .30 * min(m / 15000, 1) + .15 * tk + .10 * DEMO.get(cat(x), .5)
    pool.append(dict(x=x, c=c, p=p, m=m, mp=mp, sc=sc, cat=cat(x), d=d))
pool.sort(key=lambda r: -r['sc'])
seen = set(); top = []
for r in pool:
    fam = ' '.join(re.sub(r'[^A-Z0-9 ]', '', r['x']['producto'].upper()).split()[:3])
    if fam in seen or r['mp'] < .5: continue
    seen.add(fam); top.append(r)
    if len(top) == 20: break
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:13pt;margin:16px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.8pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:4px 5px;vertical-align:middle}td.n,th.n{text-align:right;white-space:nowrap}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:90px;object-fit:contain}.f{color:#a05a00;font-size:7.5pt}.card{display:inline-block;width:31%;vertical-align:top;border:1px solid #ddd;padding:6px;margin:0 1% 8px 0;break-inside:avoid;box-sizing:border-box}.card b{font-size:9pt}.big{font-size:20pt;font-weight:700;color:#c4161c}</style>']
H.append('<h1>El Tilichero CR</h1><p><b>Análisis y catálogo de productos ganadores</b> · 4 de noviembre de 2026</p>')
H.append('<div class=nota><b>Qué es y qué no es.</b> Es un ranking de <b>potencial comercial</b> con los datos que tenemos: costo mayorista real y precio de venta sugerido de Techno Go (catálogo 1HORA, octubre 2026), disponibilidad (sello AGOTADO) y facilidad de mostrar el producto en video. <b>No hay datos de demanda del mercado ni ventas propias de estos productos</b>: «ganador» significa «candidato prioritario para probar», no venta garantizada. El margen no descuenta envío, comisión de Vintta, publicidad ni devoluciones.</div>')
H.append('<div class=nota><b>Productos de marca/réplica.</b> Por indicación del dueño, los productos antes marcados como «no vender: réplica de marca registrada» se tratan como validados para la venta. Esa validación no la he comprobado de forma independiente; el riesgo de reclamo de marca o de retiro del anuncio por parte de las plataformas lo asume el negocio. Ver la sección 3: faltan sus costos para calcular margen.</div>')
H.append('<h2>1. Resumen del análisis</h2>')
a = [r for r in pool]
med = statistics.median(r['mp'] for r in a)
H.append(f'<p>Productos con costo y precio sugerido, disponibles y vendibles: <b>{len(a)}</b>. Margen mediano: <b>{med:.0%}</b>. {sum(1 for r in a if r["mp"]>=.5)} tienen margen ≥ 50 %. Hay {len(AGO)} productos del proveedor con sello AGOTADO, excluidos del ranking.</p>')
H.append('<table><tr><th>Categoría</th><th class=n>Productos</th><th class=n>Margen mediano</th><th class=n>Precio sugerido mediano</th><th class=n>Margen ₡ mediano</th></tr>')
bycat = defaultdict(list)
for r in a: bycat[r['cat']].append(r)
for n, L in sorted(bycat.items(), key=lambda kv: -statistics.median(r['m'] for r in kv[1])):
    H.append(f"<tr><td>{e(n)}</td><td class=n>{len(L)}</td><td class=n>{statistics.median(r['mp'] for r in L):.0%}</td><td class=n>{money(statistics.median(r['p'] for r in L))}</td><td class=n>{money(statistics.median(r['m'] for r in L))}</td></tr>")
H.append('</table><p class=sm>Lectura: las categorías con mayor margen en colones por unidad son las que más conviene probar primero, porque cada venta deja más para cubrir envío y publicidad.</p>')
H.append('<h2>2. Los 20 productos ganadores (candidatos prioritarios)</h2><table><tr><th>#</th><th>Foto</th><th>Producto</th><th>Código</th><th class=n>Costo</th><th class=n>PVP sug.</th><th class=n>Margen</th><th class=n>%</th><th>Categoría</th></tr>')
for i, r in enumerate(top, 1):
    x = r['x']
    H.append(f"<tr><td><b>{i}</b></td><td>{img(x)}</td><td>{e(x['producto'][:80])}</td><td>{e(x['codigo'])}</td><td class=n>{money(r['c'])}</td><td class=n>{money(r['p'])}</td><td class=n>{money(r['m'])}</td><td class=n>{r['mp']:.0%}</td><td>{e(r['cat'])}</td></tr>")
H.append('</table><p class=sm>Puntaje: 45 % margen porcentual, 30 % margen en colones, 15 % precio entre ₡15 000 y 35 000, 10 % facilidad de demostrarlo en video. Los pesos son un criterio de trabajo, no una fórmula validada. Se muestra una variante por familia de producto (se omiten colores).</p>')
H.append('<div class=pb></div><h2>3. Marcas y réplicas validadas por el dueño: falta el costo</h2><div class=nota>MyTechnologyCR no publica precios en su catálogo, por eso no se puede calcular el margen. Los precios de venta son los que ya tiene el negocio en Vintta (cruce inferido por nombre, sin factura). <b>Siguiente paso:</b> pedir a MyTechnologyCR la lista de precios mayoristas.</div>')
vint = {'51': None, '52': None, '53': ('AirBuds Pro 3', 14900), '107': ('Pencil 2.ª gen.', 19900), '121': ('Control PS5', 35900)}
H.append('<table><tr><th>Foto</th><th>Producto</th><th>Proveedor / página</th><th class=n>Costo</th><th class=n>Precio en Vintta hoy</th></tr>')
for x in rows:
    d = nov.get(k(x), '')
    if d.startswith('VENDER (validado'):
        v = vint.get(x['pagina']) if x['proveedor'] == 'MyTechnologyCR' else None
        H.append(f"<tr><td>{img(x)}</td><td>{e(x['producto'][:80])}</td><td>{e(x['proveedor'])} p.{x['pagina'] or ''}{(' · '+e(x['codigo'])) if x['codigo'] else ''}</td><td class=n>{money(x['costo_mayorista_crc']) or 'sin precio'}</td><td class=n>{money(v[1]) if v else ''}</td></tr>")
H.append('</table><p class=sm>Referencia: el control PS5 «sin logo» de Techno Go cuesta ₡29 380 al mayoreo y Vintta lo vende a ₡35 900 (margen bruto cercano al 18 %, si fuera el mismo producto; sin confirmar). Los carros RC de Canguro (₡26 900) no indican si el precio es mayorista.</p>')
H.append('<h2>4. Cómo validar los ganadores sin comprar mucho stock</h2><ol><li>Elegir 8–10 de la lista (mezclar categorías) y confirmar stock y garantía con Techno Go.</li><li>Publicar cada uno en Vintta y grabar un video corto de demostración; el presupuesto de la prueba lo fija el dueño.</li><li>Medir por producto: visitas, consultas y pedidos. Mantener los que vendan y retirar los demás.</li><li>Con los costos de MyTechnologyCR, repetir este análisis para los productos de marca.</li></ol><p class=sm>Fuentes: catálogos de Techno Go (PDF, octubre 2026), MyTechnologyCR y Canguro Panamá; sellos AGOTADO detectados de forma automática (lista posiblemente incompleta). Fotos: del PDF del proveedor.</p>')
out.write_text(''.join(H), encoding='utf-8')
print(len(a), f'{med:.2f}', len(top), [(r['x']['producto'][:25], r['m']) for r in top[:4]])
