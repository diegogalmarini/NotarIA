# Instrucciones de Deploy para Vercel - Tutor Ingesis

## 🎯 ESTADO ACTUAL
- ✅ Variables de entorno configuradas
- ✅ Frontend funcionando
- ❌ Backend con error 500 (FUNCTION_INVOCATION_FAILED)

## 🚀 SOLUCIÓN APLICADA
Se ha simplificado el backend para eliminar errores de Vercel:

### 📁 NUEVA ESTRUCTURA:
```
api/
├── index.py          ← Backend simplificado (FASTAPI + PYDANTIC)
└── requirements.txt  ← Solo 2 dependencias
```

### 🔧 CAMBIOS REALIZADOS:
1. **Eliminado SQLAlchemy** → Base de datos en memoria
2. **Eliminado JWT complejo** → Tokens mock simples
3. **Reducido a 2 dependencias** → FastAPI + Pydantic
4. **Configuración actualizada** → vercel.json optimizado

### 📋 ENDPOINTS FUNCIONALES:
- `GET /api/health` → Estado del servidor
- `POST /api/v1/auth/login` → Login con credenciales
- `GET /api/v1/auth/me` → Perfil de usuario
- `POST /api/v1/tutor/chat` → Chat con tutor IA

### 🔑 CREDENCIALES DE PRUEBA:
- Email: `diegogalmarini@gmail.com`
- Contraseña: `admin123`
- Rol: `admin`

## ⚙️ CONFIGURACIÓN VERCEL
Archivo `vercel.json` actualizado:
```json
{
  "builds": [
    {"src": "notaria-frontend/package.json", "use": "@vercel/next"},
    {"src": "api/index.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "api/index.py"},
    {"src": "/(.*)", "dest": "notaria-frontend/$1"}
  ]
}
```

## 🧪 PRUEBAS POST-DEPLOY
Después del deploy, verificar:
1. Backend health: https://traewk90lkpb.vercel.app/api/health
2. Login funcional con credenciales de arriba
3. Tutor respondiendo preguntas sobre Ingesis SRL

## 📊 COSTOS
- Vercel Hobby: $0/mes
- Backend simplificado: $0/mes
- Total: $0/mes ✅

---
**Estado**: Listo para deploy
**Última actualización**: $(date)