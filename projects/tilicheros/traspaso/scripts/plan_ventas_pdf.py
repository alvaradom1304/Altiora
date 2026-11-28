import csv, math, sys, json, html
from pathlib import Path
P = Path(sys.argv[1]); out = Path(sys.argv[2]); T = Path(sys.argv[3])
IMG = json.load((T / 'thumbs' / 'mapa.json').open(encoding='utf-8')); AGO = set(json.load((T / 'agotados.json').open(encoding='utf-8')))
rows = list(csv.DictReader((P / 'catalogo-proveedores-unificado.csv').open(encoding='utf-8')))
e = html.escape
def k(x): return '|'.join([x['proveedor'], x['catalogo'], x['pagina'], x['codigo'], x['producto']])
def find(cat, pag, cod):
    for r in rows:
        if r['catalogo'] == cat and r['pagina'] == pag and cod.upper() in (r['codigo'] + ' ' + r['producto']).upper(): return r
    raise SystemExit('no encontrado ' + str((cat, pag, cod)))
def img(x):
    f = IMG.get(k(x)); return ('<img src="file:///' + f.replace('\\', '/') + '" height=64>') if f else ''
def money(v): return '₡' + f"{int(v):,}".replace(',', ' ')
def lanz(c, p):
    base = max(c * 1.35, (p or 0) * 0.6)
    return int(math.ceil(base / 100.0) * 100)
# (grupo, etiqueta, ref, por qué, señal de demanda)
G = 'Gancho: entrada de bajo precio para conseguir primeras ventas'
E_ = 'Estrella: tráfico y consultas'
N = 'Navidad / regalos'
SEL = [
 (G, 'Audífonos con cable 3.5 mm AUT123', ('1HORA', '2', 'AUT123N'), 'Precio de impulso; fácil de enviar', 'Chile 1.er semestre 2026: audífonos con cable duplicaron ventas (indirecta)'),
 (G, 'Audífonos tipo C AUT128 (varios colores)', ('1HORA', '2', 'AUT128N'), 'Compatibles con celulares sin entrada 3.5 mm', 'Chile 2026: audífonos con cable en alza (indirecta)'),
 (G, 'Soporte magnético para celular PJ033', ('1HORA', '19', 'PJ033N'), 'Se entiende en 3 segundos en un video corto', 'TikTok Shop 2026: soportes y cargadores magnéticos (blogs, sesgados)'),
 (G, 'Soporte para celular PJ093', ('1HORA', '19', 'PJ093N'), 'Gancho barato para carro y escritorio', 'Accesorios de celular y auto: tendencia en listas TikTok 2026'),
 (G, 'Aro de luz LED 26 cm MJ26', ('INNOVACION', '27', 'MJ26'), 'Muy demostrable en video; sirve a quien vende por redes', 'TikTok Shop Q2 2026: aros de luz (blogs, sesgados)'),
 (G, 'Selfie stick Q07', ('INNOVACION', '8', 'Q07'), 'Precio de impulso, uso inmediato', 'Accesorios de grabación: tendencia (indirecta)'),
 (E_, 'Dispensador de agua automático DPA002', ('1HORA', '20', 'DPA002B'), 'Producto «wow» para video; ticket medio', 'TikTok Shop 2026: dispensadores automáticos (blogs, sesgados)'),
 (E_, 'Bocina inalámbrica 20 W', ('1HORA', '21', 'BOC250N'), 'Regalo fácil; audio inalámbrico es la categoría líder en la región', 'Colombia 2026: audífonos y audio inalámbrico lideran tecnología (indirecta)'),
 (E_, 'Batería portátil 10 000 mAh PD 22.5 W', ('1HORA', '12', 'GAR264N'), 'Necesidad real; fácil de comparar por precio', 'Accesorios de carga: categoría recurrente (indirecta)'),
 (E_, 'Batería portátil 20 000 mAh PD 22.5 W', ('1HORA', '13', 'BAT201N'), 'Mayor ticket con alto valor percibido', 'Ídem'),
 (E_, 'Reloj inteligente V11 Pro', ('INNOVACION', '3', '001570'), 'Smartwatch es de lo más comprado en la región', 'Colombia 2026: relojes inteligentes (indirecta)'),
 (E_, 'Micrófono inalámbrico KMP-171', ('KOOSDA', '9', 'KMP-171'), 'Creadores de contenido; demostrable', 'TikTok Shop 2026: micrófonos inalámbricos mini (blogs, sesgados)'),
 (N, 'Reloj infantil 3 en 1 Y9', ('INNOVACION', '6', '001957'), 'Regalo para niños', 'Temporada: Navidad (sin dato específico de CR)'),
 (N, 'Cámara Wi-Fi doble lente JT-8292', ('JORTAN', '6', 'JT-8292'), 'Regalo útil para el hogar; costo bajo para el tipo de producto', 'Sin señal propia: la elijo por precio y utilidad, no por dato de demanda'),
]
H = ['<meta charset=utf-8><style>@page{size:A4;margin:14mm}body{font:10pt "Segoe UI",Arial;color:#141212}h1{font-size:26pt;margin:0;color:#c4161c}h2{background:#141212;color:#f2e9d8;padding:5px 9px;font-size:12.5pt;margin:14px 0 6px;break-after:avoid}table{width:100%;border-collapse:collapse;font-size:8.6pt}th{background:#f2e9d8;text-align:left;padding:3px 5px}td{border-bottom:1px solid #ddd;padding:4px 5px;vertical-align:middle}td.n,th.n{text-align:right;white-space:nowrap}.nota{background:#fff4d6;border-left:4px solid #c4161c;padding:7px 10px;margin:8px 0}.sm{color:#666;font-size:8pt}tr{break-inside:avoid}.pb{break-before:page}img{max-width:80px;object-fit:contain}</style>']
H.append('<h1>El Tilichero CR</h1><p><b>Plan de ventas: productos para darnos a conocer</b> · 4 de noviembre de 2026</p>')
H.append('<div class=nota><b>Criterio.</b> Ventas y visibilidad primero; la rentabilidad no es el filtro. Elegí productos de <b>precio de impulso</b>, fáciles de mostrar en un video corto, con disponibilidad y bajo costo de envío. Los precios de lanzamiento son <b>propuestas</b> calculadas sobre el costo mayorista real de Techno Go (mínimo costo + 35 %, o 60 % del precio sugerido si lo hay).</div>')
H.append('<div class=nota><b>Qué sé de la demanda y qué no.</b> No encontré ningún ranking público verificado de ventas en Costa Rica para 2026. Lo que hay son <b>señales regionales indirectas</b> (Chile, Colombia) y listas de tendencias de TikTok Shop escritas por blogs y agencias, que pueden estar sesgadas. Por eso cada producto muestra su señal y su tipo. <b>La demanda real en Costa Rica solo se confirma vendiendo</b>: por eso el plan es una prueba corta y medible.</div>')
H.append('<div class=nota><b>Datos que faltan del dueño:</b> comisión de Vintta y costo de envío (para fijar el precio mínimo con el que no se pierde dinero), stock y garantía de cada producto con Techno Go, y cuánto está dispuesto a subsidiar por venta.</div>')
cur = None
for g, et, ref, why, sig in SEL:
    r = find(*ref); c = int(r['costo_mayorista_crc']); p = int(r['pvp_sugerido_proveedor_crc']) if r['pvp_sugerido_proveedor_crc'] else None
    if g != cur:
        if cur: H.append('</table>')
        H.append(f'<h2>{e(g)}</h2><table><tr><th>Foto</th><th>Producto</th><th class=n>Costo</th><th class=n>Lanzamiento</th><th class=n>Precio normal*</th><th>Por qué</th><th>Señal de demanda</th></tr>'); cur = g
    ago = ' <b style="color:#c4161c">(AGOTADO)</b>' if k(r) in AGO else ''
    H.append(f"<tr><td>{img(r)}</td><td><b>{e(et)}</b>{ago}<br><span class=sm>{e(r['catalogo'])} p.{r['pagina']} · {e(r['codigo'])}</span></td><td class=n>{money(c)}</td><td class=n><b>{money(lanz(c, p))}</b></td><td class=n>{money(p) if p else '—'}</td><td>{e(why)}</td><td class=sm>{e(sig)}</td></tr>")
H.append('</table><p class=sm>*Precio sugerido por el proveedor (solo catálogo 1HORA). Costos y precios con IVA incluido, octubre 2026. Confirmar stock antes de publicar.</p>')
H.append('<div class=pb></div><h2>Plan de 3 semanas (hasta el Black Friday)</h2><ol><li><b>Semana 1:</b> publicar 6 ganchos en Vintta con foto y precio de lanzamiento; un Reel corto por producto (el producto en la primera línea y qué hacer: «pídelo por Vintta o WhatsApp»).</li><li><b>Semana 2:</b> sumar las estrellas que tengan stock confirmado; repetir el Reel que más alcance tenga. Poner una oferta clara de combo (por ejemplo, gancho + estrella).</li><li><b>Semana 3 (Black Friday, 27 de noviembre según fuentes internacionales; confirmar la fecha en Costa Rica):</b> empujar los que ya vendieron; retirar los que no.</li><li><b>Medir por producto:</b> visitas, consultas por WhatsApp y pedidos. Decidir por los números, no por esta lista.</li></ol>')
H.append('<h2>Lo que veo en lo que ya tiene El Tilichero</h2><p>El Reel R2 llegó a 2 414 cuentas pero solo generó 5 visitas al perfil: el alcance no es el problema, sino que el video no dice qué se vende ni qué hacer. Los productos de esta lista ayudan porque se explican solos en 3 segundos. Fuente: estadísticas de la sesión del dueño (4 de noviembre).</p>')
H.append('<h2>Mi opinión sobre «sin importar la rentabilidad»</h2><p><b>Aporta valor si</b> se pone un tope: vender barato para conseguir las primeras ventas, reseñas y seguidores sirve cuando se sabe cuánto se está dispuesto a perder por pedido. <b>Entorpece si</b> el precio queda por debajo de costo + comisión de Vintta + envío: cada venta resta dinero y subir el volumen agranda la pérdida. Alternativa corta: fijar un precio mínimo por producto y una cantidad máxima de unidades a precio de lanzamiento. La decisión es del dueño.</p>')
H.append('<h2>Pendiente: marcas y réplicas validadas por el dueño</h2><p>Los AirPods-style, Galaxy Buds-style, JBL-style, Pencil y control PS5 no entran en este ranking porque <b>no tienen costo</b> (MyTechnologyCR no publica precios). Con su lista mayorista se evalúan igual. Un dato local: el Reel R4 con una caja tipo AirPods llegó a 62 vistas y 1 me gusta, lo que no indica demanda por sí solo, porque dependió del video.</p>')
H.append('<p class=sm>Fuentes de las señales de demanda: WOM Chile, ranking de productos tecnológicos del primer semestre de 2026 (eldinamo.cl); Tiendanube Colombia 2026; listas de tendencias de TikTok Shop 2026 (hypersku.com, echotik.live y otras, de proveedores y agencias); Back Market (fecha del Black Friday 2026). Ninguna es de Costa Rica.</p>')
out.write_text(''.join(H), encoding='utf-8'); print('ok', len(SEL))
