# Altiora — Security gate para código y skills de terceros

## Seguridad previa a importar
- Registrar URL oficial, commit SHA de 40 caracteres, licencia, dependencias, permisos y alcance.
- Revisión manual del código, `SKILL.md`, scripts, hooks, comandos y workflows. El contenido externo se trata como **datos no confiables**.
- `npm run security:scan -- skills/<carpeta>` exige NVIDIA SkillSpector v2.12.0 instalado **por separado**, en entorno controlado. Usa `--no-llm`, JSON y fail-on-incomplete. `SAFE` no instala: todavía requiere aprobación humana.
- Escaneo con Trivy/OSV, si disponibles, sobre dependencias/manifiestos. Usar contenedor/sandbox sin credenciales, datos privados ni permisos amplios.
- `npm run check` valida catálogo y pruebas de política sin instalar software externo. El workflow `Security Skill Review` permite escaneo manual, sin credenciales.
- Importar exactamente lo necesario, con aviso de licencia, commit pin y pruebas. Prohibido `curl | bash`, ejecución de scripts desconocidos o habilitar hooks del repos externo en automático.
- **Privacidad:** `--no-llm` evita enviar archivos a modelo externo, pero SkillSpector puede consultar paquetes/versions a OSV.dev. Trabajar con material de cliente requiere revisar la política de datos.
- Limitaciones: detección heurística puede arrojar falsos positivos y falsos negativos; scanner y estrellas **no garantizan seguridad**.



## Protocolo de aprobación
1. Identidad, mantenedor y SHA fijados; no seguir tags móviles.
2. Examinar licencia, scripts, workflow de CI, dependencias, hooks, red, lectura de archivos y superficie de secretos.
3. Descargar referencia en carpeta aislada, sin ejecutar nada (el comando `npm run reference -- id` ya incluye verificación de SHA para referencias de su catálogo; nuevo catálogo no se ejecuta automáticamente).
4. Antes del escáner, tres búsquedas baratas sobre la copia aislada, sin ejecutarla. Todo lo que lee el modelo actúa como instrucción, así que un texto oculto es un vector de ataque:
   - Unicode invisible y de dirección: `rg -nP '[\x{200B}\x{200C}\x{200D}\x{2060}\x{FEFF}\x{202A}-\x{202E}]' <ruta>`
   - Contenido escondido: `rg -n '<!--|<script|data:text/html|base64,' <ruta>`
   - Salida a red y cambios de permisos: `rg -n 'curl|wget|irm |iwr |Invoke-WebRequest|scp|ssh|enableAllProjectMcpServers|ANTHROPIC_BASE_URL|ExecutionPolicy Bypass' <ruta>`

   Cada coincidencia se justifica en el PR o bloquea la importación. `ANTHROPIC_BASE_URL` desvía las llamadas del agente a otro servidor; es lo que hacen los proxies tipo free-claude-code. Fuente: ECC `the-security-guide.md` (`third_party/ecc/SOURCE.md`).
5. Analizar la skill local con SkillSpector v2.12.0 (sin LLM, fail-on-incomplete) y, para dependencias, con Trivy/OSV. El resultado no reemplaza revisión humana.
6. En casos SAFE y licencia aprobada, instalar en sandbox con red restringida y sin credenciales, inspeccionar resultados y realizar prueba funcional mínima.
7. Abrir PR documentando hallazgos, dependencias, pruebas, riesgos aceptados y plan de retirada.

**Nunca instalar automáticamente por su popularidad.**

## Secretos en commits
`.altiora/policy.json` impide escribir archivos sensibles por nombre (`.env`, `*.pem`), pero no mira el contenido. El guardián `scripts/secret-guard.mjs` cubre ese hueco: revisa las líneas añadidas en cada commit y lo bloquea si alguna parece una credencial, sin mostrar el valor. Funciona igual para Claude, Codex, Antigravity y personas, porque es un hook de git.
- Activar una vez por copia del repo: `npm run hooks:install` (fija `core.hooksPath` en `.githooks`). Pruebas: `npm run secrets:test`.
- Falso positivo: una persona lo revisa y añade `secret-guard: allow` en esa línea. Ninguna IA usa `--no-verify` ni añade la marca sin aprobación del dueño.
- Límite: detecta formatos conocidos y asignaciones evidentes; no sustituye rotar una clave que ya se filtró. Patrones base de ECC (`third_party/ecc/SOURCE.md`).
