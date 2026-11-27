@echo off
setlocal
rem Lanzador PREAMBRA: transmite TODOS los argumentos a lean_run.py (perfil LEAN por defecto).
rem Sin argumentos: --check (sin consumo de IA). Modo interactivo solo si se pide --interactive
rem (el motor exige entonces --accept-interactive-limits). Conserva el codigo de salida.
rem Uso: scripts\preambra.cmd [--check | --help | --dry-run --task-file X --log Y | --interactive --accept-interactive-limits ...]
if "%~1"=="" (
  python "%~dp0lean_run.py" --check
) else (
  python "%~dp0lean_run.py" %*
)
exit /b %ERRORLEVEL%
