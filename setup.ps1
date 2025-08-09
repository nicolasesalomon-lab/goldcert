Param([switch]$Rebuild)

$ErrorActionPreference = "Stop"
Write-Host "`n=== GoldCert v1 :: setup.ps1 ===`n" -ForegroundColor Cyan

# Directorio del docker-compose (esta misma carpeta)
$ComposeDir = $PSScriptRoot

# 1) Forzar env.py correcto (sin fileConfig)
$EnvPyPath = Join-Path $PSScriptRoot "backend\app\migrations\env.py"
New-Item -ItemType Directory -Force -Path (Split-Path $EnvPyPath) | Out-Null

@'
from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
import os
from app.extensions import db
from app.models import *  # noqa
target_metadata = db.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL no está definido")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL no está definido")
    connectable = engine_from_config({"sqlalchemy.url": url}, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'@ | Set-Content -Encoding UTF8 $EnvPyPath
Write-Host "env.py actualizado" -ForegroundColor Green

# Helpers docker compose SIEMPRE con --project-directory y sin errores falsos
function Compose {
  param([Parameter(Mandatory)] [string[]]$Args,
        [switch]$Silent)

  $cmd = @('compose','--project-directory', $ComposeDir) + $Args
  $old = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'  # evitar NativeCommandError por stderr "informativo"
  try {
    $all = & docker @cmd 2>&1
    $code = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $old
  }
  if (-not $Silent -and $all) { $all | ForEach-Object { Write-Host $_ } }
  if ($code -ne 0) { throw "docker compose $($Args -join ' ') fallo con codigo $code" }
}

function ComposeOut {
  param([Parameter(Mandatory)] [string[]]$Args)

  $cmd = @('compose','--project-directory', $ComposeDir) + $Args
  $old = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $all = & docker @cmd 2>&1
    $code = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $old
  }
  if ($code -ne 0) { throw "docker compose $($Args -join ' ') fallo con codigo $code" }
  return ($all | Out-String)
}

# 2) Down / Build / Up
Write-Host "Bajando contenedores y volumenes..."
Compose @('down','-v') -Silent

if ($Rebuild) {
  Write-Host "Construyendo backend rebuild forzado..."
  Compose @('build','--no-cache','backend')
} else {
  Write-Host "Construyendo backend..."
  Compose @('build','backend')
}

Write-Host "Levantando servicios db y backend..."
Compose @('up','-d')

# 3) Esperar DB healthy
Write-Host "Esperando base de datos healthy..."
$cid = (ComposeOut @('ps','-q','db') | Out-String).Trim()
$tries = 0
while ([string]::IsNullOrWhiteSpace($cid) -and $tries -lt 10) {
  Start-Sleep -Seconds 2
  $cid = (ComposeOut @('ps','-q','db') | Out-String).Trim()
  $tries++
}
if (-not $cid) { throw "No se obtuvo el container ID de la DB" }

$tries = 0
while ($tries -lt 60) {
  $health = (& docker 'inspect' '-f' '{{.State.Health.Status}}' $cid 2>$null | Out-String).Trim()
  if ($health -eq 'healthy') { break }
  Start-Sleep -Seconds 2
  $tries++
}
if ($tries -ge 60) { throw "DB not healthy (timeout)" }
Write-Host "DB healthy" -ForegroundColor Green

# 4) DATABASE_URL informativo
try {
  $envOk = (ComposeOut @('exec','-T','backend','sh','-lc','env | grep DATABASE_URL || true') | Out-String).Trim()
  if (-not $envOk -or ($envOk -notmatch 'postgresql\+psycopg://')) {
    Write-Warning "DATABASE_URL no visible dentro del backend. Revisar backend\.env"
  }
} catch { Write-Warning "No se pudo verificar DATABASE_URL (continúo)" }

# 5) Migraciones
Write-Host "Aplicando migraciones..."
Compose @('exec','-T','backend','flask','db','upgrade')
Write-Host "Migraciones OK" -ForegroundColor Green

# 6) Seed
Write-Host "Cargando seed..."
Compose @('exec','-T','backend','python','seed.py')
Write-Host "Seed OK (admin@test.com / admin + SE EE ENACOM INAL)" -ForegroundColor Green

# 7) Ready
Write-Host "`nTodo listo ✅"
Write-Host "API:    http://localhost:5000/swagger-ui"
Write-Host "Health: http://localhost:5000/api/health"
