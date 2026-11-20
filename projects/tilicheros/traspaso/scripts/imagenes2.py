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
    imgs = [i for i in page.get_image_info() if 0.02 < (pymupdf.Rect(i['bbox']) & page.rect).get_area() / page.rect.get_area() < 0.40 and i['width'] > 150]
    if not imgs: continue
    for x, r in anchors:
        cx, cy = (r.x0 + r.x1) / 2, r.y0
        def d(i):
            b = pymupdf.Rect(i['bbox']) & page.rect
            dx = max(b.x0 - cx, 0, cx - b.x1); dy = max(b.y0 - cy, 0, cy - b.y1)
            penal = 0 if b.y1 <= cy + 40 or b.x1 <= r.x0 + 40 else 150  # foto arriba o a la izquierda
            return (dx * dx + dy * dy) ** .5 + penal
        best = min(imgs, key=d)
        if d(best) > 260: continue
        clip = pymupdf.Rect(best['bbox']) & page.rect
        zoom = 220 / clip.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
        f = OUT / f"tg_{cat}_{pg}_{re.sub(r'[^A-Za-z0-9]+','_',x['codigo'])[:30]}.jpg"
        pix.save(str(f), jpg_quality=70); res[key(x)] = str(f); n_tg += 1
n_c = n_m = 0
for x in rows:
    k = key(x)
    if x['proveedor'] == 'Canguro Panamá' and x['codigo'] in cang: res[k] = cang[x['codigo']]; n_c += 1
    if x['proveedor'] == 'MyTechnologyCR' and x['pagina'] in mt and mt[x['pagina']].exists(): res[k] = str(mt[x['pagina']]); n_m += 1
json.dump(res, open(OUT / 'mapa.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('TechnoGo', n_tg, 'Canguro', n_c, 'MyTech', n_m, 'total', len(res))
