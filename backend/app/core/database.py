"""
Database Connection Management

This module handles async database connections using SQLAlchemy 2.0's async features.
Understanding async database access is crucial for scalable applications.

Why Async Database?
- Non-blocking: While database query runs, the server can handle other requests
- Better resource utilization: One server process can handle many concurrent operations
- Required for FastAPI's performance benefits

SQLAlchemy 2.0 Async Flow:
1. create_async_engine: Creates connection pool (reuses connections)
2. async_sessionmaker: Factory that creates database sessions
3. AsyncSession: Represents a single database transaction
4. get_db(): FastAPI dependency that provides a session per request
"""
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create async database engine
# This manages the connection pool and is shared across all requests
engine: AsyncEngine = create_async_engine(
    settings.database.DATABASE_URL,

    # Log SQL queries in debug mode (helps with debugging, disable in production)
    echo=settings.DEBUG,

    # Connection pool configuration
    pool_size=settings.database.DATABASE_POOL_SIZE,
    max_overflow=settings.database.DATABASE_MAX_OVERFLOW,

    # Time to wait for a connection from pool before timeout (seconds)
    pool_timeout=30,

    # How long to wait before recycling connections (prevents stale connections)
    pool_recycle=3600,

    # Enable SQLAlchemy 2.0 style (future=True is default in 2.0)
    future=True,
)

# Create session factory
# async_sessionmaker is a callable that returns new AsyncSession objects
AsyncSessionLocal: async_sessionmaker = async_sessionmaker(
    engine,
    class_=AsyncSession,

    # Don't expire objects after commit (better for async workflows)
    expire_on_commit=False,

    # Automatically flush pending changes before queries
    autoflush=True,
)

# Base class for all SQLAlchemy models
# All database models will inherit from this
Base = declarative_base()

@event.listens_for(engine.sync_engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    """Event listener that runs when database connection is established"""
    logger.debug("New database connection established")


async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides a database session.

    How it works:
    1. Each request that needs database access calls this function
    2. It creates a new AsyncSession from the pool
    3. The session is automatically closed when the request finishes
    4. All database operations within the request use the same session

    Usage in endpoint:
    @app.get("/users")
    async def get_users(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User))
        return result.scalars().all()

    Yields:
        AsyncSession: Database session for the current request context
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # If no exceptions, commit any pending changes
            await session.commit()
        except Exception:
            # On error, rollback the transaction
            await session.rollback()
            raise
        finally:
            # Session automatically closed by context manager
            await session.close()