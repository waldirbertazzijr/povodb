from typing import AsyncGenerator, Generator
import sqlite3
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event, create_engine, Engine

from app.core.config import settings

# Create async engine for the database
async_engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# For Alembic migrations and utilities that need sync engine
sync_engine = create_engine(
    str(settings.DATABASE_URL).replace("+asyncpg", ""),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# Set up pragma for SQLite (if used for testing)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if hasattr(sqlite3, 'Connection') and isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Create sessionmakers
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.

    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# For testing and CLI commands that need sync sessions
def get_sync_db() -> Generator:
    """
    Get a synchronous database session.

    Yields:
        Session: SQLAlchemy sync session
    """
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
