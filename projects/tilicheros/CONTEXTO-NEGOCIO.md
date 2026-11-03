# El Tilichero · contexto del negocio completo (corrige el sesgo de campaña)

Fecha: 2026-11-03 · Norma: [CONTEXT-FIRST-BSCG.md](../../docs/altiora-business/entrega/CONTEXT-FIRST-BSCG.md) · Datos: [COBERTURA-NEGOCIO.json](COBERTURA-NEGOCIO.json) (verificador: `python docs/altiora-business/entrega/scripts/bscg.py projects/tilicheros/COBERTURA-NEGOCIO.json`). No se modificó ninguna campaña ni documento histórico; este archivo los reinterpreta.

**Resultado del BSCG hoy: HOLD** para decidir qué categoría o producto impulsar. Sí pueden avanzar la preparación del Discovery, el protocolo de autenticidad y las plantillas; no puede avanzar la priorización definitiva ni la producción.

## 1. Causa raíz del sesgo
El Tilichero es, según el fundador, un negocio de varias categorías. La documentación operativa se concentró en audífonos y campañas audiovisuales, y se leyó el alcance de una campaña como el alcance de la empresa.

| # | Causa | Evidencia |
|---|---|---|
| 1 | Un alcance acotado a un piloto se usó como descripción de la empresa | `DIRECCION_DEL_PROYECTO.md` dice «gaming y tecnología como foco **de este piloto**»; `FICHA-ENCAJE-G1.md` lo copió como el sector de la empresa |
| 2 | La plantilla de entrada no pedía el portafolio | `01-ficha-encaje.md` tenía un único campo «sector»; ninguno de categorías ni de datos por categoría |
| 3 | El primer producto se eligió por conveniencia de producción y se leyó como prioridad | DEC-01: «dos variantes aprovechan un solo rodaje»; no hay ventas ni margen detrás |
| 4 | Lo que se sabía de bebés y anime no entró al Discovery | Solo existen como variantes conceptuales de un laboratorio de motion («conceptos originales, no fichas de productos reales»); ningún documento del proyecto las menciona |
| 5 | Ningún control exigía revisar categorías o datos comerciales antes de priorizar | G1 mide comprador y problema, no cobertura del negocio |
| 6 | Parte del Discovery posterior partía de supuestos | La entrevista del #61 pregunta por «tus 3 productos que más se venden» sin antes confirmar qué categorías existen (corregido en la entrevista maestra) |

Qué no se sabe: no hay una sola cifra de ventas, margen, inventario o caja de ninguna categoría. «Los audífonos lideran» nunca fue un dato.

## 2. Inventario de categorías
«Declarada» no es «comercialmente verificada».

| Categoría | Declarada por | Qué hay en el repo | Revisada | Ventas · margen · inventario |
|---|---|---|---|---|
| Gaming | Fundador (2026-11-03) y foco del piloto | Fotos de vitrina: controles compatibles con PlayStation, aro RGB; consola retro (RETRO1) y RGB1 como extensiones | Parcial | UNKNOWN |
| Tecnología | Fundador y foco del piloto | Empaques de audífonos y periféricos en fotos; SKU de audífonos elegido sin ficha | Parcial | UNKNOWN |
| Bebés | Fundador | Solo una variante conceptual «BEBÉS · REGALOS» | No | UNKNOWN |
| Anime | Fundador | Solo una variante conceptual «ANIME · COLECCIONABLES» | No | UNKNOWN |
| Otras | Las fotos de vitrina muestran «otros dispositivos de distintas categorías» (INFERRED) | Sin lista | No | UNKNOWN |

## 3. Matriz de conocimiento (resumen; el detalle con fuente, fecha, confianza, impacto y método está en el JSON)
| Afirmación | Estado | Nota |
|---|---|---|
| Vende en gaming, tecnología, bebés y anime | REPORTED | Fundador; se confirma con el catálogo del dueño |
| Gaming y tecnología son el foco del piloto | REPORTED | 2026-10-29; ¿foco de la empresa o solo de la campaña? |
| Los audífonos son la categoría que más vende o rinde | UNKNOWN | No existen cifras; no se usa en ninguna decisión |
| El primer lote de audífonos es una prioridad | INFERRED | Es un experimento (DEC-01), no una prioridad |
| Bebés y anime tienen ventas | UNKNOWN | Solo conceptos |
| Los «AirPods» son originales | UNKNOWN | Bloqueado; ver [protocolo](PROTOCOLO-AUTENTICIDAD-AIRPODS.md) |
| Presupuesto de anuncios sin aprobar | OUTDATED | Del 2026-10-29 |
| Márgenes, inventario y caja | UNKNOWN | Hoja de captura |

## 4. Campañas anteriores
GAME1+GAME2 (audífonos), RETRO1 y RGB1 quedan como **experimentos** con su valor propio: producción, aprendizaje y material. No son prioridades automáticas. Si los datos del dueño muestran otra categoría con mejor rentabilidad, se prioriza esa.

## 5. Preguntas para el dueño, por prioridad
Cada una cambia una decisión. Se hacen en la sesión de 30 min de la [entrevista maestra](ENTREVISTA-MAESTRA-TILICHERO-G1.md); lo marcado «sesión 2» se pospone si el tiempo se acorta.
1. ¿Quién decide y aprueba el gasto? *(sin decisor no hay propuesta)*
2. ¿Qué categorías vende hoy? Dejar que las nombre él y después contrastar con esta lista. *(confirma el alcance real)*
3. ¿Cuáles dejaron más dinero el último mes? Unidades, precio y costo de las tres principales. *(permite priorizar por rentabilidad)*
4. ¿Bebés y anime son líneas activas? Unidades y margen del último mes. *(hoy solo existen como concepto)*
5. Capacidad de inversión y caja libre al mes tras reponer inventario. *(define qué es sostenible)*
6. ¿Qué tendría que pasar en 30 días para que valga la pena? *(criterio de éxito)*
7. Factura del proveedor y fotos de los audífonos. *(desbloquea cualquier pieza con marca)*
8. Inventario parado y rotación por categoría. *(sesión 2 si falta tiempo)*
9. Qué otras categorías existen. *(sesión 2 si falta tiempo)*

## 6. Qué puede avanzar y qué espera
| Puede avanzar | Debe esperar confirmación | Debe detenerse |
|---|---|---|
| Entrevista, hoja de captura, plantilla de diagnóstico, protocolo de autenticidad | Elegir categoría a impulsar, presupuesto, propuesta de alcance | Publicar piezas que afirmen autenticidad no demostrada; gasto en pauta |

Al responder el dueño: actualizar `COBERTURA-NEGOCIO.json` (nunca pasar un `REPORTED` a `VERIFIED` sin documento), volver a ejecutar el verificador y recién entonces redactar el diagnóstico.
