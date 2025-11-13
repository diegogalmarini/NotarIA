# NotarIA - Sistema de Gestión Notarial Inteligente

## Sprint Cero - Implementación Completa

NotarIA es un sistema de gestión notarial que incluye un asistente de IA especializado en derecho notarial (Tutor Ingesis).

## 🚀 Características Implementadas

### Backend (FastAPI)
- ✅ Autenticación JWT completa (login/registro)
- ✅ Base de datos SQLite con SQLAlchemy async
- ✅ Endpoints RESTful protegidos
- ✅ Integración con IA (Gemini/OpenAI) - preparada
- ✅ Sistema RAG con base de conocimientos notariales

### Frontend (Next.js)
- ✅ PWA con diseño responsive
- ✅ Sistema de autenticación completo
- ✅ Interfaz de chat con Tutor Ingesis
- ✅ Panel de control (placeholder)
- ✅ Rutas protegidas

## 📁 Estructura del Proyecto

```
notaria-backend/
├── app/
│   ├── routers/          # Endpoints API
│   │   ├── auth.py       # Autenticación
│   │   ├── tutor.py      # Chat con IA
│   │   └── panel.py      # Panel de control
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Pydantic schemas
│   ├── core/             # Configuración y seguridad
│   ├── data/             # Base de conocimientos
│   └── services/         # Servicios de IA
├── requirements.txt
└── .env

notaria-frontend/
├── src/
│   ├── app/              # Rutas Next.js
│   │   ├── login/        # Página de login
│   │   ├── dashboard/  # Panel principal
│   │   │   ├── tutor/    # Chat Tutor Ingesis
│   │   │   └── panel/    # Panel de control
│   └── context/          # Contexto de autenticación
├── package.json
└── tailwind.config.js
```

## 🛠️ Instalación y Configuración

### Backend
```bash
cd notaria-backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd notaria-frontend
npm install
npm run dev
```

## 🔑 Credenciales de Prueba

Email: `test@notaria.com`
Contraseña: `test123`

## 🧪 Flujo de Uso

1. **Login**: Accede a http://localhost:3000/login
2. **Dashboard**: Visualiza las opciones disponibles
3. **Tutor Ingesis**: Consulta sobre derecho notarial
4. **Chat**: Pregunta sobre procedimientos, documentos, tarifas, etc.

## 📚 Base de Conocimientos

El sistema incluye:
- Información sobre servicios notariales
- Procedimientos y requisitos
- Tarifas y tiempos de entrega
- Preguntas frecuentes
- Marco legal

## 🤖 Tutor Ingesis

El asistente de IA está configurado para:
- Responder preguntas sobre derecho notarial
- Proporcionar información sobre trámites
- Guiar sobre documentación requerida
- Explicar procedimientos paso a paso

## 🔧 Configuración de IA

Para activar la IA real, configura las API keys en el archivo `.env`:

```env
GEMINI_API_KEY=tu-api-key-aqui
# o
OPENAI_API_KEY=tu-api-key-aqui
```

## 🚧 Próximos Pasos

- [ ] Implementar panel de control administrativo
- [ ] Agregar gestión de usuarios
- [ ] Integrar IA real (Gemini/OpenAI)
- [ ] Implementar base de datos PostgreSQL
- [ ] Agregar más contenido a la base de conocimientos
- [ ] Implementar sistema de roles avanzado

## 📄 Licencia

Este proyecto está en desarrollo para fines educativos.