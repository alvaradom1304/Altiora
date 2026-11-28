import json, sys, time, urllib.parse, urllib.request, gzip
from pathlib import Path
out = Path(sys.argv[1])
TERMS = ['audifonos inalambricos', 'audifonos', 'audifonos bluetooth', 'parlante bluetooth', 'bocina', 'smartwatch', 'reloj inteligente', 'power bank', 'bateria portatil', 'cargador celular', 'cable usb', 'cable tipo c', 'soporte celular', 'tripode celular', 'selfie', 'aro de luz', 'microfono', 'mouse inalambrico', 'teclado', 'control ps5', 'control ps4', 'consola', 'audifonos gamer', 'camara de seguridad', 'camara wifi', 'juguete', 'carro control remoto', 'scooter', 'drone', 'kit dibujo', 'muneca', 'dispensador agua', 'regleta', 'ventilador portatil', 'cepillo electrico', 'airpods', 'jbl', 'apple pencil', 'memoria usb', 'funda celular', 'protector pantalla', 'lampara led', 'tablet', 'cargador carro']
res = {}
for t in TERMS:
    url = 'https://www.walmart.co.cr/api/catalog_system/pub/products/search?' + urllib.parse.urlencode({'ft': t, 'O': 'OrderByTopSaleDESC', '_from': 0, '_to': 19}, quote_via=urllib.parse.quote)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            b = r.read()
            if r.headers.get('Content-Encoding') == 'gzip': b = gzip.decompress(b)
            lst = json.loads(b.decode('utf-8'))
            tot = r.headers.get('resources', '')
    except Exception as ex:
        print('fallo', t, ex); res[t] = {'total': None, 'items': []}; continue
    items = []
    for p in lst:
        try:
            it = p['items'][0]; sl = it['sellers'][0]; co = sl['commertialOffer']
            items.append(dict(n=p.get('productName'), b=p.get('brand'), price=co.get('Price'), list=co.get('ListPrice'), stock=co.get('AvailableQuantity'), seller=sl.get('sellerName'), cat=(p.get('categories') or [''])[0], link=p.get('link')))
        except Exception:
            pass
    res[t] = {'total': tot, 'items': items}
    print(t, tot, len(items)); time.sleep(0.6)
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
