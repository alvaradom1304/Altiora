import csv, json, re, sys, shutil
from pathlib import Path
S = Path(sys.argv[1]); R = Path(sys.argv[2])
m = json.load((S / 'thumbs' / 'mapa.json').open(encoding='utf-8'))
rows = list(csv.DictReader((R / 'proveedores' / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
def find(prov, **kw):
    for x in rows:
        if not x['proveedor'].startswith(prov): continue
        if all(re.search(v, x[k], re.I) for k, v in kw.items()): return x
    raise SystemExit('no encontrado ' + str((prov, kw)))
def clean(t, n=380):
    t = re.sub(r'\s+', ' ', t).strip(); t = re.sub(r'(?<=\b[A-Z]) (?=[A-Z]\b)', '', t)
    t = t[:1] + t[1:].lower() if t.isupper() else t
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'
LOTES = {
 'lote-2-juguetes': ('Lote 2 · Juguetes y regalos para niños (Navidad)', [
   ('Canguro', dict(codigo='^37010066$'), 'Drone plegable P30 con cámara 4K HD y control con pantalla (2 baterías)', 'Juguetes'),
   ('Canguro', dict(codigo='^37010071$'), 'Carro con control remoto 2.4 GHz con estación de carga', 'Juguetes'),
   ('Canguro', dict(codigo='^37010290$'), 'Carro de control remoto de policía, alta velocidad', 'Juguetes'),
   ('Canguro', dict(codigo='^37010070$'), 'Carro de acrobacias con giro de 360° y luces en las llantas', 'Juguetes'),
   ('Canguro', dict(codigo='^37010272$'), 'Carro transformable Bumblebee', 'Juguetes'),
   ('Canguro', dict(codigo='^37010295$'), 'Carro transformable en robot', 'Juguetes'),
   ('Canguro', dict(codigo='^37010300$'), 'Scooter para niño ADB 306', 'Juguetes'),
   ('Canguro', dict(codigo='^37010309$'), 'Muñeca Lovely Baby', 'Juguetes'),
   ('Canguro', dict(codigo='^37010248$'), 'Kit de dibujo para niños, 156 piezas', 'Juguetes'),
   ('Canguro', dict(codigo='^37010112$'), 'Robot puzzle 3 en 1 con control remoto y app', 'Juguetes')]),
 'lote-3-regalos-tecnologia': ('Lote 3 · Regalos de tecnología (Navidad)', [
   ('Techno Go', dict(codigo='^001957$'), 'Reloj inteligente infantil 3 en 1 Y9 con cámara', 'Electrónicos'),
   ('Techno Go', dict(codigo='^001958$'), 'Cámara digital compacta M05 con pantalla a color', 'Electrónicos'),
   ('Techno Go', dict(codigo='^001917$'), 'Audífonos inalámbricos 895B con cancelación de ruido', 'Electrónicos'),
   ('Techno Go', dict(codigo='^001905$'), 'Audífonos inalámbricos Pro 5S', 'Electrónicos'),
   ('Techno Go', dict(codigo='^DT-069$'), 'Audífonos de diadema inalámbricos DADU DT-069', 'Electrónicos'),
   ('Techno Go', dict(codigo='^BOC243N$'), 'Bocina inalámbrica redonda en tela - Negro', 'Electrónicos'),
   ('Techno Go', dict(codigo='^GM201$'), 'Mouse inalámbrico recargable de doble modo GM201', 'Electrónicos'),
   ('Techno Go', dict(codigo='^CONTROL PS4$'), 'Control inalámbrico compatible con PS4, PC y celular (sin logo)', 'Electrónicos'),
   ('Techno Go', dict(codigo='^FS-260-6$'), 'Aro de luz RGB de 26 cm FS-260-6', 'Electrónicos'),
   ('Techno Go', dict(producto='^KMP-171'), 'Micrófono inalámbrico/alámbrico con cancelación de ruido y luces RGB KMP-171', 'Electrónicos')]),
 'lote-4-marcas-y-estilo-marca': ('Lote 4 · Marcas y estilo marca (validados por el dueño)', [
   ('MyTech', dict(pagina='^51$'), 'Audífonos inalámbricos con estuche (3.ª generación)', 'Electrónicos'),
   ('MyTech', dict(pagina='^52$'), 'Audífonos inalámbricos con estuche (4.ª generación)', 'Electrónicos'),
   ('MyTech', dict(pagina='^53$'), 'Audífonos inalámbricos Pro con estuche', 'Electrónicos'),
   ('MyTech', dict(pagina='^57$'), 'Audífonos inalámbricos Pro con estuche (estilo Galaxy Buds)', 'Electrónicos'),
   ('MyTech', dict(pagina='^58$'), 'Audífonos de diadema inalámbricos', 'Electrónicos'),
   ('MyTech', dict(pagina='^81$'), 'Reloj inteligente Pulso Ultra', 'Electrónicos'),
   ('MyTech', dict(pagina='^107$'), 'Lápiz óptico para tablet (2.ª generación)', 'Electrónicos'),
   ('MyTech', dict(pagina='^117$'), 'Parlante Bluetooth portátil (estilo JBL Go)', 'Electrónicos'),
   ('MyTech', dict(pagina='^118$'), 'Parlante Bluetooth portátil con clip (estilo JBL Clip)', 'Electrónicos'),
   ('MyTech', dict(pagina='^121$'), 'Control inalámbrico compatible con PS5', 'Electrónicos')])}
out = R / 'vintta' / 'navidad'; out.mkdir(parents=True, exist_ok=True)
summ = {}
for slug, (titulo, items) in LOTES.items():
    d = out / slug; d.mkdir(exist_ok=True)
    md = [f'# {titulo}\n', 'Estado: **borrador, sin precios**. Vintta exige precio e inventario para publicar; no hay modo borrador (ver nota en el chat). Precio: *lo define el dueño*. Stock: *a definir*. Fotos: recortes de los PDF de proveedores; conviene pedir originales.\n']
    csvr = []
    for i, (prov, kw, tit, cat) in enumerate(items, 1):
        x = find(prov, **kw)
        key = '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
        f = m.get(key); fn = ''
        if f and Path(f).exists(): fn = f"{i:02d}.jpg"; shutil.copy(f, d / fn)
        raw = x['producto'].split(' / ')[-1] if prov == 'Canguro' and ' / ' in x['producto'] else x['producto']
        desc = clean(raw) if prov != 'MyTech' else 'Ver fotos del producto. (Descripción a completar con el proveedor.)'
        csvr.append([i, tit, cat, 'Nuevo', '', '', x['proveedor'], f"{x['catalogo']} p.{x['pagina']}" if x['pagina'] else x['catalogo'], x['codigo'], fn, desc])
        md.append(f"## {i}. {tit}\n- Categoría: {cat} · Estado: Nuevo · Precio: *a definir* · Stock: *a definir*\n- Descripción (tomada del catálogo del proveedor): {desc}\n- Proveedor: {x['proveedor']} · {x['catalogo']}{(' p.' + x['pagina']) if x['pagina'] else ''} · código {x['codigo'] or '—'} · foto: `{fn or 'sin foto'}`\n")
    (d / f'{slug}.md').write_text('\n'.join(md), encoding='utf-8')
    w = csv.writer((d / f'{slug}.csv').open('w', newline='', encoding='utf-8'))
    w.writerow(['n', 'titulo', 'categoria', 'estado', 'precio', 'stock', 'proveedor', 'catalogo_pagina', 'codigo', 'foto', 'descripcion']); w.writerows(csvr)
    summ[slug] = len(csvr)
print(summ)
