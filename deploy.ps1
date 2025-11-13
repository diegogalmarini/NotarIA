# Script de deploy para Vercel - Tutor Ingesis (Windows)
Write-Host "🚀 Iniciando deploy de Tutor Ingesis..." -ForegroundColor Green
Write-Host "📦 Backend: FastAPI simplificado" -ForegroundColor Blue
Write-Host "🎨 Frontend: Next.js" -ForegroundColor Blue
Write-Host ""

# Verificar que estamos en el directorio correcto
if (!(Test-Path "vercel.json")) {
    Write-Host "❌ Error: No se encontró vercel.json" -ForegroundColor Red
    exit 1
}

# Mostrar estructura actual
Write-Host "📁 Estructura del proyecto:" -ForegroundColor Yellow
Get-ChildItem api/ -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "   $($_.Name)" }
if (!(Test-Path "api/")) {
    Write-Host "⚠️  Directorio api no encontrado" -ForegroundColor Yellow
}
Write-Host ""

# Verificar si Vercel CLI está instalado
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if ($vercelInstalled) {
    Write-Host "✅ Vercel CLI encontrado" -ForegroundColor Green
    Write-Host "🔄 Ejecutando: vercel deploy --prod" -ForegroundColor Yellow
    vercel deploy --prod
} else {
    Write-Host "❌ Vercel CLI no encontrado" -ForegroundColor Red
    Write-Host "💡 Por favor usa: npx vercel deploy --prod" -ForegroundColor Yellow
    Write-Host "   o sube los cambios a tu repositorio conectado a Vercel" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Script completado" -ForegroundColor Green
Write-Host "🌐 URLs de prueba:" -ForegroundColor Cyan
Write-Host "   - Frontend: https://traewk90lkpb.vercel.app" -ForegroundColor White
Write-Host "   - Backend Health: https://traewk90lkpb.vercel.app/api/health" -ForegroundColor White
Write-Host "   - Login Test: https://traewk90lkpb.vercel.app/api/v1/auth/login" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Credenciales de prueba:" -ForegroundColor Cyan
Write-Host "   - Email: diegogalmarini@gmail.com" -ForegroundColor White
Write-Host "   - Contraseña: admin123" -ForegroundColor White