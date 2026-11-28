import csv, re, sys, json, html
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3]); csvout = Path(sys.argv[4])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
mycat = {(x['pagina'], x['producto']): x['categoria'] for x in csv.DictReader((P / 'mytechnologycr-indice.csv').open(encoding='utf-8'))}
nov = {}
for x in csv.DictReader((P / 'productos-riesgo-marca.csv').open(encoding='utf-8')):
    nov['|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])] = x['decision_sugerida']
e = html.escape
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def img(x, h): f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + f'" height={h}>') if f else ''
def num(v): return int(v) if v else None
# tipo -> (peso de demanda, señal de demanda)
SIG = {
 'audio_inal': (1.0, 'Audio inalámbrico lidera en la región (Colombia 2026); en Mercado Libre Costa Rica hay categorías propias de audífonos Bluetooth y «AirPods»'),
 'audio_cable': (.9, 'Chile, primer semestre de 2026: los audífonos con cable duplicaron ventas (indirecta)'),
 'parlante': (.85, 'Audio portátil: regalo fácil; categoría fuerte en la región (indirecta)'),
 'reloj': (.9, 'Relojes inteligentes entre lo más comprado en Colombia 2026 (indirecta)'),
 'power': (.9, 'Hay power banks en tiendas costarricenses (Yaxa, Mercado Libre CR): categoría con demanda local visible'),
 'soporte': (.85, 'Soportes magnéticos y de carro en listas de TikTok Shop 2026 y en tiendas de Costa Rica'),
 'aro': (.85, 'Aros de luz y micrófonos en listas de TikTok Shop Q2 2026 (blogs, sesgados)'),
 'mic': (.8, 'Micrófonos inalámbricos mini en listas de TikTok Shop 2026 (blogs, sesgados)'),
 'hogar': (.8, 'Dispensadores automáticos y gadgets de hogar en listas de TikTok 2026 (blogs, sesgados)'),
 'gaming': (.8, 'Accesorios gamer y consolas: demanda alta en Colombia 2026 (indirecta)'),
 'juguete': (.75, 'Temporada de Navidad (sin dato específico de Costa Rica)'),
 'camara': (.55, 'Sin señal propia; se elige por utilidad como regalo'),
 'cargador': (.7, 'Accesorio recurrente de celular (indirecta)'),
 'funda': (.7, 'Fundas y protección: venta recurrente por cada celular nuevo (indirecta)'),
 'otro': (.4, 'Sin señal específica'),
}
def tipo(x):
    t = x['producto'].upper()[:60]; pr = x['proveedor']
    if pr == 'MyTechnologyCR':
        c = mycat.get((x['pagina'], x['producto']), '')
        m = {'Audio': 'audio_inal', 'Cargadores': 'cargador', 'Cables': 'cargador', 'Fundas y protección': 'funda', 'Relojes': 'reloj', 'Soportes': 'soporte', 'Juguetes y movilidad': 'juguete', 'Creadores': 'mic', 'Hogar': 'hogar', 'Cámaras y seguridad': 'camara', 'Gaming': 'gaming', 'Power banks': 'power', 'Cuidado personal': 'hogar', 'Auto y moto': 'soporte'}
        tp = m.get(c, 'otro')
        if tp == 'audio_inal' and re.search(r'PARLANTE|BOCINA|SPEAKER|JBL', t): tp = 'parlante'
        return tp
    if pr.startswith('Canguro'): return 'juguete'
    if re.search(r'POWER ?BANK|BATERIA PORT|BATERÍA PORT', t): return 'power'
    if re.search(r'RELOJ|WATCH|SMART ?BAND', t) and not re.search(r'CARGADOR|CABLE|CORREA|PROTECTOR|FUNDA', t): return 'reloj'
    if re.search(r'DISPENSADOR|CEPILLO|REGLETA|LICUADORA|PLANCHA|SECADOR|AFEITADORA|HUMIDIFICADOR', t): return 'hogar'
    if re.search(r'PARLANTE|BOCINA|BASS|SPEAKER', t): return 'parlante'
    if re.search(r'MICROF', t) and not re.search(r'CABLE|AUXILIAR|AUDIF|AUDÍF', t): return 'mic'
    if re.search(r'\bARO\b|MJ\d\d|LJJ|PANEL DE LUZ|PANEL LUZ', t): return 'aro'
    if re.search(r'AUDIF|AURICUL|DIADEMA|EARBUD', t):
        return 'audio_cable' if re.search(r'3\.5|CABLE|TIPO ?-?C|CHUPON|ALAMBR', t) and not re.search(r'INALAM|BLUETOOTH|BT|TWS', t) else 'audio_inal'
    if re.search(r'HOLDER|SOPORTE|SELFIE|TRIPODE|TRÍPODE', t): return 'soporte'
    if re.search(r'CONSOLA|CONTROL |GAMER|TECLADO|MAUSE|MOUSE|JOYSTICK', t): return 'gaming'
    if re.search(r'CAMARA|CÁMARA|DASH|TIMBRE', t): return 'camara'
    if re.search(r'CARGADOR|CABLE|CUBO|ADAPTADOR', t): return 'cargador'
    return 'otro'
def impulso(x):
    c = num(x['costo_mayorista_crc']) or num(x['precio_catalogo_sin_tipo_crc'])
    if not c: return .6
    if x['proveedor'].startswith('Canguro'): return 1 if 6000 <= c <= 16000 else .8 if 3000 <= c <= 30000 else .5
    return 1 if c <= 5000 else .85 if c <= 12000 else .6 if c <= 20000 else .3
def fam(x):
    t = x['producto']
    if x['proveedor'].startswith('Canguro'):
        t = t.split(' / ')[-1] if ' / ' in t else t
    w = re.findall(r'[A-ZÁÉÍÓÚÑ]{3,}', t.upper())
    if x['proveedor'] == 'MyTechnologyCR': return tipo(x) + ':' + x['pagina']
    return (' '.join(w[:2]) if len(w) >= 2 else (x['codigo'] or t[:14]))
cand = []
for x in rows:
    kk = k(x)
    if kk in AGO or nov.get(kk, '').startswith('NO VENDER'): continue
    tp = tipo(x); w, sg = SIG[tp]
    sc = .5 * w + .25 * impulso(x) + .15 * (1 if tp not in ('otro', 'camara') else .6) + .10 * (1 if kk in IMG else 0)
    cand.append(dict(x=x, tp=tp, sc=sc, sg=sg))
quota = {'Techno Go': 18, 'MyTechnologyCR': 10, 'Canguro Panamá': 8}
win = []
for pv, q in quota.items():
    L = sorted([c for c in cand if c['x']['proveedor'] == pv], key=lambda c: -c['sc'])
    seen = set(); typ = defaultdict(int)
    for c in L:
        f = fam(c['x'])
        if f in seen or typ[c['tp']] >= (3 if pv != 'Canguro Panamá' else 8): continue
        seen.add(f); typ[c['tp']] += 1; win.append(c)
        if sum(1 for w2 in win if w2['x']['proveedor'] == pv) >= q: break
have = {c['tp'] for c in win if c['x']['proveedor'] == 'Techno Go'}
for t in ('aro', 'mic', 'hogar', 'camara'):
    if t not in have:
        L = sorted([c for c in cand if c['x']['proveedor'] == 'Techno Go' and c['tp'] == t], key=lambda c: -c['sc'])
        if L: win.insert(sum(1 for c in win if c['x']['proveedor'] == 'Techno Go'), L[0])
cnt = {p: sum(1 for c in win if c['x']['proveedor'] == p) for p in quota}
CATS = [('Juguetes y regalos', r'TOY|JUGUETE|SCOOTER|DRONE|DRN|KIT DE DIBUJO|MU[ÑN]ECA|ROBOT|CARRO|SKATE|BIKE|TIRO|LANZADOR|BOLAS|BOLSO|TOCADOR|SET MARKET|BASKETBALL|PATINES|CAR '),
        ('Hogar y cuidado personal', r'DISPENSADOR|CEPILLO|REGLETA|LICUADORA|FREIDORA|PLANCHA|SECADOR|AFEITADORA|MASAJEADOR|HUMIDIFICADOR|VENTILADOR|LAMPARA|LÁMPARA|COCINA|HOGAR|AGUA'),
        ('Cámaras y seguridad', r'CAMARA|CÁMARA|DASH|TIMBRE'),
        ('Audio', r'AUDIF|AURICUL|PARLANTE|BOCINA|BASS|MICROF|DIADEMA|EARBUD'),
        ('Gaming', r'CONSOLA|CONTROL |GAMER|TECLADO|MAUSE|MOUSE|JOYSTICK'),
        ('Smartwatch', r'RELOJ|WATCH|SMART ?BAND'),
        ('Soportes, selfie y luces', r'HOLDER|SOPORTE|SELFIE|TRIPODE|TRÍPODE|\bARO\b|PANEL LUZ|PANEL DE LUZ|MJ\d\d|LJJ|\bLED\b|LUCES'),
        ('Cargadores, cables y energía', r'CARGADOR|CABLE|POWER ?BANK|BATERIA|BATERÍA|CUBO|ADAPTADOR|COMBO CARG'),
        ('Computación y accesorios', r'LAPTOP|USB|HUB|BASE|WEBCAM|FUNDA|PROTECTOR|MEMORIA|LECTOR|MICRO ?SD')]
def cat(x):
    t = x['producto'][:45].upper()
    for n, rx in CATS:
        if re.search(rx, t): return n
    return 'Otros'
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.6pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:middle}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:120px;object-fit:contain}.g{color:#c4161c;font-weight:700}</style>']
H.append(f'<h1>El Tilichero CR</h1><p><b>Productos ganadores y catálogo de los 3 proveedores (sin precios)</b> · 4 de noviembre de 2026</p>')
H.append('<div class=nota><b>Cómo elegí los ganadores.</b> Puntaje con cuatro factores: demanda de ese tipo de producto (señales regionales y de tiendas costarricenses, ver cada fila), facilidad de compra por impulso según el costo mayorista (interno, no se muestra), si se entiende en un video corto y si hay foto. <b>No hay un ranking público de ventas de Costa Rica</b>: las señales son indirectas y «ganador» significa candidato prioritario para vender primero; el volumen real lo confirman las ventas. Sin precios, por indicación del dueño.</div>')
H.append('<div class=nota><b>Marcas y réplicas</b> incluidas por indicación del dueño (validadas por él; no las verifiqué de forma independiente). Los productos con sello AGOTADO y los 7 «originales con logo» sin factura están fuera.</div>')
H.append(f'<h2>Los {len(win)} ganadores: {cnt['Techno Go']} de Techno Go, {cnt['MyTechnologyCR']} de MyTechnologyCR, {cnt['Canguro Panamá']} de Canguro</h2><table><tr><th>#</th><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Señal de demanda</th></tr>')
for i, c in enumerate(win, 1):
    x = c['x']; nm = x['producto'].split(' / ')[-1] if x['proveedor'].startswith('Canguro') and ' / ' in x['producto'] else x['producto']
    h = 90 if x['proveedor'] == 'MyTechnologyCR' else 58
    H.append(f"<tr><td class=g>{i}</td><td>{img(x, h)}</td><td>{e(nm[:85])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td><td class=sm>{e(c['sg'])}</td></tr>")
H.append('</table>')
H.append('<div class=pb></div><h1 style="font-size:18pt">Catálogo de los tres proveedores</h1>')
byp = defaultdict(lambda: defaultdict(list)); total = 0
for x in rows:
    kk = k(x)
    if nov.get(kk, '').startswith('NO VENDER'): continue
    g = (mycat.get((x['pagina'], x['producto'])) if x['proveedor'] == 'MyTechnologyCR' else cat(x)) or 'Otros'
    if g == 'Portada': continue
    byp[x['proveedor']][g].append(x); total += 1
H.append(f'<p class=sm>{total} productos. Los AGOTADOS se muestran marcados. Techno Go: foto del PDF del proveedor (puede mostrar productos vecinos); MyTechnologyCR: página de su catálogo; Canguro: foto del producto.</p>')
for pv in ('Techno Go', 'MyTechnologyCR', 'Canguro Panamá'):
    H.append(f'<h1 style="font-size:16pt;margin-top:14px">{pv} · {sum(len(v) for v in byp[pv].values())} productos</h1>')
    for g, L in sorted(byp[pv].items(), key=lambda kv: -len(kv[1])):
        H.append(f'<h2>{e(g)} · {len(L)}</h2><table><tr><th>Foto</th><th>Producto</th><th>Catálogo / página / código</th></tr>')
        for x in L:
            nm = x['producto'].split(' / ')[-1] if pv.startswith('Canguro') and ' / ' in x['producto'] else x['producto']
            ag = ' <b style="color:#c4161c">AGOTADO</b>' if k(x) in AGO else ''
            h = 90 if pv == 'MyTechnologyCR' else 52
            H.append(f"<tr><td>{img(x, h)}</td><td>{e(nm[:90])}{ag}</td><td class=sm>{e(x['catalogo'][:16])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:14])}</td></tr>")
        H.append('</table>')
H.append('<p class=sm>Fuentes de las señales: WOM Chile (eldinamo.cl), Tiendanube Colombia 2026, listas de tendencias de TikTok Shop 2026 (blogs y agencias), listados de Mercado Libre Costa Rica y Yaxa Costa Rica. Confirmar stock con cada proveedor antes de publicar.</p>')
out.write_text(''.join(H), encoding='utf-8')
w = csv.writer(csvout.open('w', newline='', encoding='utf-8')); w.writerow(['ranking', 'proveedor', 'catalogo', 'pagina', 'codigo', 'producto', 'tipo', 'senal_de_demanda'])
for i, c in enumerate(win, 1):
    x = c['x']; w.writerow([i, x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto'], c['tp'], c['sg']])
print(len(win), total, {p: sum(len(v) for v in d.values()) for p, d in byp.items()})
