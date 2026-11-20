# Correo comercial no solicitado en Costa Rica: qué dice la norma

Fecha: 2026-11-12 · Rol: `claude` (investigación) · Estado: **revisión documental, no es asesoría legal**. Pendiente de revisión cruzada (`qa-reviewer` u otra IA) y de confirmación por un abogado.
Motivo: decidir si la skill `higgsfield-client-finder` (y en general `cold-email`) puede enviar correos de prospección a empresas de Costa Rica. Completa el pendiente «revisión legal del correo en frío» de [ventas-skills-2026-11-01.md](../security/reviews/ventas-skills-2026-11-01.md), que solo citaba la Ley 8968.

## Conclusión

**No enviar correos de venta en frío a empresas de Costa Rica.** La norma vigente exige consentimiento previo para correo «con fines de venta directa» y no prevé una excepción para destinatarios que sean empresas. La Ley 10946 (pendiente de entrar en vigor) refuerza la misma regla. La propia skill `higgsfield-client-finder` indica descartar los países donde no esté claramente permitido; Costa Rica queda fuera.

## VERIFICADO (texto leído de la norma)

| Norma | Qué dice | Fuente |
|---|---|---|
| Decreto 35205-MINAET, art. 31 (desarrolla el art. 44 de la Ley 8642) | Prohíbe usar correo electrónico, fax, llamada automática u otro dispositivo «con fines de venta directa», salvo: (a) consentimiento previo del cliente, o (b) cliente previo a quien se le ofrecen productos similares, avisándole al recoger sus datos | [PDF SUTEL](https://sutel.go.cr/sites/default/files/normativas/reglamento_sobre_medidas_de_proteccion_de_la_privacidad_de_las_comunicaciones_decreto_ejecutivo_35205-minaet.pdf) |
| Decreto 35205, art. 32 | Remitente identificable con claridad y dirección válida para pedir la baja sin costo | Ídem |
| Decreto 35205, art. 5 c | «Correo electrónico comercial»: el que promociona bienes o servicios de una empresa, organización o persona con fines lucrativos | Ídem |
| Ley 10946, art. 29 | El comerciante debe abstenerse de enviar comunicaciones comerciales «por cualquier medio» no solicitadas ni consentidas, salvo relación contractual o precontractual; la baja se respeta de inmediato | [Texto, Bufete de Costa Rica](https://bufetedecostarica.com/wp-content/uploads/2026/07/gobernanza-de-los-servicios-digitales-y-el-comercio-electronico_10946.pdf) |
| Ley 10946, art. 9 | Prohíbe ocultar la identidad del remitente | Ídem |
| Ley 10946, art. 4 h | «Consumidor» incluye a la «entidad de hecho o de derecho», remitiendo a la Ley 7472 | Ídem |
| Ley 10946, transitorio único | Entra en vigor 12 meses después de su publicación | Ídem |

En ninguno de los dos textos se encontró una excepción para destinatarios que sean personas jurídicas.

## NO SÉ / SUPUESTO

- **Alcance del decreto hoy:** está redactado sobre abonados y operadores de telecomunicaciones y lo vigila la SUTEL. Si alcanza a una agencia que escribe a una pyme es interpretación legal: **NO SÉ**.
- **Fecha de la Ley 10946:** publicación en La Gaceta el 24-jun-2026 según [Ecija](https://files.griddo.ecija.com/ecija-informe-ley-de-gobernanza-de-servicios-digitales-y-comercio-electronico.pdf); no confirmado en La Gaceta. Si es correcta, rige desde ~junio de 2027 (SUPUESTO).
- **Empresa como consumidor:** la Ley 7472 define consumidor como destinatario final; no se leyó en esta revisión (SUPUESTO).
- Ley 8968 (datos personales): aplica además a correos de personas identificables; no se revisó aquí.

## Qué se permite hacer (OPINIÓN)

- **Aporta valor:** usar la parte de investigación de la skill (empresas con un problema visible y una muestra gratis) para conseguir presentaciones de conocidos, visitas en persona o responder a empresas que ya piden proveedores. Eso es contacto solicitado o con relación precontractual.
- **Entorpece:** enviar correos fríos desde Gmail a empresas de Costa Rica.
- Fuera de Costa Rica, seguir la tabla de países de la skill (por ejemplo, CAN-SPAM en EE. UU.), con portafolio previo.

## Fuentes secundarias

- [Tico Times, 2013: SUTEL aplica el art. 44 a llamadas de venta](https://ticotimes.net/2013/01/28/phone-customers-can-now-block-annoying-sales-calls)
- [La Nación: publicidad no deseada y operadores](https://www.nacion.com/el-pais/servicios/se-prohibe-a-telefonicas-compartir-datos-de/XGSJDCQLWNH2PHVQROHRTSSS7Y/story/)
