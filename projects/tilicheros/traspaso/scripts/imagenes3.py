"""Segunda pasada: productos de Techno Go sin foto, anclados por el texto de su descripción."""
import csv, re, sys, json
sys.path.append(r'C:\Users\Usuario\AppData\Roaming\Python\Python312\site-packages')
import warnings; warnings.filterwarnings('ignore')
import pymupdf
from pathlib import Path
P = Path(sys.argv[1]); PDFS = Path(sys.argv[2]); T = Path(sys.argv[3])
OUT = T / 'thumbs'; mapa = json.load((OUT / 'mapa.json').open(encoding='utf-8'))
docs = {}
def doc(n):
    if n not in docs: docs[n] = pymupdf.open(str(PDFS / (n + '.pdf')))
    return docs[n]
ok = 0; quedan = []
for x in csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')):
    if x['proveedor'] != 'Techno Go' or x['catalogo'] == '1HORA': continue
    k = '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
    if k in mapa or not (PDFS / (x['catalogo'] + '.pdf')).exists(): continue
    page = doc(x['catalogo'])[int(x['pagina']) - 1]
    words = re.findall(r'[\wÁÉÍÓÚÑáéíóúñ/+.-]+', x['producto'])
    r = None
    for n in (5, 4, 3, 2):
        if len(words) >= n:
            h = page.search_for(' '.join(words[:n]))
            if h: r = h[0]; break
    if r is None and x['codigo'].strip():
        h = page.search_for(x['codigo'].strip()); r = h[0] if h else None
    if r is None: quedan.append((x['catalogo'], x['pagina'], x['producto'][:30])); continue
    imgs = [i for i in page.get_image_info() if 0.02 < (pymupdf.Rect(i['bbox']) & page.rect).get_area() / page.rect.get_area() < 0.40 and i['width'] > 150]
    if not imgs: quedan.append((x['catalogo'], x['pagina'], 'sin imgs')); continue
    cx, cy = (r.x0 + r.x1) / 2, r.y0
    def d(i):
        b = pymupdf.Rect(i['bbox']) & page.rect
        dx = max(b.x0 - cx, 0, cx - b.x1); dy = max(b.y0 - cy, 0, cy - b.y1)
        penal = 0 if b.y1 <= cy + 40 or b.x1 <= r.x0 + 40 else 150
        return (dx * dx + dy * dy) ** .5 + penal
    best = min(imgs, key=d)
    if d(best) > 320: quedan.append((x['catalogo'], x['pagina'], 'lejos')); continue
    clip = pymupdf.Rect(best['bbox']) & page.rect
    pix = page.get_pixmap(matrix=pymupdf.Matrix(220 / clip.width, 220 / clip.width), clip=clip, alpha=False)
    f = OUT / f"tg2_{x['catalogo']}_{x['pagina']}_{ok}.jpg"; pix.save(str(f), jpg_quality=70)
    mapa[k] = str(f); ok += 1
json.dump(mapa, open(OUT / 'mapa.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('nuevas', ok, 'quedan', len(quedan), quedan[:10], 'mapa', len(mapa))
