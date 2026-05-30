from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User

async def seed_admin(db: AsyncSession) -> None:
    """Create the first admin user if it doesn't exist."""
    result = await db.execute(select(User).where(User.email == settings.FIRST_ADMIN_EMAIL))
    if result.scalar_one_or_none():
        return

    admin_user = User(
        email=settings.FIRST_ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
        full_name=settings.FIRST_ADMIN_NAME,
        role="admin",
        is_active=True,
    )
    db.add(admin_user)
    await db.commit()
