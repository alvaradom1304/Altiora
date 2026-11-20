import csv, re, sys, json, html
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3]); csvout = Path(sys.argv[4])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
e = html.escape
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def img(x, h): f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + f'" height={h}>') if f else ''
rows = [x for x in csv.DictReader((P / 'productos-riesgo-marca.csv').open(encoding='utf-8'))]
rows = [x for x in rows if not x['decision_sugerida'].startswith('Falso positivo') and not re.match(r'(JD060|P5425)', x['codigo'] + x['producto'])]
def etiqueta(d):
    if d.startswith('VENDER (validado'): return 'Marca/réplica · validado por el dueño'
    if d.startswith('NO VENDER sin factura'): return 'No anunciar como «original» sin factura'
    if d.startswith('VENDER como compatible'): return 'Compatible: nombrar la marca solo como compatibilidad'
    return 'Revisar nombre de marca'
SIG = {
 'earpods': (1.0, 'Chile, 1.er semestre 2026: los Apple EarPods con cable fueron los audífonos más vendidos (WOM) y los audífonos con cable duplicaron ventas'),
 'airpods': (.95, 'Audio inalámbrico lidera la región (Colombia 2026); Mercado Libre Costa Rica tiene una categoría propia «Auricular Airpod»; genéricos visibles ahí entre ₡7 500 y ₡10 000'),
 'jbl': (.9, 'La JBL Go 4 aparece entre las bocinas más vendidas de Mercado Libre México (Xataka); en Costa Rica hay JBL de marca en Mercado Libre desde ₡31 999'),
 'ps': (.85, 'Accesorios gamer y consolas: demanda alta en Colombia 2026; control DualSense con ventas constantes en la región (indirecta)'),
 'cargador': (.85, 'Cables y cargadores para iPhone y Android: compra recurrente; es la categoría de accesorios más amplia (indirecta)'),
 'buds': (.8, 'Audio inalámbrico lidera la región (Colombia 2026); los Galaxy Buds de marca superan ₡100 000 en Mercado Libre Costa Rica'),
 'power': (.8, 'Power banks y cargadores magnéticos en listas de TikTok Shop 2026 y en tiendas de Costa Rica'),
 'pencil': (.55, 'Nicho: solo usuarios de iPad; sin señal de ventas propia'),
 'regalo': (.75, 'Carros RC con licencia: regalo de Navidad (sin dato específico de Costa Rica)'),
 'funda': (.6, 'Fundas: compra recurrente por cada celular (indirecta)'),
 'otro': (.5, 'Sin señal específica'),
}
def tipo(x):
    t = (x['producto'] + ' ' + x['codigo']).upper()
    if x['proveedor'].startswith('Canguro'): return 'regalo'
    if re.search(r'FUNDA', t): return 'funda'
    if re.search(r'EARPODS', t): return 'earpods'
    if re.search(r'GALAXY BUDS', t): return 'buds'
    if re.search(r'AIRPODS|AIRPOD|AUDÍFONOS.*1:1|DIADEMA', t): return 'airpods'
    if re.search(r'JBL|PARLANTE', t): return 'jbl'
    if re.search(r'PS5|PS4|CONTROL', t): return 'ps'
    if re.search(r'PENCIL', t): return 'pencil'
    if re.search(r'MAGSAFE|POWER ?BANK|BATERIA', t): return 'power'
    if re.search(r'CARGADOR|CABLE|CUBO|LIGHTNING|IPHONE|TYPE-C|TIPO-C|OTG|ADAPTADOR', t): return 'cargador'
    return 'otro'
cand = []
for x in rows:
    kk = k(x)
    if kk in AGO: continue
    tp = tipo(x); w, sg = SIG[tp]
    cand.append(dict(x=x, tp=tp, sc=w + (.05 if kk in IMG else 0), sg=sg))
cand.sort(key=lambda c: -c['sc'])
win = []; seen = set(); typ = defaultdict(int)
for c in cand:
    x = c['x']
    f = (x['proveedor'], c['tp'], re.sub(r'[^a-z0-9 ]', '', x['producto'].lower())[:22]) if x['proveedor'] != 'MyTechnologyCR' else (x['proveedor'], x['pagina'])
    if f in seen or typ[c['tp']] >= 6: continue
    seen.add(f); typ[c['tp']] += 1; win.append(c)
    if len(win) >= 30: break
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.6pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:middle}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:120px;object-fit:contain}.g{color:#c4161c;font-weight:700}</style>']
H.append('<h1>El Tilichero CR</h1><p><b>Productos de marca: qué dice el mercado y cuáles poner primero (sin precios)</b> · 4 de noviembre de 2026</p>')
H.append('<div class=nota><b>Resultado de la búsqueda de mercado.</b> <b>No encontré ventas verificables de productos de marca en Costa Rica</b>: Mercado Libre Costa Rica pide iniciar sesión para ver sus listados (no entré a ninguna cuenta) y las búsquedas no devolvieron precios ni ventas locales de AirPods, JBL, DualSense ni Apple Pencil. Lo que sí se verificó está abajo; todo es indirecto.</div>')
H.append('<h2>Qué sí muestra el mercado</h2><ul><li><b>Costa Rica compra tecnología en línea:</b> la electrónica es el 24 % de los ingresos del comercio electrónico del país (PCMI, 2024) y las tiendas más visitadas incluyen AliExpress, Walmart, Intelec y eBay (diciembre de 2024). Los compradores ya buscan precio bajo en importaciones; el plazo de entrega rápido es una ventaja frente a ellas.</li><li><b>Audio:</b> los audífonos con cable de Apple fueron los más vendidos en Chile en el primer semestre de 2026 y los de cable duplicaron ventas; el audio inalámbrico lidera Colombia 2026.</li><li><b>Parlantes:</b> la JBL Go 4 figura entre las bocinas más vendidas de Mercado Libre México.</li><li><b>En Costa Rica:</b> los audífonos genéricos tipo AirPods se ven en Mercado Libre entre ₡7 500 y ₡10 000; las marcas conocidas van de ₡29 000 a más de ₡100 000. Esa distancia de precio es la oportunidad del «estilo marca»: quien quiere el look sin pagar la marca.</li></ul>')
H.append('<div class=nota><b>Dato propio que modera el optimismo.</b> El Reel R4 de El Tilichero, con una caja tipo AirPods, tuvo 62 vistas y 1 me gusta. Un solo video no demuestra falta de demanda (depende del video), pero no confirma la demanda del producto.</div>')
H.append('<div class=nota><b>Cómo leer la lista.</b> Los productos de marca y «estilo marca» están incluidos por indicación del dueño (validados por él; no los verifiqué de forma independiente). Antes de publicar: no llamar «original» a lo que no tenga factura del fabricante (afecta a las 7 filas marcadas), y confirmar stock. Sin precios, por indicación del dueño.</div>')
H.append(f'<h2>Los {len(win)} productos de marca para poner primero</h2><table><tr><th>#</th><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Señal de demanda</th><th>Nota</th></tr>')
for i, c in enumerate(win, 1):
    x = c['x']; h = 90 if x['proveedor'] == 'MyTechnologyCR' else 58
    H.append(f"<tr><td class=g>{i}</td><td>{img(x, h)}</td><td>{e(x['producto'][:80])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td><td class=sm>{e(c['sg'])}</td><td class=sm>{e(etiqueta(x['decision_sugerida']))}</td></tr>")
H.append('</table>')
H.append('<div class=pb></div><h2>Todos los productos de marca de los 3 proveedores</h2><table><tr><th>Foto</th><th>Producto</th><th>Proveedor</th><th>Nota</th></tr>')
for x in sorted(rows, key=lambda r: (r['proveedor'], int(r['pagina'] or 0))):
    h = 90 if x['proveedor'] == 'MyTechnologyCR' else 52
    ag = ' <b style="color:#c4161c">AGOTADO</b>' if k(x) in AGO else ''
    H.append(f"<tr><td>{img(x, h)}</td><td>{e(x['producto'][:85])}{ag}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:14])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:12])}</td><td class=sm>{e(etiqueta(x['decision_sugerida']))}</td></tr>")
H.append('</table><p class=sm>Fuentes: [Delfino/PCMI sobre comercio electrónico en Costa Rica], WOM Chile vía eldinamo.cl, Tiendanube Colombia 2026, Xataka México (JBL Go 4), listados de Mercado Libre Costa Rica vistos en búsquedas. Ningún dato es de ventas de Costa Rica por producto.</p>')
out.write_text(''.join(H), encoding='utf-8')
w = csv.writer(csvout.open('w', newline='', encoding='utf-8')); w.writerow(['ranking', 'proveedor', 'catalogo', 'pagina', 'codigo', 'producto', 'tipo', 'nota'])
for i, c in enumerate(win, 1):
    x = c['x']; w.writerow([i, x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto'], c['tp'], etiqueta(x['decision_sugerida'])])
print(len(rows), len(win), dict(typ))
