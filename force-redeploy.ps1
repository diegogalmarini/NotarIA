# Script para forzar redeploy en Vercel
# Este script actualiza un archivo para forzar un nuevo despliegue

Write-Host "🔄 Forzando redeploy de Tutor Ingesis..." -ForegroundColor Green

# Obtener la fecha y hora actual
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Crear un archivo de marca de tiempo para forzar el redeploy
$deployFile = "force-redeploy.txt"
$timestamp | Out-File -FilePath $deployFile -Encoding UTF8

Write-Host "✅ Archivo de fuerza de redeploy creado: $deployFile" -ForegroundColor Green
Write-Host "📄 Contenido: $timestamp" -ForegroundColor Yellow

# También actualizar el frontend para forzar redeploy
$apiConfigFile = "notaria-frontend\src\config\api.ts"
if (Test-Path $apiConfigFile) {
    $content = Get-Content $apiConfigFile -Raw
    if ($content -match "Force redeploy") {
        # Actualizar la línea de fuerza de redeploy
        $content = $content -replace "Force redeploy - Vercel deployment fix.*", "Force redeploy - Vercel deployment fix $timestamp"
    } else {
        # Agregar la línea de fuerza de redeploy
        $content = $content + "`n// Force redeploy - Vercel deployment fix $timestamp"
    }
    Set-Content -Path $apiConfigFile -Value $content -Encoding UTF8
    Write-Host "✅ Frontend actualizado para forzar redeploy" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Pasos siguientes:" -ForegroundColor Cyan
Write-Host "1. Sube estos cambios a Git:" -ForegroundColor Yellow
Write-Host "   git add ." -ForegroundColor White
Write-Host "   git commit -m 'Force redeploy'" -ForegroundColor White
Write-Host "   git push" -ForegroundColor White
Write-Host ""
Write-Host "2. Vercel detectará el cambio y hará automáticamente el redeploy" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Alternativamente, ve a:" -ForegroundColor Yellow
Write-Host "   https://vercel.com/dashboard" -ForegroundColor Blue
Write-Host "   y haz click en 'Redeploy' manualmente" -ForegroundColor Blue