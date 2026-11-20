import csv, sys, json, html
from pathlib import Path
from collections import defaultdict
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3]); csvout = Path(sys.argv[4])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8'))
e = html.escape
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def img(x, h): f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + f'" height={h}>') if f else ''
tg = list(csv.DictReader((P / 'plan-de-ventas-ampliado.csv').open(encoding='utf-8')))
uni = {k(x): x for x in csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8'))}
nov = {k(x): x['decision_sugerida'] for x in csv.DictReader((P / 'productos-riesgo-marca.csv').open(encoding='utf-8'))}
tgrows = defaultdict(list)
for r in tg:
    kk = '|'.join([r['proveedor'], r['catalogo'], r['pagina'], r['codigo'], r['producto']])
    tgrows[r['categoria']].append(uni[kk])
my = [x for x in csv.DictReader((P / 'mytechnologycr-indice.csv').open(encoding='utf-8')) if x['categoria'] != 'Portada']
uni_my = [x for x in uni.values() if x['proveedor'] == 'MyTechnologyCR']
bykey = {(x['pagina'], x['producto']): x for x in uni_my}
myrows = defaultdict(list)
for r in my:
    x = bykey.get((r['pagina'], r['producto']))
    if x: myrows[r['categoria']].append((x, r['riesgo_marca'].split(':')[0]))
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.8pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:3px 5px;vertical-align:middle}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:130px;object-fit:contain}</style>']
ntg = sum(len(v) for v in tgrows.values()); nmy = sum(len(v) for v in myrows.values())
H.append(f'<h1>El Tilichero CR</h1><p><b>Plan de trabajo sin precios: Techno Go + MyTechnologyCR</b> · 4 de noviembre de 2026</p>')
H.append(f'<div class=nota><b>Qué es.</b> Lista de trabajo de <b>{ntg + nmy} productos</b>: {ntg} de Techno Go (selección para vender por volumen) y {nmy} de MyTechnologyCR (todo su catálogo). <b>Sin precios</b>: se definen después. Las fotos de MyTechnologyCR son la página de su catálogo, que puede mostrar varias referencias del mismo producto.</div>')
H.append('<div class=nota><b>Marcas y réplicas.</b> Los productos de marca o «estilo marca» están incluidos por indicación del dueño (validados por él; no los verifiqué de forma independiente) y llevan la etiqueta «marca».</div>')
H.append('<h1 style="font-size:18pt;margin-top:12px">Parte A · Techno Go</h1>')
for g, L in tgrows.items():
    H.append(f'<h2>{e(g)} · {len(L)}</h2><table><tr><th>Foto</th><th>Producto</th><th>Catálogo / página / código</th></tr>')
    for x in L:
        nm = x['producto'].split(' / ')[-1] if x['proveedor'].startswith('Canguro') and ' / ' in x['producto'] else x['producto']
        H.append(f"<tr><td>{img(x, 58)}</td><td>{e(nm[:90])}</td><td class=sm>{e(x['proveedor'])} · {e(x['catalogo'][:16])}{(' p.' + x['pagina']) if x['pagina'] else ''} {e(x['codigo'][:14])}</td></tr>")
    H.append('</table>')
H.append('<div class=pb></div><h1 style="font-size:18pt">Parte B · MyTechnologyCR (catálogo completo)</h1>')
for g, L in sorted(myrows.items(), key=lambda kv: -len(kv[1])):
    H.append(f'<h2>{e(g)} · {len(L)}</h2><table><tr><th>Foto (página del catálogo)</th><th>Producto</th><th>Página</th></tr>')
    for x, rg in L:
        tag = ' <b style="color:#a05a00">· marca</b>' if rg in ('ALTO', 'MEDIO') else ''
        H.append(f"<tr><td>{img(x, 110)}</td><td>{e(x['producto'][:90])}{tag}</td><td class=sm>p. {x['pagina']}</td></tr>")
    H.append('</table>')
H.append('<p class=sm>Fuentes: catálogos de Techno Go (PDF, octubre 2026) y MyTechnologyCR (catálogo sin precios). Los productos con sello AGOTADO en Techno Go están excluidos; confirmar stock con cada proveedor antes de publicar.</p>')
out.write_text(''.join(H), encoding='utf-8')
w = csv.writer(csvout.open('w', newline='', encoding='utf-8')); w.writerow(['proveedor', 'categoria', 'catalogo', 'pagina', 'codigo', 'producto', 'marca_o_estilo_marca'])
for g, L in tgrows.items():
    for x in L: w.writerow([x['proveedor'], g, x['catalogo'], x['pagina'], x['codigo'], x['producto'], ''])
for g, L in myrows.items():
    for x, rg in L: w.writerow([x['proveedor'], g, x['catalogo'], x['pagina'], x['codigo'], x['producto'], 'sí' if rg in ('ALTO', 'MEDIO') else ''])
print(ntg, nmy)
