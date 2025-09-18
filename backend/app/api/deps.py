from typing import AsyncGenerator, Callable, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

# Reusable dependency for database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session.

    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async for session in get_db():
        yield session


# Pagination parameters
def pagination_params(
    skip: int = 0,
    limit: int = 100,
) -> dict:
    """
    Get pagination parameters.

    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return

    Returns:
        dict: Dictionary with pagination parameters
    """
    return {"skip": skip, "limit": limit}


# Filter by active status (not deleted)
def active_only() -> bool:
    """
    Filter to only include active (not deleted) records.

    Returns:
        bool: True to filter for active records only
    """
    return True
