# Prompt · imágenes de productos El Tilichero CR

Para Codex (preferido, si tiene créditos) o Antigravity (excepción: solo si Claude y Codex no pueden y su modelo de imagen está disponible). Pegar tal cual con el repo Altiora abierto en la rama `claude/tilicheros-traspaso`.

```
Continúas un trabajo de Altiora para El Tilichero CR. Responde en español.

ANTES DE EMPEZAR
1. Lee projects/tilicheros/traspaso/LEEME-TRASPASO.md y projects/tilicheros/traspaso/PROMPT-ANTIGRAVITY.md (reglas del dueño y errores conocidos). Esas reglas mandan.
2. Confirma qué capacidad REAL de imagen tienes (generar, editar, quitar elementos). Si no puedes generar o editar imágenes, dilo y detente.

ENCARGO
A) Cuatro imágenes por producto, para atraer clientes, de los 40 productos publicados en Vintta (lotes en projects/tilicheros/vintta/). Orden: primero los 10 mejores del ranking projects/tilicheros/proveedores/estudio-mercado-costa-rica-virales-ranking.csv; entrega ese lote y espera mi visto bueno antes de seguir con los demás.
   Cuatro encuadres sugeridos: (1) principal sobre fondo limpio, (2) en uso, (3) detalle, (4) tamaño o contenido de la caja. Formato cuadrado 1080x1080, sin texto ni logos.
B) Las fotos publicadas hoy muestran la marca/logo del proveedor y nos perjudica. Propón la vía más segura:
   - preferida: imágenes nuevas generadas a partir del producto, sin la marca del proveedor;
   - alternativa: pedir al proveedor fotos sin marca (redáctame el mensaje; no lo envíes);
   - NO borrar logos de fotos del proveedor sin que yo confirme que tenemos derecho a usarlas.

LÍMITES
- Una imagen generada no puede mostrar características, accesorios, marcas ni acabados que el producto real no tenga. Si no puedes comprobarlo con la ficha del proveedor, márcalo SUPUESTO y dímelo.
- No llamar «original» a nada sin factura del fabricante. No incluir marcas de terceros en las imágenes.
- No subir, publicar ni editar nada en Vintta; solo guardar los archivos en projects/tilicheros/imagenes/<producto>/ y un índice CSV (producto, archivo, método usado, fuente de referencia).
- No contactar proveedores ni clientes, no gastar, no crear cuentas, no push ni PR sin que yo lo ordene.
- Descargar archivos requiere mi permiso previo (nombre, origen, tamaño).
- Nota para cuando lleguemos a subir: el traspaso dice que Vintta admite una sola foto por la vía usada. Comprueba si el panel admite varias y dímelo; no lo des por hecho.

ENTREGA
Qué hiciste, cuántas imágenes, cómo las comprobaste (captura o comando) y qué queda sin verificar. Marca VERIFICADO / SUPUESTO / NO SÉ.
```
