from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user
)
from datetime import timedelta
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalar_one_or_none()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with empleado role by default
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role="empleado"  # Default role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Login attempt for user: {user_credentials.email}")
        
        # Get user by email
        result = await db.execute(select(User).filter(User.email == user_credentials.email))
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(user_credentials.password, user.hashed_password):
            logger.warning(f"Invalid password for user: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"Successful login for user: {user_credentials.email}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for user {user_credentials.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error en el servidor",
        )

@router.post("/create-admin", response_model=UserResponse)
async def create_admin_user(db: AsyncSession = Depends(get_db)):
    """Create admin user for Escribanía Galmarini"""
    try:
        # Check if admin already exists
        result = await db.execute(select(User).filter(User.email == "diegogalmarini@gmail.com"))
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            logger.info("Admin user already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin user already exists"
            )
        
        # Create admin user
        hashed_password = get_password_hash("admin123")
        admin_user = User(
            email="diegogalmarini@gmail.com",
            hashed_password=hashed_password,
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        await db.commit()
        await db.refresh(admin_user)
        
        logger.info("Admin user created successfully")
        return admin_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear usuario administrador",
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user