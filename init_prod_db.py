#!/usr/bin/env python3
"""
Initialize the database with default admin user for production deployment.
This script should be run once after deployment to create the admin user.
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'notaria-backend'))

from app.database import create_tables, get_db
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select

async def init_production_db():
    """Initialize production database with admin user."""
    print("Initializing production database...")
    
    # Create tables
    await create_tables()
    print("✅ Database tables created")
    
    # Create admin user
    async for db in get_db():
        # Check if admin user already exists
        result = await db.execute(select(User).where(User.email == "diegogalmarini@gmail.com"))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("ℹ️  Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="diegogalmarini@gmail.com",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        await db.commit()
        print("✅ Admin user created successfully")
        print("📧 Email: diegogalmarini@gmail.com")
        print("🔑 Password: admin123")
        print("👑 Role: admin")
        break

if __name__ == "__main__":
    asyncio.run(init_production_db())