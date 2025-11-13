from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import with error handling for Vercel deployment
try:
    from app.routers import auth, tutor, panel
    from app.database import engine, Base
    from app.models.user import User
    from app.core.security import get_password_hash
    from sqlalchemy import select
    IMPORT_SUCCESS = True
except ImportError as e:
    logger.error(f"Import error: {e}")
    IMPORT_SUCCESS = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not IMPORT_SUCCESS:
        logger.error("Failed to import required modules")
        yield
        return
        
    try:
        logger.info("Starting Tutor Ingesis API...")
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created")
        
        # Create default admin user if it doesn't exist
        from app.database import async_session_maker
        async with async_session_maker() as session:
            try:
                result = await session.execute(select(User).where(User.email == "diegogalmarini@gmail.com"))
                existing_user = result.scalar_one_or_none()
                
                if not existing_user:
                    admin_user = User(
                        email="diegogalmarini@gmail.com",
                        hashed_password=get_password_hash("admin123"),
                        role="admin",
                        is_active=True
                    )
                    session.add(admin_user)
                    await session.commit()
                    logger.info("✅ Admin user created: diegogalmarini@gmail.com")
                else:
                    logger.info("ℹ️  Admin user already exists")
            except Exception as e:
                logger.error(f"Error creating admin user: {e}")
                await session.rollback()
    except Exception as e:
        logger.error(f"Error during startup: {e}")
    
    yield

app = FastAPI(
    title="Tutor Ingesis API",
    description="API para el tutor de Ingesis SRL - Escribanía Galmarini",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://traewk90lkpb.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes (only if imports succeeded)
if IMPORT_SUCCESS:
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(tutor.router, prefix="/api/v1/tutor", tags=["tutor"])
    app.include_router(panel.router, prefix="/api/v1/panel", tags=["panel"])

@app.get("/api/health")
async def health_check():
    if not IMPORT_SUCCESS:
        return {"status": "error", "message": "Failed to import required modules", "service": "Tutor Ingesis API"}
    return {"status": "healthy", "service": "Tutor Ingesis API"}

@app.get("/api")
async def api_info():
    return {
        "message": "Tutor Ingesis API - Escribanía Galmarini",
        "version": "1.0.0",
        "documentation": "/docs",
        "import_status": IMPORT_SUCCESS
    }

# Fallback routes for when imports fail
@app.post("/api/admin/init-db")
async def init_db_fallback():
    if not IMPORT_SUCCESS:
        return {"status": "error", "message": "Database initialization failed - import error"}
    return {"status": "error", "message": "Database not properly configured"}

@app.post("/api/auth/login")
async def login_fallback():
    if not IMPORT_SUCCESS:
        return {"status": "error", "message": "Login failed - import error"}
    return {"status": "error", "message": "Authentication not properly configured"}

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
