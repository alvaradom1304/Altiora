import csv, re, sys, html
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); import json; T = Path(sys.argv[3])
IMG = json.load((T/'thumbs'/'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T/'agotados.json').open(encoding='utf-8')))
def k(x): return '|'.join([x['proveedor'],x['catalogo'],x['pagina'],x['codigo'],x['producto']])
def img(x):
    f = IMG.get(k(x)); return ('<img src="file:///'+f.replace(chr(92),'/')+'" height=52>') if f else ''
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
nov = {}
for x in csv.DictReader((P / 'productos-riesgo-marca.csv').open(encoding='utf-8')):
    nov[(x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto'])] = x['decision_sugerida']
CATS = [('Hogar, cocina y cuidado personal', r'DISPENSADOR|CEPILLO|REGLETA|LICUADORA|FREIDORA|PLANCHA|SECADOR|AFEITADORA|MASAJEADOR|HUMIDIFICADOR|VENTILADOR|LAMPARA|LÁMPARA|COCINA|HOGAR|BASCULA|BÁSCULA|TERMO|CAFE|CAFÉ|AGUA|MASCOTA|PERRO|GATO'),
        ('Cámaras y seguridad', r'CAMARA|CÁMARA|DASH|CCTV|VIGILANCIA|TIMBRE'),
        ('Cargadores, cables y energía', r'CARGADOR|CABLE|POWER ?BANK|BATERIA|BATERÍA|CUBO|ADAPTADOR|OTG|INVERSOR|FUENTE DE|COMBO CARG'),
        ('Audio y audífonos', r'AUDIF|AURICUL|PARLANTE|BOCINA|BASS|MICROF|SPEAKER|EARBUD|HEADSET|DIADEMA|SOUNDBAR'),
        ('Gaming y consolas', r'CONSOLA|CONTROL |GAMER|GAMING|JOYSTICK|VIDEOJUEGO|R36|TECLADO|MAUSE|MOUSE'),
        ('Smartwatch y wearables', r'RELOJ|WATCH|SMART ?BAND|PULSERA'),
        ('Auto y luces LED', r'LED|AUTO|AROS|FARO|LUCES|LUZ '),
        ('Juguetes y niños', r'JUGUETE|TOY|SCOOTER|DRONE|DRN|BOLSO|KIT DE DIBUJO|MU[ÑN]ECA|ROBOT|CARRO|SKATE|BIKE|TIRO|LANZADOR|BOLAS|CAR '),
        ('Computación y accesorios', r'LAPTOP|USB|HUB|SOPORTE|BASE|WEBCAM|FUNDA|PROTECTOR|MEMORIA|LECTOR|TABLET|TRIPODE|TRÍPODE')]
def cat(x):
    t = (x['producto'] + ' ' + x['catalogo']).upper()
    for n, rx in CATS:
        if re.search(rx, t): return n
    return 'Otros / sin clasificar'
def money(v):
    return '' if v in ('', None) else '₡' + f"{int(float(v)):,}".replace(',', ' ')
keep = defaultdict(list); excl = []
for x in rows:
    d = nov.get((x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']), '')
    if d.startswith('NO VENDER'):
        excl.append((x, d)); continue
    x['_d'] = d; keep[cat(x)].append(x)
def cost(x): return int(x['costo_mayorista_crc']) if x['costo_mayorista_crc'] else None
def pvp(x): return int(x['pvp_sugerido_proveedor_crc']) if x['pvp_sugerido_proveedor_crc'] else None
cand = [x for c in keep.values() for x in c if cost(x) and pvp(x) and not x['riesgo_marca'] and not x['_d']]
for x in cand:
    x['_m'] = pvp(x) - cost(x); x['_p'] = (pvp(x) - cost(x)) / pvp(x)
cand = [x for x in cand if x['_p'] >= 0.5 and x['_m'] >= 2500]
cand.sort(key=lambda x: -x['_m']); top = cand[:15]
e = html.escape
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:13pt;margin:18px 0 6px;break-after:avoid}h3{color:#c4161c}table{width:100%;border-collapse:collapse;font-size:8.5pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:top}img{max-width:90px;object-fit:contain}td.n,th.n{text-align:right;white-space:nowrap}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}.f{color:#a05a00;font-size:7.5pt}</style>']
tot = sum(len(v) for v in keep.values())
H.append(f'<h1>El Tilichero CR</h1><p><b>Catálogo de productos y candidatos a ganadores</b> · preparado el 4 de noviembre de 2026</p><div class=nota><b>Léelo así.</b> Son {tot} productos de 3 proveedores (Techno Go, MyTechnologyCR, Canguro Panamá), agrupados por categoría. Los precios de Techno Go son <b>mayoristas con IVA incluido, octubre 2026</b> (según el PDF del proveedor). MyTechnologyCR no trae precios. En Canguro no está confirmado si el precio es mayorista. Confirma precio y existencias con el proveedor antes de pedir.</div>')
H.append('<div class=nota><b>Sobre los «ganadores».</b> No hay un estudio de mercado ni de demanda verificado: lo que sigue es una <b>preselección por margen</b> (precio de venta sugerido por el proveedor frente al costo) y por <b>ausencia de riesgo de marca</b>. Hay que validarla con pruebas reales de venta (anuncio pequeño, historias o Reel) antes de comprar stock.</div>')
H.append('<h2>Candidatos a ganadores (preselección por margen)</h2><table><tr><th>Foto</th><th>Producto</th><th>Código</th><th class=n>Costo</th><th class=n>PVP sugerido</th><th class=n>Margen ₡</th><th class=n>Margen %</th><th>Categoría</th></tr>')
for x in top:
    H.append(f"<tr><td>{img(x)}</td><td>{e(x['producto'][:90])}</td><td>{e(x['codigo'])}</td><td class=n>{money(x['costo_mayorista_crc'])}</td><td class=n>{money(x['pvp_sugerido_proveedor_crc'])}</td><td class=n>{money(x['_m'])}</td><td class=n>{x['_p']:.0%}</td><td>{e(cat(x))}</td></tr>")
H.append('</table><p class=sm>Criterio: costo y PVP del mismo proveedor (Techno Go, catálogo 1HORA), sin riesgo de marca, margen ≥ 50 % y ≥ ₡2 500 por unidad, ordenados por margen en colones. El margen no descuenta envío, comisión de Vintta, publicidad ni devoluciones.</p>')
H.append('<h3>Otros candidatos sin riesgo de marca (solo costo; el PVP lo fija el dueño)</h3><table><tr><th>Foto</th><th>Producto</th><th class=n>Costo</th><th>Dónde</th></tr>')
def find(cat, pag, cod):
    for r in rows:
        if r['catalogo'] == cat and r['pagina'] == pag and cod in (r['codigo'] + ' ' + r['producto']): return r
OT = [('Cámaras Wi-Fi doble lente JORTAN JT-9695', '₡12 995', 'JORTAN p. 2', ('JORTAN', '2', 'JT-9695')), ('Cámara Wi-Fi doble lente JORTAN JT-8292', '₡12 430', 'JORTAN p. 6', ('JORTAN', '6', 'JT-8292')), ('Cámara Wi-Fi doble lente JORTAN JT-9696', '₡12 995', 'JORTAN p. 7', ('JORTAN', '7', 'JT-9696')), ('Cámara JORTAN JT-9680', '₡24 860', 'JORTAN p. 4', ('JORTAN', '4', 'JT-9680')), ('Dash cam 3 canales Y106 (AGOTADA en el catálogo)', '₡15 820', 'INNOVACIÓN p. 42', ('INNOVACION', '42', 'Y106')), ('Parlante BASS-31', '₡23 730', 'INNOVACIÓN p. 32', ('INNOVACION', '32', 'BASS-31')), ('Parlante BASS-30', '₡24 295', 'INNOVACIÓN p. 32', ('INNOVACION', '32', 'BASS-30')), ('Reloj infantil Y9', '₡22 600', 'INNOVACIÓN p. 6', ('INNOVACION', '6', '001957')), ('Kit de luces LED panel', '₡20 340', 'INNOVACIÓN p. 27', ('INNOVACION', '27', 'KIT DE LUCES')), ('Aro LED LJJ-45', '₡10 170', 'INNOVACIÓN p. 27', ('INNOVACION', '27', 'LJJ-45')), ('Micrófono KMP-171', '₡15 255', 'KOOSDA p. 9', ('KOOSDA', '9', 'KMP-171')), ('Trípode de grabación KSD-T50', '₡12 995', 'KOOSDA p. 6', ('KOOSDA', '6', 'KSD-T50')), ('Base enfriadora laptop NCP-786', '₡15 255', 'MIKUSO p. 7', ('MIKUSO', '7', 'NCP-786')), ('Kit teclado y mouse KN-C029', '₡10 170', 'MIKUSO p. 15', ('MIKUSO', '15', 'KB-C029')), ('Control compatible PS4 «sin logo»', '₡9 605', 'INNOVACIÓN p. 16', ('INNOVACION', '16', 'CONTROL PS4')), ('Power bank CC58 50 000 mAh', '₡19 210', 'FENGQI p. 6', ('FENGQI', '6', 'CC58'))]
for t, c, w, ref in OT:
    r = find(*ref)
    H.append(f'<tr><td>{img(r) if r else ""}</td><td>{t}</td><td class=n>{c}</td><td>Techno Go · {w}</td></tr>')
H.append('</table><p class=sm>La cámara de doble lente de Vintta está a ₡28 900. Si fuera el mismo modelo (sin confirmar), el margen rondaría el 55 %.</p>')
H.append('<div class=nota><b>Fotos.</b> Canguro y Techno Go 1HORA: foto del producto. MyTechnologyCR: página de su catálogo. Techno Go (marcas): imagen más cercana al producto en el PDF del proveedor; puede ser una tira o mostrar productos vecinos, confirma siempre con el código. Sin foto: unos 18 productos (cargadores de laptop y algunos adaptadores). <b>AGOTADO</b>: sello visto en el catálogo del proveedor, detectado de forma automática (la lista puede no ser completa); confirma el stock antes de pedir.</div><div class=pb></div><h1 style="font-size:18pt">Catálogo completo por categoría</h1><p class=sm>«Compatible» = mencionar la marca solo como compatibilidad, sin su nombre ni logo en la imagen o el título.</p>')
order = [n for n, _ in CATS] + ['Otros / sin clasificar']
for n in order:
    L = keep.get(n)
    if not L: continue
    H.append(f'<h2>{e(n)} · {len(L)} productos</h2><table><tr><th>Foto</th><th>Producto</th><th>Proveedor / catálogo</th><th class=n>Costo</th><th class=n>PVP prov.</th><th class=n>Otro precio</th></tr>')
    L.sort(key=lambda x: (cost(x) is None, cost(x) or 0))
    for x in L:
        ago = ' <span class=f style="color:#c4161c"><b>AGOTADO en el catálogo</b></span>' if k(x) in AGO else ''
        flag = ago + ((' <span class=f>⚠ ' + ('validado por el dueño' if x['_d'].startswith('VENDER (validado') else 'compatible' if x['_d'].startswith('VENDER') else 'revisar marca') + '</span>') if x['_d'] else '')
        pg = (' p.' + x['pagina']) if x['pagina'] else ''
        H.append(f"<tr><td>{img(x)}</td><td>{e(x['producto'][:110])}{flag}</td><td>{e(x['proveedor'])} · {e(x['catalogo'][:18])}{pg}</td><td class=n>{money(x['costo_mayorista_crc'])}</td><td class=n>{money(x['pvp_sugerido_proveedor_crc'])}</td><td class=n>{money(x['precio_catalogo_sin_tipo_crc'])}</td></tr>")
    H.append('</table>')
H.append(f'<div class=pb></div><h2>Excluidos del catálogo: {len(excl)} productos con riesgo de marca</h2><div class=nota>Réplicas de marcas registradas (AirPods, Galaxy Buds, JBL, Apple Pencil, PS5) y «originales con logo» a precios incompatibles con un original. No se recomienda venderlos; el dueño decide y conviene revisión legal.</div><table><tr><th>Foto</th><th>Producto</th><th>Proveedor</th><th class=n>Costo</th><th>Motivo</th></tr>')
for x, d in excl:
    H.append(f"<tr><td>{img(x)}</td><td>{e(x['producto'][:100])}</td><td>{e(x['proveedor'])}</td><td class=n>{money(x['costo_mayorista_crc'])}</td><td>{e(d.replace('NO VENDER', 'No vender'))}</td></tr>")
H.append('</table><p class=sm>Clasificación por categoría y riesgo automática, por palabras clave; no revisada ficha por ficha. Fuente: catálogos de los proveedores (PDF y catálogo en línea).</p>')
out.write_text(''.join(H), encoding='utf-8')
print(tot, len(excl), len(cand), [(x['producto'][:30], x['_m']) for x in top[:5]])
print({n: len(v) for n, v in keep.items()})
