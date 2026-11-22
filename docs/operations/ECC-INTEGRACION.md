# ECC en Altiora / PREAMBRA

## Alcance
La integración es selectiva; el plugin nativo ECC no se instala. [Matriz de adopción](../../references/ecc-adoption.json) con el inventario de metadatos de upstream, seis prácticas centrales comparadas, archivos locales y exclusiones. Las especialidades de lenguajes no usadas quedan para evaluación bajo demanda. [Procedencia y MIT](../../third_party/ecc/SOURCE.md).

## Qué se agrega
- Diagnóstico ejecutable que distingue archivos presentes, hook configurado y prueba funcional pendiente.
- Instalación del guardián solo en el worktree elegido. Rechaza sustituir un hooksPath o wrapper personalizado y no redirige los otros checkouts. Comprueba archivo regular y ejecutabilidad POSIX.
- Verificación de seis fases y ficha de capacidad/regresión dentro de la skill de revisión existente.
- Lecciones atómicas por proyecto dentro del Learning OS, sin observador ni captura de conversaciones.

## Uso desde la raíz Git
- npm run ecc:doctor: solo lectura; código 1 indica integración incompleta y 2 error de configuración.
- npm run hooks:install: activación explícita local; valida archivos y conserva hooks personalizados. Habilita extensions.worktreeConfig en el repositorio común y escribe core.hooksPath solo para el worktree actual. Rechaza repositorios comunes bare y core.worktree personalizado antes de escribir configuración.
- npm run ecc:test: fixtures aislados, incluye un commit con secreto ficticio bloqueado y otro limpio aceptado.
- npm run check: control completo compartido; contiene las nuevas pruebas.

El diagnóstico no revisa instalaciones personales de Claude ni afirma plugin nativo, consumo, escucha, conexiones o cobertura total. Configurado no significa probado; la prueba funcional se conserva por separado. No escanea transcripciones, archivos de clientes ni entornos.

## Canonical y otros worktrees
La presencia en una rama no instala nada en la copia canónica. Instalar solo después de llevar los archivos revisados al checkout elegido y preservar sus cambios locales. Un hooksPath heredado con archivo inexistente se informa como missing. Repetir el doctor en cada checkout: sus estados no se transfieren automáticamente.

## Retirada
Desactivar el core.hooksPath del worktree con Git solo si sigue apuntando al guardián de esta integración; conservar cualquier hook personalizado. Las fuentes del PR y los cambios locales deben revisarse antes de retirarlos. No borrar el repositorio ni datos de clientes.
