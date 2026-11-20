import json, sys, time, urllib.parse, urllib.request, gzip
from pathlib import Path
out = Path(sys.argv[1])
TERMS = ['1hora', '1 hora', 'dadu', 'jortan', 'koosda', 'mikuso', 'hopestar', 'fengqi', 'umipro', 'technogo', 'xo', 'onikuma', 'tuqin', 'vidvie', 'byyo', 'argom', 'durabrand', 'klip xtreme', 'xtech', 'devia', 'trust', 'unno tekno', 'imou', 'tapo', 'ezviz']
def get(term, a, b):
    url = 'https://www.walmart.co.cr/api/catalog_system/pub/products/search?' + urllib.parse.urlencode({'ft': term, 'O': 'OrderByTopSaleDESC', '_from': a, '_to': b}, quote_via=urllib.parse.quote)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'})
    with urllib.request.urlopen(req, timeout=30) as r:
        x = r.read()
        if r.headers.get('Content-Encoding') == 'gzip': x = gzip.decompress(x)
        return json.loads(x.decode('utf-8')), r.headers.get('resources', '')
res = {}
for t in TERMS:
    items = []; tot = ''
    for a in (0, 50):
        try:
            lst, tot = get(t, a, a + 49)
        except Exception as ex:
            break
        for rank, p in enumerate(lst, a + 1):
            try:
                it = p['items'][0]; sl = it['sellers'][0]; co = sl['commertialOffer']
                items.append(dict(rank=rank, n=p.get('productName'), b=p.get('brand'), ref=p.get('productReference'), price=co.get('Price'), stock=co.get('AvailableQuantity'), seller=sl.get('sellerName'), cat=(p.get('categories') or [''])[0]))
            except Exception: pass
        if len(lst) < 50: break
        time.sleep(.5)
    res[t] = {'total': tot, 'items': items}; print(t, tot, len(items)); time.sleep(.5)
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
