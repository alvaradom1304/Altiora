"""Miniaturas por producto. Techno Go: recorte de la fila del catálogo donde aparece el código (NO es foto aislada).
Canguro: foto por código. MyTechnologyCR: página del catálogo (1 producto por página)."""
import csv, re, sys, json, glob
sys.path.append(r'C:\Users\Usuario\AppData\Roaming\Python\Python312\site-packages')
import warnings; warnings.filterwarnings('ignore')
import pymupdf
from pathlib import Path
P = Path(sys.argv[1]); PDFS = Path(sys.argv[2]); OUT = Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
MV3 = P.parent / 'master-v3' / 'imagenes'
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
res = {}  # clave -> ruta
def key(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
# Canguro
cang = {Path(f).name.split('-')[0]: f for f in glob.glob(str(MV3 / 'canguro' / '*.jpg'))}
# MyTechnologyCR
mt = {}
for r in csv.DictReader((P / 'mytechnologycr-indice.csv').open(encoding='utf-8')):
    mt[r['pagina']] = P.parent / r['imagen_local']
docs = {}
def doc(n):
    if n not in docs: docs[n] = pymupdf.open(str(PDFS / (n + '.pdf')))
    return docs[n]
# Techno Go ORIGINAL: anclas por página
bypage = {}
for x in rows:
    if x['proveedor'] == 'Techno Go' and x['catalogo'] != '1HORA' and x['pagina']:
        bypage.setdefault((x['catalogo'], int(x['pagina'])), []).append(x)
n_tg = 0
for (cat, pg), items in bypage.items():
    if not (PDFS / (cat + '.pdf')).exists(): continue
    page = doc(cat)[pg - 1]; W, H = page.rect.width, page.rect.height
    anchors = []
    for x in items:
        c = x['codigo'].strip()
        if len(c) < 3: continue
        hits = page.search_for(c)
        if hits: anchors.append((x, hits[0]))
    if not anchors: continue
    anchors.sort(key=lambda a: (a[1].y0, a[1].x0))
    rowsg = []
    for a in anchors:
        if rowsg and abs(rowsg[-1][0][1].y0 - a[1].y0) < 45: rowsg[-1].append(a)
        else: rowsg.append([a])
    for i, rg in enumerate(rowsg):
        top = (max(a[1].y1 for a in rowsg[i - 1]) + 25) if i else max(rg[0][1].y0 - 430, 120)
        top = max(top, rg[0][1].y0 - 480)
        bot = max(a[1].y1 for a in rg) + 55
        rg.sort(key=lambda a: a[1].x0)
        for j, (x, r) in enumerate(rg):
            cx = (r.x0 + r.x1) / 2
            left = 0 if j == 0 else (rg[j - 1][1].x1 + r.x0) / 2 - 20
            right = W if j == len(rg) - 1 else (r.x1 + rg[j + 1][1].x0) / 2 + 20
            if len(rg) == 1: left, right = max(0, cx - 330), min(W, cx + 330)
            clip = pymupdf.Rect(max(0, left), max(0, top), min(W, right), min(H, bot))
            if clip.width < 40 or clip.height < 40: continue
            zoom = 240 / clip.width
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
            f = OUT / f"tg_{cat}_{pg}_{re.sub(r'[^A-Za-z0-9]+','_',x['codigo'])[:30]}.jpg"
            pix.save(str(f), jpg_quality=70)
            res[key(x)] = str(f); n_tg += 1
n_c = n_m = 0
for x in rows:
    k = key(x)
    if x['proveedor'] == 'Canguro Panamá' and x['codigo'] in cang: res[k] = cang[x['codigo']]; n_c += 1
    if x['proveedor'] == 'MyTechnologyCR' and x['pagina'] in mt and mt[x['pagina']].exists(): res[k] = str(mt[x['pagina']]); n_m += 1
json.dump(res, open(OUT / 'mapa.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('TechnoGo', n_tg, 'Canguro', n_c, 'MyTech', n_m, 'total', len(res))
