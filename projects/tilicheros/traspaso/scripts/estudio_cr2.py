import collections
import sys, math
sys.argv = sys.argv[:5] + sys.argv[5:]
SC = sys.argv[3]
_src = open(SC + '/scripts/analisis_total.py', encoding='utf-8').read()
exec(_src[:_src.index('cand = []')])          # datos, tipo(), fam(), NOM, helpers
WM = json.load(open(SC + '/walmart_cr.json', encoding='utf-8'))
WMB = json.load(open(SC + '/walmart_marcas.json', encoding='utf-8'))
EXC = ('Farmacia', 'Higiene', 'Bebes', 'Alimentos', 'Bebidas', 'Limpieza')
TT = {'audio_inal': ['audifonos inalambricos', 'audifonos bluetooth'], 'audio_cable': ['audifonos'], 'earpods': ['audifonos'], 'airpods': ['airpods'],
      'jbl': ['jbl'], 'parlante': ['parlante bluetooth', 'bocina'], 'reloj': ['smartwatch', 'reloj inteligente'], 'power': ['power bank', 'bateria portatil'],
      'soporte': ['soporte celular', 'selfie', 'tripode celular'], 'aro': ['aro de luz'], 'mic': ['microfono'], 'hogar': ['dispensador agua', 'regleta', 'cepillo electrico'],
      'gaming': ['mouse inalambrico', 'teclado'], 'ps': ['control ps5'], 'juguete': ['juguete', 'carro control remoto', 'scooter', 'muneca', 'drone'],
      'camara': ['camara de seguridad', 'camara wifi'], 'cargador': ['cargador celular', 'cable usb', 'cable tipo c', 'cargador carro'], 'funda': ['funda celular'],
      'pencil': ['apple pencil'], 'buds': ['audifonos'], 'computo': ['memoria usb'], 'otro': []}
def q(v, p):
    v = sorted(v); return v[min(len(v) - 1, int(p * (len(v) - 1)))]
CR = {}
for tp, terms in TT.items():
    tot = 0; pr = []; nz = 0; brands = []
    for t in terms:
        d = WM.get(t)
        if not d: continue
        try: tot += int(d['total'].split('/')[-1])
        except Exception: pass
        for it in d['items']:
            if any(x in (it['cat'] or '') for x in EXC): continue
            if it['price'] and it['price'] > 0: pr.append(it['price'])
            if it['b']: brands.append(it['b'])
    CR[tp] = dict(total=tot, med=statistics.median(pr) if pr else None, lo=q(pr, .25) if pr else None, hi=q(pr, .75) if pr else None, n=len(pr),
                  brands=', '.join(b for b, _ in collections.Counter(brands).most_common(3)) if brands else '') if True else None
import collections
for tp in TT:
    pr = []; brands = []
    for t in TT[tp]:
        d = WM.get(t)
        if not d: continue
        for it in d['items']:
            if any(x in (it['cat'] or '') for x in EXC): continue
            if it['price'] and it['price'] > 0: pr.append(it['price'])
            if it['b']: brands.append(it['b'])
    c = CR[tp]
    c['brands'] = ', '.join(b for b, _ in collections.Counter(brands).most_common(3))
TRD = json.load(open(SC + '/trends_cr.json', encoding='utf-8'))
TTR = {'airpods': ['airpods'], 'earpods': ['audifonos'], 'audio_cable': ['audifonos'], 'audio_inal': ['audifonos'], 'buds': ['audifonos'], 'jbl': ['jbl'], 'parlante': ['parlante'],
       'reloj': ['smartwatch', 'reloj inteligente'], 'power': ['power bank'], 'soporte': ['soporte celular', 'tripode'], 'aro': ['aro de luz'], 'mic': ['microfono'],
       'hogar': ['dispensador de agua', 'regleta', 'cepillo electrico', 'humidificador', 'masajeador'], 'gaming': ['control ps5'], 'ps': ['control ps5'],
       'juguete': ['juguetes', 'muñecas', 'scooter', 'drone', 'carros control remoto'], 'camara': ['camara de seguridad', 'camara wifi'], 'cargador': ['cargador'],
       'funda': ['funda iphone', 'protector de pantalla'], 'pencil': ['apple pencil'], 'computo': ['tablet'], 'otro': []}
def tr(tp):
    r = {}
    for src in ('web', 'yt'):
        best = None
        for t in TTR.get(tp, []):
            v = TRD[src].get(t)
            if v and (best is None or v[0] > best[1][0]): best = (t, v)
        r[src] = best
    return r
def nrm(v): return 0 if v is None else min(1.0, math.log10(1 + v) / math.log10(81))
def rising(v): return v is not None and v[1] >= 5 and v[2] > 0 and v[1] / v[2] >= 1.15
def wdem(tp):
    if tp == 'otro': return .45
    t = tr(tp); gw = t['web'][1][0] if t['web'] else None; gy = t['yt'][1][0] if t['yt'] else None
    b = .03 if (rising(t['web'][1] if t['web'] else None) or rising(t['yt'][1] if t['yt'] else None)) else 0
    return round(min(1.0, .5 * wcr(tp) + .3 * nrm(gw) + .2 * nrm(gy) + b), 3)
def wcr(tp):
    t = CR[tp]['total']
    return 0.45 if tp == 'otro' else round(max(.35, min(1.0, .4 + .6 * math.log10(1 + t) / math.log10(151))), 2)
def money(v): return '₡' + f"{int(v):,}".replace(',', ' ')
def sg(tp):
    c = CR[tp]
    if not c['total'] and tp not in ('otro',): return 'Sin oferta en Walmart CR: oportunidad sin competencia o sin demanda (no distinguible con estos datos)'
    if c['med'] is None: return 'Sin dato de precio en Walmart CR'
    t = tr(tp); a = f"Walmart CR: {c['total']} productos; más vendidos {money(c['lo'])}–{money(c['hi'])}"
    if t['web']: a += f" · Google CR «{t['web'][0]}»: {t['web'][1][0]:.0f}" + (' ↑' if rising(t['web'][1]) else '')
    if t['yt']: a += f" · YouTube CR «{t['yt'][0]}»: {t['yt'][1][0]:.0f}" + (' ↑' if rising(t['yt'][1]) else '')
    return a
def room(x, tp):
    med = CR[tp]['med']; c = num(x['costo_mayorista_crc']) or num(x['precio_catalogo_sin_tipo_crc'])
    if not med: return .5
    if c is None: return .9 if med >= 40000 else .6
    if c < 1500: return .4
    return max(0.0, min(0.85, (med - c) / med))
cand = []
for x in rows:
    if x['proveedor'] == 'MyTechnologyCR' and mycat.get((x['pagina'], x['producto'])) == 'Portada': continue
    tp = tipo(x); w = wdem(tp); kk = k(x)
    s = .5 * w + .25 * room(x, tp) + .15 * (1 if tp not in ('otro', 'camara', 'computo') else .6) + .10 * (1 if kk in IMG else 0)
    cand.append(dict(x=x, tp=tp, sc=s, sg=sg(tp), ag=kk in AGO, mk=marca.get(kk, '')))
disp = sorted([c for c in cand if not c['ag']], key=lambda c: -c['sc'])
quota = {'Techno Go': 30, 'MyTechnologyCR': 18, 'Canguro Panamá': 12}; tcap = {'Techno Go': 4, 'MyTechnologyCR': 5, 'Canguro Panamá': 12}
A = []; seen = set()
for pv, qu in quota.items():
    typ = collections.defaultdict(int); n = 0
    for c in disp:
        if c['x']['proveedor'] != pv: continue
        f = fam(c['x'])
        if (pv, f) in seen or typ[c['tp']] >= tcap[pv]: continue
        seen.add((pv, f)); typ[c['tp']] += 1; A.append(c); n += 1
        if n >= qu: break
for c in cand: c['tier'] = 'A' if any(c is a for a in A) else ('Sin stock' if c['ag'] else None)
rest = sorted([c for c in cand if c['tier'] is None], key=lambda c: -c['sc'])
for i, c in enumerate(rest): c['tier'] = 'B' if i < 260 else 'C'
nA = len(A); nB = sum(1 for c in cand if c['tier'] == 'B'); nC = sum(1 for c in cand if c['tier'] == 'C'); nS = sum(1 for c in cand if c['tier'] == 'Sin stock')
# coincidencias directas 1Hora
MATCH = [('AUT114B', 'Audífonos 1Hora Buds AUT114B'), ('CAB265', 'Cable 1Hora CAB265 tipo C 1 m'), ('GAR152', 'Cubo 1Hora GAR152 tipo C 20 W'), ('CAB250', 'Cable 1Hora CAB250 lightning 1 m'), ('CAB246', 'Cable 1Hora CAB246 tipo A a tipo C 2 m'), ('CAB237', 'Cable 1Hora CAB237 tipo C 1 m'), ('GAR162', 'Cubo 1Hora GAR162 dos puertos 20 W'), ('GAR111', 'Cargador 1Hora GAR111 para auto')]
wm1 = {}
for it in WMB['1hora']['items']:
    for cod, _ in MATCH:
        if cod.lower() in (it['n'] or '').lower(): wm1[cod] = it
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.6pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:middle}td.n,th.n{text-align:right;white-space:nowrap}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:120px;object-fit:contain}.g{color:#c4161c;font-weight:700}</style>']
H.append('<h1>El Tilichero CR</h1><p><b>Estudio con datos de Costa Rica (tienda, buscadores y redes de video) y ranking de los 755 productos</b> · 4 de noviembre de 2026</p>')
H.append('<div class=nota><b>Fuente de los datos.</b> Consulté el catálogo público de <b>Walmart Costa Rica</b> (walmart.co.cr) ordenado por «más vendidos»: 44 búsquedas por tipo de producto y 25 por marca, con sus precios y existencias del 4 de noviembre de 2026. Es lo más cercano a datos reales de ventas en Costa Rica que pude obtener sin iniciar sesión en ninguna cuenta (Mercado Libre Costa Rica pide iniciar sesión).</div>')
H.append('<div class=nota><b>Límites.</b> Es un solo minorista (incluye vendedores externos de su marketplace). El orden «más vendidos» indica qué se vende más <i>dentro de cada búsqueda</i>, pero no da unidades ni compara entre tipos; por eso uso la <b>amplitud de la oferta</b> de cada tipo como indicador de demanda, que es una inferencia. No conozco las ventas de otros comercios, ni de Mercado Libre, Facebook o Instagram. Las ventas propias confirmarán o corregirán este orden.</div>')
H.append('<div class=nota><b>Productos virales y redes sociales.</b> No pude ver las listas de tendencias de TikTok, Instagram ni Facebook de Costa Rica: el Creative Center de TikTok redirige a una página sin datos sin iniciar sesión y no entré a ninguna cuenta. Como medida de lo que está de moda en redes usé el <b>interés de búsqueda en Google y en YouTube dentro de Costa Rica</b> (Google Trends, últimos 12 meses y últimas 8 semanas frente a las 8 anteriores). YouTube es la red social de video con datos públicos por país. Contexto: TikTok lo usa el 58 % de los adultos con celular en Costa Rica, Instagram el 47 % y Facebook el 80 % (estudio CICOM-UCR 2025 citado por Tico Times).</div>')
H.append('<h2>1. Lo que muestra el mercado de Costa Rica</h2><ul>'
 '<li><b>Se vende barato y genérico.</b> Los primeros puestos de «más vendidos» en cables, mouse, soportes, regletas, audífonos Bluetooth y power banks los ocupan marcas económicas (Durabrand, Xtech, Trust, Klip Xtreme, Devia, 1Hora) y no las marcas premium. Cables USB: ₡1 500–5 400; mouse inalámbrico: ₡2 900–5 900; soportes de celular: ₡3 900–13 600; regletas: ₡2 700–4 900.</li>'
 '<li><b>Hay oferta amplia donde hay demanda:</b> cables (73 a 118 productos), audífonos (180), parlantes y bocinas (68), muñecas (173), juguetes (172), tablets, teclados (53), micrófonos (43), cámaras de seguridad (42).</li>'
 '<li><b>Las marcas conocidas son caras y escasas:</b> AirPods 4 ₡89 900 y Pro 3 ₡154 900; Galaxy Buds 4 ₡89 900; JBL desde ₡21 900 hasta ₡690 000; Apple Pencil ₡58 800; funda oficial de iPhone ₡34 900. Hay mucho espacio de precio para alternativas «estilo marca».</li>'
 '<li><b>Smartwatch:</b> los más vendidos están entre ₡16 400 y ₡30 000 (Argom, Blackview, Samsung Fit 3). <b>Cámaras de seguridad:</b> ₡11 700–78 300 (TP-Link, Imou, Ezviz).</li>'
 '<li><b>Juguetes de Navidad:</b> carros de control remoto ₡3 500–15 000; scooters infantiles ₡12 500–17 500; la oferta de muñecas y juguetes es de las más profundas.</li>'
 '<li><b>Sin oferta en Walmart Costa Rica:</b> aros de luz, trípodes de celular (2), kits de dibujo, audífonos gamer (1), drones (1 de marca DJI a ₡120 000). No se puede distinguir si es un hueco sin competencia o falta de demanda.</li></ul>')
H.append('<h2>2. Walmart Costa Rica ya vende la línea 1Hora de nuestro proveedor</h2><table><tr><th>Producto 1Hora</th><th class=n>Precio en Walmart CR</th><th>Existencias</th><th class=n>Precio sugerido Techno Go</th><th class=n>Costo mayorista</th></tr>')
for cod, nm in MATCH:
    it = wm1.get(cod); tg = next((x for x in rows if x['catalogo'] == '1HORA' and cod in x['codigo']), None)
    wp = f"{money(it['price'])}" if it and it['price'] else ('sin stock' if it else '—')
    st = (str(it['stock']) if it and it['price'] else 'agotado') if it else 'no listado'
    H.append(f"<tr><td>{e(nm)}</td><td class=n>{wp}</td><td>{st}</td><td class=n>{money(num(tg['pvp_sugerido_proveedor_crc'])) if tg else ''}</td><td class=n>{money(num(tg['costo_mayorista_crc'])) if tg else ''}</td></tr>")
H.append('</table><p class=sm>Lectura: el precio de Walmart Costa Rica es un techo realista de mercado. En los audífonos AUT114B el precio sugerido del proveedor (₡15 000) queda muy por encima de lo que cobra Walmart (₡8 900). Los cables, que son lo que más rota, se venden entre ₡3 900 y ₡5 900. No incluyo precios de venta nuestros, por indicación del dueño.</p>')
H.append('<h2>3. Datos de Walmart Costa Rica por tipo de producto</h2><table><tr><th>Tipo</th><th class=n>Productos en Walmart CR</th><th class=n>Precio típico (más vendidos)</th><th>Marcas que dominan</th><th class=n>Peso de demanda</th></tr>')
for tp in sorted(TT, key=lambda t: -wcr(t)):
    if tp == 'otro': continue
    c = CR[tp]
    H.append(f"<tr><td>{e(NOM[tp])}</td><td class=n>{c['total'] or 0}</td><td class=n>{(money(c['lo']) + '–' + money(c['hi'])) if c['med'] else '—'}</td><td class=sm>{e(c['brands'])}</td><td class=n>{wcr(tp):.2f}</td></tr>")
H.append('</table><p class=sm>El peso de demanda (0,35 a 1,00) crece con la amplitud de la oferta del tipo en Walmart Costa Rica. Es una inferencia mía, no una cifra de ventas.</p>')
H.append('<h2>3b. Interés en redes y buscadores de Costa Rica (viral y tendencia)</h2><table><tr><th>Tipo de producto</th><th>Búsqueda en Google CR</th><th>Búsqueda en YouTube CR</th><th>Tendencia (8 semanas)</th></tr>')
def fmt(b):
    if not b: return '—'
    return f"«{b[0]}»: {b[1][0]:.0f}" + (f" (↑ {b[1][1]:.0f} vs {b[1][2]:.0f})" if rising(b[1]) else '')
for tp in sorted(TTR, key=lambda t: -wdem(t)):
    if tp == 'otro': continue
    t = tr(tp); up = rising(t['web'][1] if t['web'] else None) or rising(t['yt'][1] if t['yt'] else None)
    H.append(f"<tr><td>{e(NOM[tp])}</td><td>{e(fmt(t['web']))}</td><td>{e(fmt(t['yt']))}</td><td>{'<b style=\"color:#c4161c\">al alza</b>' if up else 'estable o a la baja'}</td></tr>")
H.append('</table><p class=sm>Índice relativo a «audífonos» = 56 en cada fuente (por eso no se comparan entre Google y YouTube). 0 significa volumen demasiado bajo para medirse. Cuidado: los juguetes y las muñecas tienen mucho volumen en YouTube por contenido infantil, no por compra; «cargador», «tablet» y «micrófono» pueden mezclar otros significados. Google Trends mide búsquedas, no ventas.</p>')
RISE = {}
for src, nmx in (('web', 'Google'), ('yt', 'YouTube')):
    for t, v in TRD[src].items():
        if t != 'audifonos' and rising(v): RISE.setdefault(t, []).append(f"{nmx} {v[2]:.0f}→{v[1]:.0f}")
H.append('<p><b>Términos al alza en Costa Rica (últimas 8 semanas frente a las 8 anteriores, con volumen de al menos 5):</b> ' + '; '.join(f"{t} ({', '.join(v)})" for t, v in sorted(RISE.items())) + '. Los demás términos medidos están estables o a la baja. Con la temporada de Navidad, juguetes, scooters y drones mantienen interés alto.</p>')
H.append(f'<div class=nota><b>Ranking de los {len(cand)} productos.</b> Puntaje = demanda del tipo (50 %: amplitud de la oferta en Walmart CR 50 %, búsquedas en Google CR 30 %, YouTube CR 20 %, más un pequeño bono si va al alza) + margen de precio frente al precio típico de Costa Rica, es decir, cuánto más barato se puede ofrecer que el mercado (25 %) + facilidad de mostrarlo en video (15 %) + foto (10 %). <b>A</b> ({nA}) poner primero; <b>B</b> ({nB}) segunda ola; <b>C</b> ({nC}) resto; <b>Sin stock</b> ({nS}) con sello AGOTADO. Ningún producto se excluye por marca ni tipo. Las marcas y réplicas están incluidas por indicación del dueño; los «originales con logo» sin factura no deben anunciarse como originales.</div>')
def row(c, h):
    x = c['x']; nm = x['producto'].split(' / ')[-1] if x['proveedor'].startswith('Canguro') and ' / ' in x['producto'] else x['producto']
    mk = ' <b style="color:#a05a00">· marca</b>' if c['mk'] and not c['mk'].startswith('Falso') else ''
    return f"<td>{img(x, h)}</td><td>{e(nm[:80])}{mk}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td>"
H.append(f'<div class=pb></div><h2>4. Nivel A: los {nA} productos para poner primero</h2><table><tr><th>#</th><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Tipo</th><th>Dato de Costa Rica</th></tr>')
for i, c in enumerate(A, 1):
    H.append(f"<tr><td class=g>{i}</td>{row(c, 90 if c['x']['proveedor']=='MyTechnologyCR' else 58)}<td class=sm>{e(NOM[c['tp']])}</td><td class=sm>{e(c['sg'])}</td></tr>")
H.append('</table>')
H.append(f'<div class=pb></div><h2>5. Nivel B: segunda ola ({nB})</h2><table><tr><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Tipo</th></tr>')
for c in sorted([c for c in cand if c['tier'] == 'B'], key=lambda c: (c['tp'], -c['sc'])):
    H.append(f"<tr>{row(c, 70 if c['x']['proveedor']=='MyTechnologyCR' else 46)}<td class=sm>{e(NOM[c['tp']])}</td></tr>")
H.append('</table>')
H.append(f'<div class=pb></div><h2>6. Nivel C: resto del catálogo ({nC})</h2><table><tr><th>Producto</th><th>Proveedor</th><th>Tipo</th></tr>')
for c in sorted([c for c in cand if c['tier'] == 'C'], key=lambda c: (c['tp'], -c['sc'])):
    x = c['x']; nm = x['producto'].split(' / ')[-1] if x['proveedor'].startswith('Canguro') and ' / ' in x['producto'] else x['producto']
    H.append(f"<tr><td>{e(nm[:80])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td><td class=sm>{e(NOM[c['tp']])}</td></tr>")
H.append(f'</table><h2>7. Sin stock en el catálogo del proveedor ({nS})</h2><table><tr><th>Producto</th><th>Proveedor</th><th>Tipo</th></tr>')
for c in [c for c in cand if c['tier'] == 'Sin stock']:
    x = c['x']; H.append(f"<tr><td>{e(x['producto'][:80])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])} p.{x['pagina']} {e(x['codigo'][:12])}</td><td class=sm>{e(NOM[c['tp']])}</td></tr>")
H.append('</table><p class=sm>Fuente: API pública del catálogo de walmart.co.cr, orden «más vendidos» (OrderByTopSaleDESC), consultada el 4 de noviembre de 2026. Fotos: PDF de cada proveedor (pueden mostrar productos vecinos). Confirmar stock con cada proveedor antes de publicar.</p>')
out.write_text(''.join(H), encoding='utf-8')
w = csv.writer(csvout.open('w', newline='', encoding='utf-8')); w.writerow(['nivel', 'puntaje', 'tipo', 'proveedor', 'catalogo', 'pagina', 'codigo', 'producto', 'marca', 'dato_costa_rica'])
for c in sorted(cand, key=lambda c: ({'A': 0, 'B': 1, 'C': 2, 'Sin stock': 3}[c['tier']], -c['sc'])):
    x = c['x']; w.writerow([c['tier'], f"{c['sc']:.2f}", NOM[c['tp']], x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto'], 'sí' if c['mk'] and not c['mk'].startswith('Falso') else '', c['sg']])
print(len(cand), nA, nB, nC, nS, sorted(wm1))
for tp in sorted(TT, key=lambda t: -wcr(t)): print(tp, CR[tp]['total'], wcr(tp), CR[tp]['med'])
