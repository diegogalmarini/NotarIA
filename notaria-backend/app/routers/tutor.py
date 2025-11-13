from fastapi import APIRouter, Depends, HTTPException
from app.schemas.tutor import ChatRequest, ChatResponse
from app.core.security import get_current_user
from app.models.user import User
import os
from typing import Optional
import httpx
from app.core.config import settings

router = APIRouter()

def load_knowledge_base() -> str:
    """Load the knowledge base from file"""
    knowledge_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge-base.md')
    try:
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Knowledge base not found."

def load_system_prompt() -> str:
    """Load the system prompt from file"""
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'INSTRUCCIONES_GPT_COMPACTAS.txt')
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful tutor assistant for NotarIA."

async def call_ai_api(prompt: str) -> str:
    """Call AI API (Gemini) with system instructions"""
    from app.services.rag_service import get_tutor_response
    
    # Combine system instructions with user prompt
    system_prompt = load_system_prompt()
    knowledge = load_knowledge_base()
    
    final_prompt = f"""{system_prompt}

Contexto del manual de Ingesis:
{knowledge}

Pregunta del usuario:
{prompt}

Por favor, proporciona una respuesta basada EXCLUSIVAMENTE en el manual oficial de Ingesis SRL. Si la información no está en el manual, indícalo claramente y sugiere contactar al soporte técnico."""
    
    return await get_tutor_response(final_prompt)

@router.post("/chat", response_model=ChatResponse)
async def handle_chat_request(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Handle chat requests from authenticated users.
    Combines system prompt, knowledge base, and user message to generate AI response.
    """
    try:
        response_text = await call_ai_api(request.message)
        
        return ChatResponse(answer=response_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the tutor service"""
    return {"status": "healthy", "service": "tutor"}
