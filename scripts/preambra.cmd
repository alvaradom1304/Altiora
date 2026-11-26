@echo off
rem Lanzador PREAMBRA: sesion interactiva de Claude CLI con perfil LEAN (o --profile ...) y proyecto detectado por el remote.
rem Uso: scripts\preambra.cmd [--profile standard] [--effort low]  -  revisar antes con: scripts\preambra.cmd --check
if /I "%~1"=="--check" (
  python "%~dp0lean_run.py" --check %2 %3 %4 %5 %6
) else (
  python "%~dp0lean_run.py" --interactive %*
)
