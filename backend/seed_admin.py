#!/usr/bin/env python
"""
Run this script to create the first admin user.
Usage: python seed_admin.py
"""

import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User

async def create_admin():
    """Create the first admin user if it doesn't exist"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Check if admin exists
        result = await session.execute(
            select(User).where(User.email == settings.FIRST_ADMIN_EMAIL)
        )
        admin = result.scalar_one_or_none()

        if admin:
            print(f"Admin user already exists: {admin.email}")
            return

        # Create admin
        admin_user = User(
            email=settings.FIRST_ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
            full_name=settings.FIRST_ADMIN_NAME,
            role="admin",
            is_active=True,
        )

        session.add(admin_user)
        await session.commit()
        print(f"✅ Admin user created: {settings.FIRST_ADMIN_EMAIL}")
        print(f"   Password: {settings.FIRST_ADMIN_PASSWORD}")
        print("   Please change this password after first login!")

if __name__ == "__main__":
    asyncio.run(create_admin())