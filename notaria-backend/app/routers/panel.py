from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_current_user
from app.models.user import User
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_data(current_user: User = Depends(get_current_user)):
    """
    Get dashboard data for the authenticated user.
    """
    return {
        "message": "Panel de control - Escribanía Galmarini",
        "user": {
            "email": current_user.email,
            "role": current_user.role
        }
    }

@router.get("/users")
async def get_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all users (admin only).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access user management"
        )
    
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    return {
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at
            }
            for user in users
        ]
    }

@router.post("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user role (admin only).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can update roles"
        )
    
    if new_role not in ["admin", "empleado"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'admin' or 'empleado'"
        )
    
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.role = new_role
    await db.commit()
    
    return {
        "message": "User role updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }