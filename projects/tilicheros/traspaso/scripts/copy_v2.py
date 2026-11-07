import json, sys
from pathlib import Path
R = Path(sys.argv[1])  # projects/tilicheros/vintta
FOOT = 'Envío a todo Costa Rica con Vintta. Pago con SINPE Móvil, transferencia o efectivo contra entrega.'
def d(hook, bullets, extra=''):
    t = hook + '\n\nCaracterísticas:\n' + '\n'.join('• ' + b for b in bullets)
    if extra: t += '\n\n' + extra
    return t + '\n\n' + FOOT
KIDS = 'Un regalo de Navidad para niños.'
P = [
 # lote 2 · Canguro
 ('Drone plegable con cámara 4K HD y control con pantalla P30 (2 baterías)', d('Drone plegable con cámara 4K HD, pensado para quienes empiezan a volar. Incluye control con pantalla y 2 baterías.', ['Cámara 4K HD', 'Plegable', 'Control con pantalla', '2 baterías incluidas', 'Para principiantes'], 'Un regalo de Navidad para aficionados a la tecnología.')),
 ('Carro a control remoto 2.4 GHz con estación de carga', d('Carro a control remoto con estación de carga, en blanco y turquesa.', ['Control remoto 2.4 GHz', 'Con estación de carga', 'Colores: blanco y turquesa'], KIDS)),
 ('Carro a control remoto de policía, alta velocidad', d('Carro de policía a control remoto, de alta velocidad y acabado tornasol.', ['Control remoto', 'Diseño de policía', 'Alta velocidad'], KIDS)),
 ('Carro de acrobacias a control remoto con giro de 360° y luces en las llantas', d('Carro de acrobacias que gira 360° y enciende luces en las llantas.', ['Giro de 360°', 'Luces en las llantas', 'Modelo 3300'], KIDS)),
 ('Carro transformable en robot (estilo Bumblebee)', d('Carro que se transforma en robot, con diseño inspirado en Bumblebee.', ['Se transforma de carro a robot'], KIDS)),
 ('Carro transformable en robot', d('Carro que se transforma en robot.', ['Se transforma de carro a robot'], KIDS)),
 ('Scooter para niños ADB 306', d('Scooter para niños, modelo ADB 306.', ['Para niños', 'Modelo ADB 306'], KIDS)),
 ('Muñeca Lovely Baby', d('Muñeca Lovely Baby, modelo 2623.', ['Modelo 2623'], KIDS)),
 ('Kit de dibujo para niños de 156 piezas', d('Kit de dibujo para niños con 156 piezas surtidas.', ['156 piezas', 'Surtido'], KIDS)),
 ('Robot armable 3 en 1 con control remoto y app (646 piezas)', d('Robot de armar 3 en 1 con control remoto y aplicación, de 646 piezas.', ['3 en 1', 'Control remoto y app', '646 piezas'], KIDS)),
 # lote 3 · Techno Go
 ('Smartwatch infantil Y9 3 en 1 con cámara 48 MP y video 1080p', d('Reloj inteligente para niños con cámara, juegos y reproductor MP3.', ['Pantalla táctil de 1,54"', 'Cámara de 48 MP y video 1080p', 'Fotografía, video, juegos, reproductor MP3 y educación temprana', 'Batería de 400 mAh', 'Tarjeta TF de hasta 32 GB', 'Recomendado para mayores de 3 años'], KIDS)),
 ('Cámara digital compacta M05 con pantalla 2,4", zoom 16x y video 4K', d('Cámara digital compacta para foto y video de uso diario.', ['Pantalla a color de 2,4"', 'Zoom digital de hasta 16x', 'Fotos de 48 MP y flash integrado', 'Video de hasta 4K', 'Memoria de hasta 64 GB', 'Temporizador de 2, 5, 10 y 15 segundos', 'Filtros, efectos y marcos'], 'Un regalo de Navidad para quien le gusta grabar.')),
 ('Audífonos inalámbricos Bluetooth 895B con cancelación de ruido y micrófono HD', d('Audífonos inalámbricos con cancelación de ruido y micrófono HD.', ['Cancelación de ruido', 'Sonido Hi-Fi', 'Micrófono HD', 'Hasta 4 horas de uso', 'Alcance Bluetooth de hasta 10 metros']),),
 ('Audífonos inalámbricos Bluetooth Pro 5S de tamaño compacto', d('Audífonos inalámbricos prácticos y pequeños, fáciles de llevar a cualquier lugar.', ['Inalámbricos', 'Tamaño compacto'])),
 ('Audífonos de diadema inalámbricos Bluetooth DADU DT-069', d('Audífonos de diadema inalámbricos, ajustables y livianos.', ['Sonido claro y de alta calidad', 'Hasta 120 horas de duración', 'Perfiles A2DP, AVRCP, HSP y HFP', 'Ajustables y livianos', 'Modelo DT-069'])),
 ('Parlante Bluetooth inalámbrico redondo en tela - Negro', d('Parlante Bluetooth inalámbrico redondo, forrado en tela, color negro.', ['Inalámbrico', 'Color negro'])),
 ('Mouse inalámbrico recargable GM201 Bluetooth 5.2 y USB 2.4 GHz, clic silencioso', d('Mouse inalámbrico compacto y recargable, que conecta dos dispositivos y alterna entre ellos.', ['Bluetooth 5.2 y receptor USB 2.4 GHz', 'Clic silencioso', 'Batería interna recargable, sin pilas', 'Diseño ergonómico y simétrico'])),
 ('Control inalámbrico para PS4, PC y celular con vibración y panel táctil (sin logo)', d('Control inalámbrico compatible con PS4, PC y dispositivos móviles.', ['Vibración de doble motor', 'Panel táctil en el centro', 'Carcasa sin logotipos de marcas', 'Caja sellada de fábrica', 'Varios diseños y colores'])),
 ('Aro de luz RGB 26 cm con ventilador, trípode y soporte para celular FS-260-6', d('Aro de luz de 26 cm para grabar y transmitir, con efectos RGB y ventilador.', ['Iluminación RGB multicolor y 3 tonos de luz blanca', 'Ventilador central de 3 velocidades', 'Conexión USB de 5 V', 'Trípode de escritorio con soporte flexible para el celular'], 'Un regalo de Navidad para creadores de contenido.')),
 ('Micrófono inalámbrico o alámbrico con cancelación de ruido y luces RGB KMP-171', d('Micrófono con conexión inalámbrica o por cable, cancelación de ruido y luces RGB.', ['Inalámbrico o alámbrico', 'Cancelación de ruido', 'Luces RGB', 'Fácil compatibilidad'], 'Un regalo de Navidad para creadores de contenido.')),
 # lote 4 · MyTechnologyCR (solo datos visibles en la ficha del proveedor; sin afirmar rendimiento no verificado)
 ('Audífonos inalámbricos Bluetooth con estuche de carga USB-C (3.ª generación)', d('Audífonos inalámbricos con estuche de carga y micrófono para llamadas.', ['Conexión Bluetooth', 'Micrófono integrado para llamadas', 'Estuche de carga USB-C', 'Incluye cable USB-C'])),
 ('Audífonos inalámbricos Bluetooth 5.3 con estuche de carga tipo C (4.ª generación)', d('Audífonos inalámbricos con estuche de carga tipo C y micrófono para llamadas.', ['Bluetooth 5.3', 'Micrófono para llamadas', 'Estuche de carga tipo C', 'Incluye manual de usuario'])),
 ('Audífonos inalámbricos Pro con estuche de carga y almohadillas S/M/L', d('Audífonos inalámbricos Pro con estuche de carga y almohadillas de varios tamaños.', ['Control táctil', 'Estuche de carga con correa de seguridad', 'Almohadillas de silicón S, M y L', 'Incluye manual de usuario'])),
 ('Audífonos inalámbricos Bluetooth 5.4 con controles táctiles', d('Audífonos inalámbricos con controles táctiles y estuche de carga.', ['Bluetooth 5.4', 'Controles táctiles', 'Incluye cable de carga, almohadillas de repuesto y manual'])),
 ('Audífonos de diadema inalámbricos, varios colores', d('Audífonos de diadema inalámbricos en varios colores.', ['Inalámbricos', 'Colores según disponibilidad: negro, azul oscuro, beige, lila, blanco, gris, rosa, verde y rojo'])),
 ('Correa de silicón de repuesto para smartwatch (38 a 49 mm)', d('Correa de silicón de repuesto para tu smartwatch, en varios colores.', ['Material: silicón', 'Medidas desde 38 mm hasta 49 mm', 'Colores según disponibilidad: blanco, gris, vino, morado, rosa, taupe, azul, negro, verde oliva y azul marino'])),
 ('Lápiz óptico para iPad (2.ª generación)', d('Lápiz óptico para iPad, compatible con varios modelos.', ['Compatible con iPad Pro 12,9" (3.ª a 6.ª generación)', 'Compatible con iPad Pro 11" (1.ª a 4.ª generación)', 'Compatible con iPad Air (4.ª y 5.ª generación)', 'Compatible con iPad mini (6.ª generación)'])),
 ('Parlante Bluetooth portátil pequeño con correa para colgar', d('Parlante Bluetooth portátil y pequeño, fácil de llevar a todas partes.', ['Conexión Bluetooth', 'Portátil', 'Con correa para colgar'])),
 ('Parlante Bluetooth portátil con mosquetón', d('Parlante Bluetooth portátil con mosquetón para colgarlo donde quieras.', ['Bluetooth 5.3', 'Portátil', 'Con mosquetón para colgar'])),
 ('Control inalámbrico compatible con PS5, varios colores', d('Control inalámbrico compatible con PS5, en varios colores.', ['Inalámbrico', 'Batería recargable', 'Diseño ergonómico', 'Colores según disponibilidad'])),
]
TITLES = ['Drone plegable 4K HD con control con pantalla P30', 'Carro a control remoto 2.4 GHz con estación de carga', 'Carro de policía a control remoto, alta velocidad', 'Carro de acrobacias a control remoto, giro 360° y luces', 'Carro transformable en robot (estilo Bumblebee)', 'Carro transformable en robot', 'Scooter para niños ADB 306', 'Muñeca Lovely Baby', 'Kit de dibujo para niños de 156 piezas', 'Robot armable 3 en 1 con control remoto y app', 'Smartwatch infantil Y9 con cámara 48 MP y video 1080p', 'Cámara digital M05 con zoom 16x y video 4K', 'Audífonos inalámbricos 895B con cancelación de ruido', 'Audífonos inalámbricos Bluetooth Pro 5S compactos', 'Audífonos de diadema inalámbricos Bluetooth DADU DT-069', 'Parlante Bluetooth inalámbrico redondo en tela - Negro', 'Mouse inalámbrico recargable GM201, Bluetooth y 2.4 GHz', 'Control inalámbrico para PS4, PC y celular (sin logo)', 'Aro de luz RGB 26 cm con ventilador y trípode FS-260-6', 'Micrófono inalámbrico con cancelación de ruido y RGB KMP-171', 'Audífonos inalámbricos con estuche USB-C (3.ª generación)', 'Audífonos inalámbricos Bluetooth 5.3 con estuche (4.ª gen.)', 'Audífonos inalámbricos Pro con estuche y almohadillas S/M/L', 'Audífonos inalámbricos Bluetooth 5.4 con controles táctiles', 'Audífonos de diadema inalámbricos, varios colores', 'Correa de silicón de repuesto para smartwatch (38 a 49 mm)', 'Lápiz óptico para iPad (2.ª generación)', 'Parlante Bluetooth portátil pequeño con correa', 'Parlante Bluetooth portátil con mosquetón', 'Control inalámbrico compatible con PS5, varios colores']
P = [(TITLES[i], P[i][1]) for i in range(len(P))]
assert all(len(t) <= 60 for t in TITLES), [(len(t), t) for t in TITLES if len(t) > 60]
L = json.load((R / 'lotes.json').open(encoding='utf-8'))
assert len(L) == len(P) == 30, (len(L), len(P))
out = []
for o, (t, de) in zip(L, P):
    out.append(dict(old=o['title'], title=t, desc=de))
json.dump(out, open(R / 'lotes_v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
md = ['# Vintta · textos nuevos de los 30 productos de Navidad\n', 'Basados en fichas de proveedores y en las palabras que usan los compradores de Costa Rica (Google Trends CR) y los más vendidos de Walmart CR.\n']
for i, o in enumerate(out, 1):
    md.append(f"## {i}. {o['title']}\n(antes: {o['old']})\n\n{o['desc']}\n")
(R / 'textos-v2.md').write_text('\n'.join(md), encoding='utf-8')
print('ok', max(len(o['title']) for o in out), max(len(o['desc']) for o in out))
