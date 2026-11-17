# Migración responsable: Altiora → PREAMBRA
**Decisión de marca:** desde 2026-11-17 el nombre público de la firma es PREAMBRA.  
**Alcance de esta PR:** identidad, textos de marca y visibilidad en la documentación madre, sin renombrados destructivos.

## Identidades separadas
- **PREAMBRA:** marca comercial propuesta para clientes y comunicaciones.
- **Altiora:** nombre histórico del repositorio y de módulos técnicos existentes, rutas, automatizaciones, paquetes, namespaces y referencias. Mantener los identificadores vigentes hasta auditar dependencias.
- **Proyectos de clientes:** La Central del Queso, El Tilichero y demás no deben cambiar de nombre ni perder despliegues, contratos o integraciones.

## Hecho ahora
- Plataforma estratégica de marca, manifiesto, titulares, descripción y tono.
- Sistema visual base: logo horizontal, isotipo y logo monocromático SVG, paleta y tipografía.
- Avisos de precedencia de marca en README y AGENTS.
- Documentos históricos preservados con referencia a la identidad vigente.

## Pendiente de verificación antes de publicación pública
- Búsqueda formal de coincidencias y registrabilidad en Costa Rica y otros mercados (profesional marcario).
- Disponibilidad de dominio, marcas, nombre social y usuarios de redes.
- Conversión a contornos del wordmark con tipografía final y QA visual a escalas reales.
- Nuevos contratos, plantillas comerciales, dirección de correo y landing page aprobados.
- Inventario de referencias Altiora en código, variables, CI, URLs y conectores; migrar con pruebas y redirecciones.
- Actualizar automatizaciones externas y sitios en producción solo cuando el responsable del entorno lo valide.

## Criterio de finalización
La nueva marca estará implementada en código de producción solo cuando nombre, textos, favicon, logo, estilos y recursos hayan pasado accesibilidad, QA, revisión legal/comercial y despliegue controlado. Esta PR no acredita eso.
