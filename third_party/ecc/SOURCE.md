# ECC (Everything Claude Code) · procedencia

- **Repositorio oficial:** https://github.com/affaan-m/ECC (antes `everything-claude-code`). Las copias de otros usuarios con el mismo nombre no son oficiales; no usarlas.
- **Commit fijado:** `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b` (rama `main`, consultado el 2026-11-09).
- **Licencia:** MIT. Copia en `LICENSE.txt`.
- **Revisado por:** Claude (sesión del 2026-11-09). Solo lectura por la API de GitHub; no se instaló el plugin ni se ejecutó ningún script de ECC.

## Qué se tomó y dónde está

| Pieza de ECC | Uso en Altiora | Archivo |
|---|---|---|
| `scripts/hooks/governance-capture.js`: lista `SECRET_PATTERNS` (AWS, secreto asignado, clave privada, JWT, token de GitHub) | Patrones base del guardián de commits; reescrito sin dependencias, bloquea en vez de solo registrar | `scripts/secret-guard.mjs`, `.githooks/pre-commit` |
| `the-security-guide.md`: escaneos de Unicode oculto, comentarios HTML y comandos de red | Paso de revisión en la puerta de seguridad | `docs/security/third-party-skill-gate.md` |
| `the-longform-guide.md`: CLI en vez de MCP, archivo de sesión, compactar en puntos lógicos | Hábitos de ahorro | `docs/operations/CONECTORES-Y-AHORRO.md` |

## Qué NO se tomó y por qué

- El plugin completo (71 agentes, 314 skills, 98 comandos, hooks): duplicaría capacidades de Altiora y aumentaría el contexto fijo de cada turno.
- Sus hooks tal cual: dependen de varios módulos internos (`gateguard-fact-force`, `run-with-flags`, `plugin-hook-bootstrap`) y se ejecutan en cada llamada de herramienta.
- `suggest-compact.js`: la técnica se recoge como hábito; el script añade estado y lógica que no hacen falta para aplicarla.

## Retirada

Borrar `scripts/secret-guard.mjs`, su prueba, `.githooks/` y esta carpeta; quitar `secrets:test`, `hooks:install` y la prueba de `toolkit:test` en `package.json`, y ejecutar `git config --unset core.hooksPath`.
