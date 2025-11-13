from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Use aiosqlite for async SQLite support
# For SQLite, we need to use aiosqlite://// format
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Create async session maker for use in lifespan
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()