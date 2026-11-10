import csv, math, re, sys, json, html
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3]); csvout = Path(sys.argv[4])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
e = html.escape
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def img(x): f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + '" height=58>') if f else ''
def money(v): return '₡' + f"{int(v):,}".replace(',', ' ')
CATS = [('Juguetes y regalos para niños', r'TOY|JUGUETE|SCOOTER|DRONE|DRN|KIT DE DIBUJO|MU[ÑN]ECA|ROBOT|CARRO|SKATE|BIKE|TIRO|LANZADOR|BOLAS|BOLSO|TOCADOR|SET MARKET|BASKETBALL|PATINES|CAR '),
        ('Hogar y cuidado personal', r'DISPENSADOR|CEPILLO|REGLETA|LICUADORA|FREIDORA|PLANCHA|SECADOR|AFEITADORA|MASAJEADOR|HUMIDIFICADOR|VENTILADOR|LAMPARA|LÁMPARA|COCINA|HOGAR|AGUA'),
        ('Cámaras y seguridad', r'CAMARA|CÁMARA|DASH|TIMBRE'),
        ('Audio', r'AUDIF|AURICUL|PARLANTE|BOCINA|BASS|MICROF|DIADEMA|EARBUD'),
        ('Gaming', r'CONSOLA|CONTROL |GAMER|TECLADO|MAUSE|MOUSE|JOYSTICK'),
        ('Smartwatch y wearables', r'RELOJ|WATCH|SMART ?BAND'),
        ('Soportes, selfie y creadores', r'HOLDER|SOPORTE|SELFIE|TRIPODE|TRÍPODE|PALO DE SELFIE|\bARO\b|PANEL LUZ|PANEL DE LUZ|MJ\d\d|LJJ'),
        ('Cargadores, cables y energía', r'CARGADOR|CABLE|POWER ?BANK|BATERIA|BATERÍA|CUBO|ADAPTADOR|COMBO CARG'),
        ('Auto y luces LED', r'\bLED\b|\bAUTO\b|AROS|FARO|LUCES|KIT DE LUCES'),
        ('Computación y accesorios', r'LAPTOP|USB|HUB|BASE|WEBCAM|FUNDA|PROTECTOR|MEMORIA|LECTOR|MICRO ?SD')]
def cat(x):
    t = x['producto'][:45].upper()
    for n, rx in CATS:
        if re.search(rx, t): return n
    return None
QUOTA = {'Juguetes y regalos para niños': 14, 'Hogar y cuidado personal': 8, 'Cámaras y seguridad': 7, 'Audio': 12, 'Gaming': 6, 'Smartwatch y wearables': 4,
         'Soportes, selfie y creadores': 12, 'Cargadores, cables y energía': 12, 'Auto y luces LED': 5, 'Computación y accesorios': 6}
def num(v): return int(v) if v else None
def fam(x):
    t = x['producto']
    if x['proveedor'].startswith('Canguro'):
        t = t.split(' / ')[-1] if ' / ' in t else t
        w = re.findall(r'[A-ZÁÉÍÓÚÑ]{3,}', t.upper()); return 'C:' + (w[0] if w else t[:8])
    w = re.findall(r'[A-ZÁÉÍÓÚÑ]{3,}', t.upper()); return ' '.join(w[:2])
pool = defaultdict(list)
for x in rows:
    if x['proveedor'] == 'MyTechnologyCR' or k(x) in AGO or k(x) not in IMG: continue
    c = num(x['costo_mayorista_crc']) or num(x['precio_catalogo_sin_tipo_crc']); p = num(x['pvp_sugerido_proveedor_crc'])
    if not c or c > 30000: continue
    g = cat(x)
    if not g: continue
    L = int(math.ceil(max(c * 1.35, (p or 0) * 0.6) / 100.0) * 100)
    if L > 35000 or L < 1500: continue
    pool[g].append(dict(x=x, c=c, p=p, L=L, g=g, canguro=x['proveedor'].startswith('Canguro')))
sel = []
for g, q in QUOTA.items():
    seen = set(); L = sorted(pool[g], key=lambda r: abs(math.log(r['L'] / 9000.0)))
    n = 0
    for r in L:
        f = fam(r['x'])
        if f in seen: continue
        seen.add(f); sel.append(r); n += 1
        if n >= q: break
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.6pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:middle}td.n,th.n{text-align:right;white-space:nowrap}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:75px;object-fit:contain}</style>']
H.append(f'<h1>El Tilichero CR</h1><p><b>Plan de ventas ampliado: {len(sel)} productos de todo el catálogo</b> · 4 de noviembre de 2026</p>')
H.append('<div class=nota><b>Qué cambió.</b> Ya no filtro por marca, tipo ni rentabilidad. Tomé todo el catálogo de los tres proveedores (755 productos) y elegí los que mejor se venden por precio de impulso y regalo: sin sello AGOTADO, con foto y precio de lanzamiento entre ₡1 500 y ₡35 000. Se muestra una variante por tipo de producto; hay más variantes en el catálogo completo.</div>')
H.append('<div class=nota><b>Sobre «asegurar ventas».</b> Nadie puede garantizarlas, y no hay un ranking público de ventas de Costa Rica. Lo que sí hace más probable vender: <b>precio claramente bajo frente a lo que ya existe en el país</b> (ver abajo), entrega rápida (los importadores tardan de 8 a 14 días hábiles), productos que se entienden en un video de 5 segundos y muchas opciones para que cada visitante encuentre algo. Lo confirma vender, por eso el plan mide por producto.</div>')
H.append('<h2>Referencias de precio en Costa Rica (visto hoy, no son ventas)</h2><ul><li>Audífonos inalámbricos genéricos tipo AirPods en Mercado Libre Costa Rica: ₡7 500 a ₡10 000. Marcas conocidas: Xiaomi Redmi Buds 4 Lite ₡28 999; JBL Vibe Beam ₡31 999; Galaxy Buds3 Pro ₡115 000.</li><li>Yaxa Costa Rica (importación, entrega de 8 a 14 días hábiles): power bank de 6 000 mAh ₡25 877; soporte magnético de carro para iPhone ₡21 177.</li><li>Nuestros costos: soportes de celular desde ₡1 800, power bank de 10 000 mAh ₡11 500, audífonos inalámbricos desde ₡2 825 (costo mayorista).</li></ul><p class=sm>Fuentes: listados de Mercado Libre Costa Rica y Yaxa Costa Rica. Los precios cambian y no son precios de venta confirmados.</p>')
cur = None; csvrows = []
for g in QUOTA:
    L = [r for r in sel if r['g'] == g]
    if not L: continue
    H.append(f'<h2>{e(g)} · {len(L)}</h2><table><tr><th>Foto</th><th>Producto</th><th>Dónde</th><th class=n>Costo</th><th class=n>Lanzamiento</th><th class=n>Normal*</th></tr>')
    for r in L:
        x = r['x']; nm = x['producto'].split(' / ')[-1] if r['canguro'] and ' / ' in x['producto'] else x['producto']
        flag = ' <span class=sm>(precio Canguro: no confirmado si es mayorista)</span>' if r['canguro'] else ''
        H.append(f"<tr><td>{img(x)}</td><td>{e(nm[:75])}{flag}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td><td class=n>{money(r['c'])}</td><td class=n><b>{money(r['L'])}</b></td><td class=n>{money(r['p']) if r['p'] else '—'}</td></tr>")
        csvrows.append([g, x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto'], r['c'], r['L'], r['p'] or ''])
    H.append('</table>')
H.append('<p class=sm>*Precio sugerido por Techno Go (solo catálogo 1HORA). Lanzamiento = costo + 35 % como mínimo (o 60 % del precio sugerido si lo hay): propuesta, sin descontar comisión de Vintta ni envío.</p>')
H.append('<div class=pb></div><h2>Marcas y réplicas validadas por el dueño</h2><p>Los AirPods-style, Galaxy Buds-style, JBL-style, Pencil, control PS5 y los carros RC con licencia de MyTechnologyCR y Canguro entran en el catálogo, pero <b>no tienen costo publicado</b> (MyTechnologyCR no trae precios), así que no puedo ponerles precio de lanzamiento. En Mercado Libre Costa Rica los genéricos tipo AirPods están entre ₡7 500 y ₡10 000: ese es el techo de precio a vencer. Con la lista mayorista se agregan de inmediato.</p>')
H.append('<h2>Cómo se vende esto en 3 semanas</h2><ol><li><b>Semana 1:</b> publicar los ~30 más baratos (ganchos) con foto y precio de lanzamiento; un Reel de 5 segundos por tipo de producto.</li><li><b>Semana 2:</b> publicar el resto y armar 3 combos (por ejemplo, audífonos + soporte + cable).</li><li><b>Semana 3 (Black Friday, 27 de noviembre según fuentes internacionales; confirmar fecha en CR):</b> empujar lo que ya vendió y retirar lo que no se movió.</li></ol><p><b>Antes de publicar:</b> confirmar stock con el proveedor y fijar el precio mínimo con la comisión de Vintta y el envío (datos del dueño).</p>')
out.write_text(''.join(H), encoding='utf-8')
w = csv.writer(csvout.open('w', newline='', encoding='utf-8')); w.writerow(['categoria', 'proveedor', 'catalogo', 'pagina', 'codigo', 'producto', 'costo_crc', 'precio_lanzamiento_propuesto_crc', 'precio_normal_proveedor_crc']); w.writerows(csvrows)
print(len(sel), {g: len([r for r in sel if r['g'] == g]) for g in QUOTA})
