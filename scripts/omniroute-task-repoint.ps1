<#
  Repunta la tarea Altiora-OmniRoute-SafeStart al checkout canonico (no a un worktree).
  Por defecto es SIMULACRO: solo informa. Con -Apply modifica UNICAMENTE la accion de la tarea,
  y solo si el script destino existe, es identico al de origen y la tarea tiene respaldo XML.
  No requiere administrador, no toca firewall, datos ni credenciales.
    powershell -File scripts/omniroute-task-repoint.ps1            # simulacro
    powershell -File scripts/omniroute-task-repoint.ps1 -Apply     # aplicar (tras fusionar el PR y actualizar el checkout canonico)
  Revertir: Register-ScheduledTask -Xml (Get-Content <respaldo>.xml -Raw) -TaskName Altiora-OmniRoute-SafeStart -Force
#>
[CmdletBinding()]
param(
  [string]$Target = 'C:\Users\Usuario\orca\workspaces\Altiora-Immersive-Web-Lab\altiora-unificado\scripts\omniroute-safe-start.ps1',
  [string]$TaskName = 'Altiora-OmniRoute-SafeStart',
  [string]$BackupDir = (Join-Path $env:USERPROFILE '.altiora-backups'),
  [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$task = Get-ScheduledTask -TaskName $TaskName
$current = $task.Actions[0].Arguments
Write-Host "Accion actual : $current"
if (-not (Test-Path -LiteralPath $Target)) { Write-Host "BLOQUEO: el destino no existe aun ($Target). Fusionar el PR y actualizar el checkout canonico primero."; exit 2 }
$src = Join-Path (Split-Path $PSScriptRoot -Parent) 'scripts\omniroute-safe-start.ps1'
if ((Get-FileHash $Target).Hash -ne (Get-FileHash $src).Hash) { Write-Host 'BLOQUEO: el destino difiere del script revisado; no se repunta.'; exit 3 }
$bk = Get-ChildItem $BackupDir -Filter "task-$TaskName-*.xml" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $bk) { Write-Host 'BLOQUEO: no hay respaldo XML de la tarea.'; exit 4 }
$newArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Target`""
Write-Host "Accion nueva  : $newArgs`nRespaldo      : $($bk.FullName)"
if (-not $Apply) { Write-Host 'SIMULACRO: nada modificado. Usar -Apply para aplicar.'; exit 0 }
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $newArgs
Set-ScheduledTask -TaskName $TaskName -Action $action | Out-Null
Start-ScheduledTask -TaskName $TaskName; Start-Sleep -Seconds 20
$r = (Get-ScheduledTaskInfo -TaskName $TaskName).LastTaskResult
Write-Host "Verificacion: LastTaskResult=$r (0 = correcto)"; exit ([int]($r -ne 0))
