"""Extrae fichas de los catálogos ORIGINAL de Techno Go.

Cada ficha termina en '(IVA incluido)'; el precio es la línea anterior y, si existe,
'MODELO:' o 'CODIGO:' va antes del precio. Las fichas sin precio o con varios precios
seguidos se marcan para revisión en lugar de adivinarse.
"""
import csv, re, subprocess, sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
PRICE = re.compile(r'^\d{1,3}(\.\d{3})+$')
CODE = re.compile(r'^(MODELO|C[OÓ]DIGO)\s*:?\s*(.+)$', re.I)
SKIP = re.compile(r'^(Precios con IVA incluido|PRECIOS MAYORISTAS.*|CAT[AÁ]LOGO.*|OCTUBRE 2026|SEPTIEMBRE 2026|\d+)$', re.I)
RISK_HIGH = re.compile(r'AIRPODS|EARPODS|APPLE|IPHONE ORIGINAL|CON LOGO|JBL|PS5|PLAYSTATION|GALAXY BUDS|1:1|ESTILO', re.I)
RISK_MED = re.compile(r'IPHONE|SAMSUNG|LIGHTNING|XIAOMI|HUAWEI|ORIGINAL', re.I)

rows = []
for pdf in sorted(src.glob('*.pdf')):
    txt = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(pdf), '-'], capture_output=True, text=True, encoding='utf-8').stdout
    for page_no, page in enumerate(txt.split('\f'), 1):
        # Texto continuo de la página: en orden de lectura el precio queda pegado al modelo o a '(IVA incluido)'.
        flat = ' '.join(l.strip() for l in page.split('\n') if l.strip() and not SKIP.match(l.strip()))
        # Algunos catálogos escriben el precio con letras espaciadas: '₡1 . 2 4 5' o ':8 . 4 7 5'.
        flat = re.sub(r'(₡|:)\s*((?:\d\s*){1,3})\.\s*((?:\d\s*){3})(?!\s*\d)',
                      lambda m: m.group(1) + re.sub(r'\s', '', m.group(2)) + '.' + re.sub(r'\s', '', m.group(3)), flat)
        chunks = re.split(r'\(IVA incluido\)', flat, flags=re.I)[:-1]
        for chunk in chunks:
            # Preferir montos con '₡': así '10.000 MAH' no se toma por precio.
            prices = re.findall(r'₡\s*(\d{1,3}(?:\.\d{3})*)(?![\d.])', chunk) or \
                     re.findall(r'(?<![\d.])(\d{1,3}(?:\.\d{3})+)(?![\d.])', chunk)
            price = prices[-1] if prices else ''
            m = re.search(r'(?:MODELO|C[OÓ]DIGO)\s*:\s*([A-Z0-9][A-Z0-9 ./-]*?)(?=\s*₡|\s*\d{1,3}\.\d{3}|$)', chunk, re.I)
            code = m.group(1).strip() if m else ''
            desc = chunk
            if m: desc = desc.replace(m.group(0), ' ')
            desc = re.sub(r'₡?\s*\d{1,3}(?:\.\d{3})+\s*$', '', desc.strip())
            desc = re.sub(r'[^\w\s.,:;()/+%"\'-]', '', re.sub(r'\s+', ' ', desc)).strip()
            flag = []
            if not price: flag.append('sin precio')
            if len(prices) > 1: flag.append('varios precios en el bloque')
            if not code: flag.append('sin código')
            text = desc + ' ' + code
            risk = 'ALTO' if RISK_HIGH.search(text) else ('MEDIO' if RISK_MED.search(text) else '')
            rows.append([pdf.stem, page_no, code, desc[:220], int(price.replace('.', '')) if price else '', risk, '; '.join(flag)])

with out.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['catalogo', 'pagina', 'modelo_o_codigo', 'descripcion', 'precio_mayorista_con_iva_crc', 'riesgo_marca', 'revisar'])
    w.writerows(rows)

from collections import Counter
c = Counter(r[0] for r in rows)
print('total', len(rows), dict(c))
print('sin precio', sum(1 for r in rows if r[4] == ''), '| varios precios', sum('varios' in r[6] for r in rows), '| sin código', sum('sin código' in r[6] for r in rows))
print('riesgo', Counter(r[5] for r in rows))
