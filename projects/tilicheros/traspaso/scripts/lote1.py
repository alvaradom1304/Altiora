import csv, json, sys, shutil
from pathlib import Path
S = Path(sys.argv[1]); R = Path(sys.argv[2])   # scratchpad, projects/tilicheros
m = json.load((S / 'thumbs' / 'mapa.json').open(encoding='utf-8'))
L = [
 ('AUT123N', '1HORA', 'Audífonos con cable 3.5 mm 1Hora AUT123 - Negro', 'Electrónicos', 2500, 'Audífonos con cable y conector de 3.5 mm, color negro. Compatibles con celulares, tablets y computadoras con entrada de audio de 3.5 mm.', ['Conector: 3.5 mm', 'Color: negro', 'Tipo: con cable']),
 ('AUT128N', '1HORA', 'Audífonos con cable USB tipo C 1Hora AUT128 - Negro', 'Electrónicos', 3500, 'Audífonos con cable y conector USB tipo C, color negro. Para celulares y tablets con entrada tipo C.', ['Conector: USB tipo C', 'Color: negro', 'Tipo: con cable']),
 ('AUT119P', '1HORA', 'Audífonos inalámbricos Bluetooth 1Hora AUT119', 'Electrónicos', 9900, 'Audífonos inalámbricos con conexión Bluetooth.', ['Conexión: Bluetooth', 'Tipo: inalámbricos']),
 ('BOC062N', '1HORA', 'Bocina Bluetooth pequeña 1Hora BOC062 - Negro', 'Electrónicos', 9900, 'Bocina Bluetooth portátil pequeña, color negro.', ['Conexión: Bluetooth', 'Color: negro']),
 ('CAB265N', '1HORA', 'Cable USB tipo C a tipo C 60 W trenzado 1 m 1Hora CAB265', 'Electrónicos', 3500, 'Cable de carga USB tipo C a tipo C, trenzado, de 1 metro, con carga de hasta 60 W y 3 A.', ['Largo: 1 m', 'Potencia: hasta 60 W / 3 A', 'Conectores: tipo C a tipo C', 'Cubierta: trenzada']),
 ('GAR152N', '1HORA', 'Cubo cargador de pared USB tipo C PD 20 W 1Hora GAR152 - Negro', 'Electrónicos', 5900, 'Cubo cargador de pared con carga rápida PD de 20 W, color negro.', ['Potencia: PD 20 W', 'Color: negro']),
 ('PJ033N', '1HORA', 'Soporte magnético para celular 1Hora PJ033 - Negro', 'Electrónicos', 4900, 'Soporte magnético para celular, color negro.', ['Tipo: magnético', 'Color: negro']),
 ('PJ093N', '1HORA', 'Soporte para celular 1Hora PJ093 - Negro', 'Electrónicos', 3900, 'Soporte para celular, color negro.', ['Color: negro']),
 ('DPA002B', '1HORA', 'Dispensador de agua automático - Blanco', 'Hogar', 14900, 'Dispensador de agua automático, color blanco.', ['Color: blanco', 'Tipo: automático']),
 ('001570', 'INNOVACION', 'Reloj inteligente V11 Pro con pantalla táctil y Bluetooth', 'Electrónicos', 17900, 'Reloj inteligente con pantalla táctil y conexión Bluetooth.', ['Pantalla: táctil', 'Conexión: Bluetooth']),
]
rows = {(x['catalogo'], x['codigo']): x for x in csv.DictReader((R / 'proveedores' / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8'))}
dst = R / 'vintta' / 'lote-1'; dst.mkdir(parents=True, exist_ok=True)
out = []; md = ['# Vintta · lote 1 (propuesta, nada publicado)\n', 'Estado: **borrador para aprobación**. Precios propuestos (colones, IVA incluido). Stock: pendiente del dueño. Fotos: recortes de los PDF del proveedor; se recomienda pedir originales.\n']
for i, (cod, cat, t, c, p, d, sp) in enumerate(L, 1):
    x = rows[(cat, cod)]
    key = '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
    f = m.get(key); fn = ''
    if f and Path(f).exists():
        fn = f"{i:02d}-{cod}.jpg"; shutil.copy(f, dst / fn)
    cost = int(x['costo_mayorista_crc'])
    out.append([i, t, c, 'Nuevo', p, cost, '', cod, f"{x['catalogo']} p.{x['pagina']}", fn, d, ' | '.join(sp)])
    md.append(f"## {i}. {t}\n- Categoría: {c} · Estado: Nuevo · **Precio propuesto: ₡{p:,}** (costo ₡{cost:,}) · Stock: *a definir*\n- Descripción: {d}\n- Especificaciones: {'; '.join(sp)}\n- Proveedor: Techno Go · {x['catalogo']} p.{x['pagina']} · código {cod} · foto: `{fn or 'sin foto'}`\n")
w = csv.writer((dst / 'lote-1.csv').open('w', newline='', encoding='utf-8'))
w.writerow(['n', 'titulo', 'categoria', 'estado', 'precio_propuesto_crc', 'costo_crc', 'stock', 'codigo_proveedor', 'proveedor_pagina', 'foto', 'descripcion', 'especificaciones'])
w.writerows(out)
(dst / 'lote-1.md').write_text('\n'.join(md), encoding='utf-8')
print(len(out), [o[9] for o in out])
