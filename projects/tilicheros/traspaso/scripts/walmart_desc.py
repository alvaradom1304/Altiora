import json, sys, time, urllib.parse, urllib.request, gzip, re
from pathlib import Path
out = Path(sys.argv[1])
TERMS = ['audifonos inalambricos', 'audifonos bluetooth', 'parlante bluetooth', 'smartwatch', 'mouse inalambrico', 'camara digital', 'carro control remoto', 'scooter', 'muneca', 'microfono', 'soporte celular', 'cable usb', 'power bank', 'juguete', 'drone']
res = {}
for t in TERMS:
    url = 'https://www.walmart.co.cr/api/catalog_system/pub/products/search?' + urllib.parse.urlencode({'ft': t, 'O': 'OrderByTopSaleDESC', '_from': 0, '_to': 7}, quote_via=urllib.parse.quote)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            b = r.read()
            if r.headers.get('Content-Encoding') == 'gzip': b = gzip.decompress(b)
            lst = json.loads(b.decode('utf-8'))
    except Exception as ex:
        print('fallo', t, ex); continue
    items = []
    for p in lst:
        try:
            co = p['items'][0]['sellers'][0]['commertialOffer']
            if not (co.get('Price') or 0) > 0: continue
            if any(x in (p.get('categories') or [''])[0] for x in ('Farmacia', 'Higiene', 'Bebes', 'Alimentos')): continue
            spec = {k: p.get(k) for k in (p.get('allSpecifications') or [])[:12]}
            items.append(dict(title=p.get('productName'), brand=p.get('brand'), price=co['Price'], desc=re.sub(r'<[^>]+>', ' ', p.get('description') or '')[:700], spec=spec))
        except Exception:
            pass
    res[t] = items[:5]; print(t, len(items)); time.sleep(.5)
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
