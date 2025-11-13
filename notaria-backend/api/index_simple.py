from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tutor Ingesis API - Simplified",
    description="API simplificada para el tutor de Ingesis SRL - Escribanía Galmarini",
    version="1.0.0"
)

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://traewk90lkpb.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple data models
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

# Mock database and users
MOCK_USERS = {
    "diegogalmarini@gmail.com": {
        "password": "admin123",
        "role": "admin",
        "id": 1
    },
    "empleado@escribania.com": {
        "password": "empleado123", 
        "role": "empleado",
        "id": 2
    }
}

# Mock JWT token generation
def create_mock_token(email: str, role: str) -> str:
    import base64
    import json
    payload = {
        "sub": email,
        "role": role,
        "exp": 9999999999  # Far future
    }
    # Simple mock JWT (not secure for production)
    header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode()
    payload_enc = base64.b64encode(json.dumps(payload).encode()).decode()
    signature = base64.b64encode(b"mock_signature").decode()
    return f"{header}.{payload_enc}.{signature}"

@app.get("/")
async def root():
    return {"message": "Tutor Ingesis API - Simplified Version", "status": "running"}

@app.get("/api")
async def api_info():
    return {
        "message": "Tutor Ingesis API - Escribanía Galmarini (Simplified)",
        "version": "1.0.0",
        "mode": "simplified",
        "documentation": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Tutor Ingesis API - Simplified", "mode": "mock"}

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    try:
        logger.info(f"Login attempt for: {request.email}")
        
        # Check if user exists in mock database
        user = MOCK_USERS.get(request.email)
        if not user:
            logger.warning(f"User not found: {request.email}")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Check password
        if user["password"] != request.password:
            logger.warning(f"Invalid password for: {request.email}")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Create mock token
        token = create_mock_token(request.email, user["role"])
        
        logger.info(f"Login successful for: {request.email} with role: {user['role']}")
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            role=user["role"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

@app.post("/api/admin/init-db")
async def init_db():
    return {"status": "success", "message": "Mock database initialized", "users_count": len(MOCK_USERS)}

# Mock tutor endpoints
@app.post("/api/v1/tutor/chat")
async def tutor_chat(request: dict):
    question = request.get("question", "")
    
    # Mock responses for Ingesis SRL questions
    mock_responses = {
        "como usar ingesis": "Para usar Ingesis SRL, primero debes iniciar sesión con tus credenciales. Luego puedes acceder a los módulos de gestión de clientes, documentos y reportes.",
        "cliente": "En Ingesis SRL, puedes gestionar clientes desde el módulo 'Clientes'. Allí puedes agregar nuevos clientes, editar información existente y ver el historial.",
        "documento": "Para gestionar documentos en Ingesis SRL, ve al módulo 'Documentos'. Puedes subir archivos PDF, asignarlos a clientes y categorizarlos.",
        "reporte": "Los reportes en Ingesis SRL se generan desde el módulo 'Reportes'. Puedes crear reportes de clientes, documentos y actividades.",
        "configuracion": "La configuración de Ingesis SRL está en el menú 'Configuración'. Allí puedes modificar ajustes del sistema, usuarios y permisos."
    }
    
    # Find best matching response
    best_match = None
    question_lower = question.lower()
    
    for keyword, response in mock_responses.items():
        if keyword in question_lower:
            best_match = response
            break
    
    if not best_match:
        best_match = "Soy el tutor de Ingesis SRL. Puedo ayudarte con preguntas sobre cómo usar el sistema. ¿Qué necesitas saber?"
    
    return {
        "response": best_match,
        "sources": ["Manual de Ingesis SRL"],
        "confidence": 0.8
    }

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)