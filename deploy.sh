#!/bin/bash
# Script de deploy para Vercel - Tutor Ingesis

echo "🚀 Iniciando deploy de Tutor Ingesis..."
echo "📦 Backend: FastAPI simplificado"
echo "🎨 Frontend: Next.js"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: No se encontró vercel.json"
    exit 1
fi

# Mostrar estructura actual
echo "📁 Estructura del proyecto:"
ls -la api/ 2>/dev/null || echo "⚠️  Directorio api no encontrado"
echo ""

# Deploy con Vercel CLI (si está instalado)
if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI encontrado"
    echo "🔄 Ejecutando: vercel deploy --prod"
    vercel deploy --prod
else
    echo "❌ Vercel CLI no encontrado"
    echo "💡 Por favor usa: npx vercel deploy --prod"
    echo "   o sube los cambios a tu repositorio conectado a Vercel"
fi

echo ""
echo "✅ Script completado"
echo "🌐 URLs de prueba:"
echo "   - Frontend: https://traewk90lkpb.vercel.app"
echo "   - Backend Health: https://traewk90lkpb.vercel.app/api/health"
echo "   - Login Test: https://traewk90lkpb.vercel.app/api/v1/auth/login"
echo ""
echo "🔑 Credenciales de prueba:"
echo "   - Email: diegogalmarini@gmail.com"
echo "   - Contraseña: admin123"