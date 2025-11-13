from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tutor, panel
from app.database import engine, Base
import asyncio

app = FastAPI(title="NotarIA Backend", version="1.0.0")

# Create database tables (async)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Initialize tables on startup
@app.on_event("startup")
async def startup_event():
    await create_tables()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(tutor.router, prefix="/api/v1/tutor", tags=["tutor"])
app.include_router(panel.router, prefix="/api/v1/panel", tags=["panel"])

@app.get("/")
async def root():
    return {"message": "NotarIA Backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}