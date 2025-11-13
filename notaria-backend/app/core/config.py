from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite+aiosqlite:///./notaria.db"
    
    # Vercel deployment configuration
    VERCEL_URL: Optional[str] = None
    
    # AI API Configuration
    GEMINI_API_KEY: Optional[str] = "AIzaSyBaCkV4-EFwj36dfWvJCxWcUWY4dpJLUC0"
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
if settings.JWT_SECRET_KEY:
    settings.SECRET_KEY = settings.JWT_SECRET_KEY
