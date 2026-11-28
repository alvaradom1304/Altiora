import csv, re, sys, json
sys.path.append(r'C:\Users\Usuario\AppData\Roaming\Python\Python312\site-packages')
import warnings; warnings.filterwarnings('ignore')
import pymupdf
from pathlib import Path
P = Path(sys.argv[1]); PDF = Path(sys.argv[2]); T = Path(sys.argv[3])
OUT = T / 'thumbs'; OUT.mkdir(exist_ok=True)
mapa = json.load((OUT / 'mapa.json').open(encoding='utf-8'))
rows = [x for x in csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')) if x['catalogo'] == '1HORA']
d = pymupdf.open(str(PDF))
cache = {}; ok = miss = 0; faltan = []
for x in rows:
    pg = int(x['pagina']); page = d[pg - 1]
    imgs = [i for i in page.get_image_info() if 60 < i['width'] < 600 and abs(i['bbox'][2] - i['bbox'][0]) < 200]
    hits = page.search_for(x['codigo'].strip()) if len(x['codigo'].strip()) >= 3 else []
    if not hits or not imgs:
        miss += 1; faltan.append((pg, x['codigo'])); continue
    r = hits[0]; cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
    def dist(i):
        b = pymupdf.Rect(i['bbox']); return ((b.x0 + b.x1) / 2 - cx) ** 2 + ((b.y0 + b.y1) / 2 - cy) ** 2
    best = min(imgs, key=dist)
    kb = (pg, tuple(round(v) for v in best['bbox']))
    if kb not in cache:
        clip = pymupdf.Rect(best['bbox']) & page.rect
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip, alpha=False)
        f = OUT / f"h_{pg}_{len(cache)}.jpg"; pix.save(str(f), jpg_quality=75); cache[kb] = str(f)
    mapa['|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])] = cache[kb]; ok += 1
json.dump(mapa, open(OUT / 'mapa.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('1HORA ok', ok, 'sin foto', miss, faltan[:15], 'total mapa', len(mapa))
