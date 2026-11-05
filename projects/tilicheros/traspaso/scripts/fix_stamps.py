"""Reemplaza miniaturas que eran solo el sello AGOTADO por la foto real más cercana; consolida lista AGOTADO."""
import csv, re, sys, json
sys.path.append(r'C:\Users\Usuario\AppData\Roaming\Python\Python312\site-packages')
import warnings; warnings.filterwarnings('ignore')
import pymupdf
from pathlib import Path
P = Path(sys.argv[1]); PDFS = Path(sys.argv[2]); T = Path(sys.argv[3]); OUT = T / 'thumbs'
mapa = json.load((OUT / 'mapa.json').open(encoding='utf-8'))
rojo = {Path(f).name: a for a, f in json.load((OUT / 'rojo.json').open())}
ago = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
def redfrac(pm):
    s = pm.samples; n = pm.n; t = r = 0
    for k in range(0, len(s), n * 3):
        t += 1
        if s[k] > 170 and s[k + 1] < 70 and s[k + 2] < 70: r += 1
    return r / max(t, 1)
docs = {}
def doc(n):
    if n not in docs: docs[n] = pymupdf.open(str(PDFS / (n + '.pdf')))
    return docs[n]
rows = {'|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']]): x
        for x in csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8'))}
fixed = removed = poster = 0
for k, f in list(mapa.items()):
    nm = Path(f).name
    a = rojo.get(nm, 0)
    if not nm.startswith('tg'): continue
    if a >= 0.18 or (a >= 0.12 and 'HOPESTAR' not in nm):
        ago.add(k)
        if 'HOPESTAR' in nm: poster += 1; continue
        x = rows[k]
        page = doc(x['catalogo'])[int(x['pagina']) - 1]
        words = re.findall(r'[\wÁÉÍÓÚÑáéíóúñ/+.-]+', x['producto']); r = None
        if x['codigo'].strip():
            h = page.search_for(x['codigo'].strip()); r = h[0] if h else None
        if r is None:
            for n in (5, 4, 3, 2, 1):
                if len(words) >= n:
                    h = page.search_for(' '.join(words[:n]))
                    if h: r = h[0]; break
        cands = []
        for i in page.get_image_info():
            b = pymupdf.Rect(i['bbox']) & page.rect
            if b.is_empty or i['width'] < 60 or not (0.004 < b.get_area() / page.rect.get_area() < 0.7): continue
            pm = page.get_pixmap(matrix=pymupdf.Matrix(.2, .2), clip=b, alpha=False)
            if redfrac(pm) >= 0.10: continue
            cands.append((i, b))
        if r is None or not cands: del mapa[k]; removed += 1; continue
        cx, cy = (r.x0 + r.x1) / 2, r.y0
        def d(c):
            b = c[1]; dx = max(b.x0 - cx, 0, cx - b.x1); dy = max(b.y0 - cy, 0, cy - b.y1)
            return (dx * dx + dy * dy) ** .5 + (0 if b.y1 <= cy + 40 or b.x1 <= r.x0 + 40 else 150)
        best = min(cands, key=d)
        if d(best) > 600: del mapa[k]; removed += 1; continue
        clip = best[1]
        pm = page.get_pixmap(matrix=pymupdf.Matrix(220 / clip.width, 220 / clip.width), clip=clip, alpha=False)
        g = OUT / f"fx_{fixed}.jpg"; pm.save(str(g), jpg_quality=70); mapa[k] = str(g); fixed += 1
json.dump(mapa, open(OUT / 'mapa.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(sorted(ago), open(T / 'agotados.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('reemplazadas', fixed, 'sin foto', removed, 'posters con sello', poster, 'agotados', len(ago), 'mapa', len(mapa))
