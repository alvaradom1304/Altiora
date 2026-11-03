<#
  Arranque seguro de OmniRoute: solo 127.0.0.1, carpeta de trabajo neutra, sin leer credenciales.

  Uso (manual; este script NO se registra como tarea ni se ejecuta solo):
    pwsh scripts/omniroute-safe-start.ps1 -CheckOnly   # solo verifica exposicion, no arranca nada
    pwsh scripts/omniroute-safe-start.ps1              # arranca si no esta corriendo y verifica

  Garantias:
    - Fija HOSTNAME/HOST=127.0.0.1 (las variables de entorno tienen prioridad sobre .env).
    - Usa un directorio de trabajo vacio, para que no se cargue ningun .env de proyecto.
    - No lee, imprime ni modifica credenciales ni ~/.omniroute.
    - Aborta si detecta una escucha de OmniRoute en una direccion distinta de loopback.
    - No usa 'omniroute stop' (comprobado como no fiable: informa parada y deja el proceso vivo).
#>
[CmdletBinding()]
param(
  [int]$Port = 20128,
  [switch]$CheckOnly
)
$ErrorActionPreference = 'Stop'

function Get-Listeners([int]$p) {
  Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalAddress -ne '' } |
    Select-Object LocalAddress, LocalPort, OwningProcess -Unique
}

function Assert-LoopbackOnly([int]$p) {
  $bad = Get-Listeners $p | Where-Object { $_.LocalAddress -notin @('127.0.0.1', '::1') }
  if ($bad) {
    $bad | Format-Table | Out-String | Write-Host
    throw "BLOQUEO: el puerto $p escucha fuera de loopback. No se arranca nada; identificar el proceso antes de intervenir."
  }
}

# 1. Estado actual
$existing = Get-Listeners $Port
if ($existing) {
  Assert-LoopbackOnly $Port
  Write-Host "OmniRoute ya escucha solo en loopback (PID $(($existing | Select-Object -First 1).OwningProcess))."
} elseif ($CheckOnly) {
  Write-Host "NO_RUNNING: nada escucha en el puerto $Port (modo -CheckOnly: no se arranca)."
  exit 3
} else {
  # 2. Requisitos
  $omni = Get-Command omniroute -ErrorAction SilentlyContinue
  if (-not $omni) { throw 'BLOQUEO: omniroute no esta en PATH (no se reinstala automaticamente).' }
  $neutral = Join-Path $env:USERPROFILE '.altiora\omniroute-cwd'
  New-Item -ItemType Directory -Force -Path $neutral | Out-Null
  if (Get-ChildItem -Force -Path $neutral -Filter '.env*' -ErrorAction SilentlyContinue) {
    throw "BLOQUEO: hay archivos .env en $neutral; el directorio de trabajo debe estar vacio de .env."
  }
  # 3. Arranque ligado a loopback
  $env:HOSTNAME = '127.0.0.1'
  $env:HOST = '127.0.0.1'
  $env:PORT = "$Port"
  Push-Location $neutral
  try { & omniroute serve --daemon --no-open | Out-Null } finally { Pop-Location }
  $deadline = (Get-Date).AddSeconds(60)
  while ((Get-Date) -lt $deadline -and -not (Get-Listeners $Port)) { Start-Sleep -Seconds 2 }
  if (-not (Get-Listeners $Port)) { throw "FAIL: no aparece ninguna escucha en $Port tras 60 s." }
  Assert-LoopbackOnly $Port
}

# 4. Verificacion (solo sondas sin credenciales)
function Probe([string]$url) {
  try { (Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 5 -MaximumRedirection 0).StatusCode }
  catch { if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 'SIN_RESPUESTA' } }
}
$base = "http://127.0.0.1:$Port"
$result = [ordered]@{
  health_local          = Probe "$base/api/health"            # esperado 200
  admin_providers       = Probe "$base/api/providers"         # esperado 401
  admin_keys            = Probe "$base/api/keys"              # esperado 401
  admin_settings        = Probe "$base/api/settings"          # esperado 401
  v1_models_sin_clave   = Probe "$base/v1/models"             # esperado 401
}
$lan = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
  Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' } | Select-Object -First 1 -ExpandProperty IPAddress
if ($lan) { $result['lan_' + $lan] = Probe "http://${lan}:$Port/api/health" } # esperado SIN_RESPUESTA
$result.GetEnumerator() | ForEach-Object { Write-Host ('{0,-28} {1}' -f $_.Key, $_.Value) }

$ok = ($result.health_local -eq 200) -and
      (@($result.admin_providers, $result.admin_keys, $result.admin_settings, $result.v1_models_sin_clave) | Where-Object { $_ -notin 401, 403 }).Count -eq 0 -and
      (-not $lan -or $result['lan_' + $lan] -eq 'SIN_RESPUESTA')
if ($ok) { Write-Host 'PASS: solo loopback y rutas administrativas protegidas.'; exit 0 }
Write-Host 'FAIL: revisar los valores anteriores.'; exit 1
