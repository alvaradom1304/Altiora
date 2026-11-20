"""Une los catálogos de proveedores de El Tilichero en un solo CSV con la misma estructura."""
import csv, sys
from pathlib import Path

P = Path(sys.argv[1])
def rd(name): return list(csv.DictReader((P / name).open(encoding='utf-8')))

cols = ['proveedor', 'catalogo', 'pagina', 'codigo', 'producto', 'costo_mayorista_crc', 'pvp_sugerido_proveedor_crc',
        'precio_catalogo_sin_tipo_crc', 'riesgo_marca', 'fuente']
rows = []
for r in rd('mytechnologycr-indice.csv'):
    if r['categoria'] == 'Portada': continue
    rows.append(['MyTechnologyCR', 'Catalogo_sin_precios', r['pagina'], '', r['producto'], '', '', '',
                 r['riesgo_marca'].split(':')[0], 'PDF local, sin precios'])
for r in rd('canguro-catalogo.csv'):
    rows.append(['Canguro Panamá', r['categoria'], '', r['codigo'], r['producto'], '', '', r['precio_catalogo_crc'],
                 'MEDIO' if any(k in r['producto'] for k in ('LAMBORGHINI', 'MASERATI', 'MCLAREN', 'BUMBLEBEE')) else '',
                 'Catálogo qvix; no indica si el precio es mayorista'])
for r in rd('technogo-1hora.csv'):
    risk = 'MEDIO' if any(k in r['producto'] for k in ('IPHONE', 'LIGHTNING')) else ''
    rows.append(['Techno Go', '1HORA', r['pagina'], r['codigo'], r['producto'], r['mayoreo_con_iva_crc'],
                 r['pvp_sugerido_crc'], '', risk, 'PDF Drive: mayoreo con IVA + PVP sugerido'])
for r in rd('technogo-marcas-original.csv'):
    rows.append(['Techno Go', r['catalogo'], r['pagina'], r['modelo_o_codigo'], r['descripcion'],
                 r['precio_mayorista_con_iva_crc'], '', '', r['riesgo_marca'], 'PDF Drive: precios mayoristas con IVA'])

with (P / 'catalogo-proveedores-unificado.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(rows)

from collections import Counter
print('filas', len(rows))
print('por proveedor', Counter(r[0] for r in rows))
print('con costo', sum(1 for r in rows if r[5]), '| con PVP', sum(1 for r in rows if r[6]), '| riesgo', Counter(r[8] for r in rows))
