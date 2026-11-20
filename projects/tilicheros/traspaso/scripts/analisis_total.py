import csv, re, sys, json, html, statistics
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3]); csvout = Path(sys.argv[4])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
mycat = {(x['pagina'], x['producto']): x['categoria'] for x in csv.DictReader((P / 'mytechnologycr-indice.csv').open(encoding='utf-8'))}
marca = {}
for x in csv.DictReader((P / 'productos-riesgo-marca.csv').open(encoding='utf-8')):
    marca['|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])] = x['decision_sugerida']
e = html.escape
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def img(x, h): f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + f'" height={h}>') if f else ''
def num(v): return int(v) if v else None
SIG = {
 'earpods': (1.0, 'Chile 1.er semestre 2026: Apple EarPods con cable fueron los audífonos más vendidos (WOM); los audífonos con cable duplicaron ventas'),
 'airpods': (.95, 'Audio inalámbrico lidera la región (Colombia 2026); Mercado Libre Costa Rica tiene categoría «Auricular Airpod»'),
 'audio_inal': (1.0, 'Audio inalámbrico lidera la región (Colombia 2026); Mercado Libre Costa Rica tiene categorías propias de audífonos Bluetooth'),
 'audio_cable': (.9, 'Chile 2026: audífonos con cable duplicaron ventas (indirecta)'),
 'jbl': (.9, 'JBL Go 4 entre las bocinas más vendidas de Mercado Libre México (Xataka); marcas JBL en Mercado Libre Costa Rica'),
 'parlante': (.85, 'Audio portátil: regalo fácil; categoría fuerte en la región (indirecta)'),
 'reloj': (.9, 'Relojes inteligentes entre lo más comprado en Colombia 2026 (indirecta)'),
 'power': (.9, 'Power banks y cargadores magnéticos: listas TikTok Shop 2026 y tiendas de Costa Rica (Yaxa, Mercado Libre CR)'),
 'soporte': (.85, 'Soportes magnéticos y de carro: listas TikTok Shop 2026 y tiendas de Costa Rica'),
 'aro': (.85, 'Aros de luz y creadores: listas TikTok Shop Q2 2026 (blogs, sesgados)'),
 'mic': (.8, 'Micrófonos inalámbricos mini: listas TikTok Shop 2026 (blogs, sesgados)'),
 'hogar': (.8, 'Dispensadores y gadgets de hogar: listas TikTok 2026 (blogs, sesgados)'),
 'gaming': (.85, 'Accesorios gamer y consolas: demanda alta en Colombia 2026 (indirecta)'),
 'ps': (.85, 'Controles de consola: demanda constante en la región (indirecta)'),
 'buds': (.8, 'Audio inalámbrico lidera la región (Colombia 2026)'),
 'juguete': (.75, 'Temporada de Navidad (sin dato específico de Costa Rica)'),
 'camara': (.55, 'Sin señal propia; se elige por utilidad como regalo'),
 'cargador': (.8, 'Cables y cargadores: compra recurrente de accesorios (indirecta)'),
 'funda': (.65, 'Fundas y protección: venta recurrente por cada celular (indirecta)'),
 'pencil': (.55, 'Nicho: solo usuarios de iPad; sin señal de ventas propia'),
 'computo': (.6, 'Accesorios de computación: demanda estable, sin señal específica'),
 'otro': (.45, 'Sin señal específica de demanda'),
}
NOM = {'earpods': 'Audífonos EarPods (marca)', 'airpods': 'Audífonos estilo AirPods (marca)', 'audio_inal': 'Audífonos inalámbricos', 'audio_cable': 'Audífonos con cable', 'jbl': 'Parlantes estilo JBL (marca)', 'parlante': 'Parlantes y bocinas', 'reloj': 'Relojes inteligentes', 'power': 'Power banks y baterías', 'soporte': 'Soportes y selfie', 'aro': 'Aros de luz y creadores', 'mic': 'Micrófonos', 'hogar': 'Hogar y cuidado personal', 'gaming': 'Gaming (mouse, teclado, audífonos gamer)', 'ps': 'Controles de consola', 'buds': 'Galaxy Buds estilo (marca)', 'juguete': 'Juguetes y regalos', 'camara': 'Cámaras y seguridad', 'cargador': 'Cargadores, cables y adaptadores', 'funda': 'Fundas y protección', 'pencil': 'Apple Pencil estilo (marca)', 'computo': 'Computación y accesorios', 'otro': 'Otros'}
def tipo(x):
    t = (x['producto'] + ' ' + x['codigo']).upper()[:90]; pr = x['proveedor']
    if pr.startswith('Canguro'): return 'juguete'
    if pr == 'MyTechnologyCR':
        c = mycat.get((x['pagina'], x['producto']), '')
        if re.search(r'EARPODS', t): return 'earpods'
        if re.search(r'GALAXY BUDS', t): return 'buds'
        if re.search(r'PENCIL', t): return 'pencil'
        if re.search(r'JBL', t): return 'jbl'
        if re.search(r'AIRPODS|AIRPOD', t): return 'airpods'
        m = {'Audio': 'audio_inal', 'Cargadores': 'cargador', 'Cables': 'cargador', 'Fundas y protección': 'funda', 'Relojes': 'reloj', 'Soportes': 'soporte', 'Juguetes y movilidad': 'juguete', 'Creadores': 'mic', 'Hogar': 'hogar', 'Cámaras y seguridad': 'camara', 'Gaming': 'ps', 'Power banks': 'power', 'Cuidado personal': 'hogar', 'Auto y moto': 'soporte', 'Protectores de pantalla': 'funda', 'Accesorios tablet': 'funda', 'Almacenamiento': 'computo'}
        tp = m.get(c, 'otro')
        if tp == 'audio_inal' and re.search(r'PARLANTE|BOCINA|SPEAKER', t): tp = 'parlante'
        return tp
    if re.search(r'EARPODS', t): return 'earpods'
    if re.search(r'PANEL LUZ|PANEL DE LUZ', t): return 'aro'
    if re.search(r'PS5|PS4|CONTROL (PS|DE)', t): return 'ps'
    if re.search(r'POWER ?BANK|BATERIA PORT|BATERÍA PORT|BATERIA DE', t): return 'power'
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
    if re.search(r'CARGADOR|CABLE|CUBO|ADAPTADOR|OTG', t): return 'cargador'
    if re.search(r'LAPTOP|USB|HUB|BASE|WEBCAM|MEMORIA|LECTOR|MICRO ?SD', t): return 'computo'
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
        w = re.findall(r'[A-ZÁÉÍÓÚÑ]{3,}', t.upper()); return 'C:' + (w[0] if w else t[:8])
    w = re.findall(r'[A-ZÁÉÍÓÚÑ]{3,}', t.upper())
    if x['proveedor'] == 'MyTechnologyCR': return 'M:' + x['pagina']
    return ' '.join(w[:2]) if len(w) >= 2 else (x['codigo'] or t[:14])
cand = []
for x in rows:
    if x['proveedor'] == 'MyTechnologyCR' and (x['pagina'], x['producto']) in mycat and mycat[(x['pagina'], x['producto'])] == 'Portada': continue
    tp = tipo(x); w, sg = SIG[tp]; kk = k(x)
    sc = .5 * w + .25 * impulso(x) + .15 * (1 if tp not in ('otro', 'camara', 'computo') else .6) + .10 * (1 if kk in IMG else 0)
    cand.append(dict(x=x, tp=tp, sc=sc, sg=sg, ag=kk in AGO, mk=marca.get(kk, '')))
disp = sorted([c for c in cand if not c['ag']], key=lambda c: -c['sc'])
quota = {'Techno Go': 30, 'MyTechnologyCR': 18, 'Canguro Panamá': 12}; tcap = {'Techno Go': 4, 'MyTechnologyCR': 5, 'Canguro Panamá': 12}
A = []; seen = set()
for pv, q in quota.items():
    typ = defaultdict(int); n = 0
    for c in disp:
        if c['x']['proveedor'] != pv: continue
        f = fam(c['x'])
        if (pv, f) in seen or typ[c['tp']] >= tcap[pv]: continue
        seen.add((pv, f)); typ[c['tp']] += 1; A.append(c); n += 1
        if n >= q: break
for c in cand: c['tier'] = 'A' if any(c is a for a in A) else ('Sin stock' if c['ag'] else None)
rest = sorted([c for c in cand if c['tier'] is None], key=lambda c: -c['sc'])
for i, c in enumerate(rest): c['tier'] = 'B' if i < 260 else 'C'
nA = len(A); nB = sum(1 for c in cand if c['tier'] == 'B'); nC = sum(1 for c in cand if c['tier'] == 'C'); nS = sum(1 for c in cand if c['tier'] == 'Sin stock')
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.6pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:middle}td.n,th.n{text-align:right;white-space:nowrap}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:120px;object-fit:contain}.g{color:#c4161c;font-weight:700}</style>']
H.append('<h1>El Tilichero CR</h1><p><b>Análisis de ventas con todos los productos (sin precios)</b> · 4 de noviembre de 2026</p>')
H.append(f'<div class=nota><b>Qué se hizo.</b> Analicé los <b>{len(cand)} productos de los tres proveedores</b> sin dejar ninguno fuera por marca, tipo ni margen: incluidas las marcas y réplicas, los «originales con logo» y los de menor valor. Cada producto recibió un puntaje de potencial de venta y quedó en un nivel: <b>A</b> ({nA}) poner primero; <b>B</b> ({nB}) segunda ola; <b>C</b> ({nC}) resto, publicar después; <b>Sin stock</b> ({nS}) con sello AGOTADO, confirmar reposición con el proveedor.</div>')
H.append('<div class=nota><b>Límites.</b> No hay un ranking público de ventas de Costa Rica; las señales de demanda son regionales o indirectas (cada fila indica la suya). El puntaje (demanda del tipo 50 %, facilidad de compra por impulso según costo interno 25 %, demostrable en video 15 %, tiene foto 10 %) es un criterio de trabajo, no una fórmula validada. «Nivel A» significa candidato prioritario; las ventas reales confirman o corrigen este orden. Sin precios, por indicación del dueño. Las marcas y réplicas están incluidas por indicación del dueño (no verificadas de forma independiente); los «originales con logo» sin factura no deben anunciarse como originales.</div>')
H.append('<h2>1. Señales del mercado</h2><ul><li><b>Costa Rica compra tecnología en línea:</b> la electrónica es el 24 % de los ingresos del comercio electrónico (PCMI, 2024); AliExpress, Walmart, Intelec y eBay son las tiendas más visitadas. La entrega rápida es la ventaja frente a las importaciones.</li><li><b>Audio:</b> EarPods con cable fueron los audífonos más vendidos en Chile (1.er semestre de 2026) y los de cable duplicaron ventas; el audio inalámbrico lidera Colombia 2026.</li><li><b>Tendencias TikTok Shop 2026</b> (blogs, sesgados): aros de luz, micrófonos mini, cargadores y soportes magnéticos, dispensadores automáticos.</li><li><b>Mercado Libre Costa Rica</b> (visto en búsquedas): genéricos tipo AirPods entre ₡7 500 y ₡10 000; marcas conocidas de ₡29 000 a más de ₡100 000. El listado requiere iniciar sesión, por eso no pude ver ventas por producto.</li><li><b>Dato propio:</b> el Reel R4, con caja tipo AirPods, tuvo 62 vistas y 1 me gusta; el alcance orgánico no es el problema (R2 llegó a 2 414 cuentas) sino decir qué se vende.</li></ul>')
H.append('<h2>2. Resultado por tipo de producto</h2><table><tr><th>Tipo</th><th class=n>Productos</th><th class=n>Nivel A</th><th class=n>Nivel B</th><th class=n>Nivel C</th><th class=n>Sin stock</th><th class=n>Puntaje medio</th></tr>')
bt = defaultdict(list)
for c in cand: bt[c['tp']].append(c)
for tp, L in sorted(bt.items(), key=lambda kv: -statistics.mean(c['sc'] for c in kv[1])):
    H.append(f"<tr><td>{e(NOM[tp])}</td><td class=n>{len(L)}</td><td class=n>{sum(1 for c in L if c['tier']=='A')}</td><td class=n>{sum(1 for c in L if c['tier']=='B')}</td><td class=n>{sum(1 for c in L if c['tier']=='C')}</td><td class=n>{sum(1 for c in L if c['tier']=='Sin stock')}</td><td class=n>{statistics.mean(c['sc'] for c in L):.2f}</td></tr>")
H.append('</table>')
def row(c, h):
    x = c['x']; nm = x['producto'].split(' / ')[-1] if x['proveedor'].startswith('Canguro') and ' / ' in x['producto'] else x['producto']
    mk = ' <b style="color:#a05a00">· marca</b>' if c['mk'] and not c['mk'].startswith('Falso') else ''
    return f"<td>{img(x, h)}</td><td>{e(nm[:80])}{mk}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td>"
H.append(f'<div class=pb></div><h2>3. Nivel A: los {nA} productos para poner primero</h2><table><tr><th>#</th><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Tipo</th><th>Señal de demanda</th></tr>')
for i, c in enumerate(A, 1):
    H.append(f"<tr><td class=g>{i}</td>{row(c, 90 if c['x']['proveedor']=='MyTechnologyCR' else 58)}<td class=sm>{e(NOM[c['tp']])}</td><td class=sm>{e(c['sg'])}</td></tr>")
H.append('</table>')
H.append(f'<div class=pb></div><h2>4. Nivel B: segunda ola ({nB})</h2><table><tr><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Tipo</th></tr>')
for c in sorted([c for c in cand if c['tier'] == 'B'], key=lambda c: (c['tp'], -c['sc'])):
    H.append(f"<tr>{row(c, 70 if c['x']['proveedor']=='MyTechnologyCR' else 46)}<td class=sm>{e(NOM[c['tp']])}</td></tr>")
H.append('</table>')
H.append(f'<div class=pb></div><h2>5. Nivel C: resto del catálogo ({nC}), sin dejar ninguno fuera</h2><table><tr><th>Producto</th><th>Proveedor</th><th>Tipo</th></tr>')
for c in sorted([c for c in cand if c['tier'] == 'C'], key=lambda c: (c['tp'], -c['sc'])):
    x = c['x']; nm = x['producto'].split(' / ')[-1] if x['proveedor'].startswith('Canguro') and ' / ' in x['producto'] else x['producto']
    H.append(f"<tr><td>{e(nm[:80])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td><td class=sm>{e(NOM[c['tp']])}</td></tr>")
H.append(f'</table><h2>6. Sin stock en el catálogo del proveedor ({nS})</h2><table><tr><th>Producto</th><th>Proveedor</th><th>Tipo</th></tr>')
for c in [c for c in cand if c['tier'] == 'Sin stock']:
    x = c['x']; H.append(f"<tr><td>{e(x['producto'][:80])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])} p.{x['pagina']} {e(x['codigo'][:12])}</td><td class=sm>{e(NOM[c['tp']])}</td></tr>")
H.append('</table><p class=sm>Fuentes de las señales: WOM Chile (eldinamo.cl), Tiendanube Colombia 2026, Delfino/PCMI, Xataka México, listas de TikTok Shop 2026 (blogs y agencias), búsquedas de Mercado Libre y Yaxa Costa Rica. Confirmar stock con cada proveedor antes de publicar. Fotos: PDF de cada proveedor (pueden mostrar productos vecinos).</p>')
out.write_text(''.join(H), encoding='utf-8')
w = csv.writer(csvout.open('w', newline='', encoding='utf-8')); w.writerow(['nivel', 'puntaje', 'tipo', 'proveedor', 'catalogo', 'pagina', 'codigo', 'producto', 'marca'])
for c in sorted(cand, key=lambda c: ({'A': 0, 'B': 1, 'C': 2, 'Sin stock': 3}[c['tier']], -c['sc'])):
    x = c['x']; w.writerow([c['tier'], f"{c['sc']:.2f}", NOM[c['tp']], x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto'], 'sí' if c['mk'] and not c['mk'].startswith('Falso') else ''])
print(len(cand), nA, nB, nC, nS)
