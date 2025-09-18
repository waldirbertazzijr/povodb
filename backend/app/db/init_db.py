"""
Database initialization module.

This module handles the initialization of the database connection and
ensures the database is properly set up when the application starts.
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from tenacity import retry, stop_after_attempt, wait_fixed, after_log

from app.db.session import AsyncSessionLocal
from app.core.config import settings

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(20),
    wait=wait_fixed(1),
    after=after_log(logger, logging.INFO),
)
async def check_database_connection() -> None:
    """
    Verify database connection is working.
    Retries several times with a 1-second wait between attempts.
    """
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


async def create_initial_data(db: AsyncSession) -> None:
    """
    Create initial data in the database if needed.
    This function can be expanded to seed the database with initial data.

    Args:
        db: Database session
    """
    # This function can be expanded to create initial data
    # For now, we're relying on the SQL initialization script
    pass


async def init_db() -> None:
    """
    Initialize database connections and create initial data.

    This function is called during application startup to ensure
    the database is properly connected and initialized.
    """
    try:
        # First check if the database is accessible
        await check_database_connection()

        # If we need to create initial data beyond what's in the SQL init script
        # we can do it here
        async with AsyncSessionLocal() as db:
            await create_initial_data(db)

        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
