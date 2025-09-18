from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.db.session import get_db

router = APIRouter()


@router.get("", summary="Health check")
async def health_check():
    """
    Health check endpoint.

    Returns status information about the API service.
    """
    return {
        "status": "healthy",
        "service": "povodb-api",
        "version": "0.1.0"
    }


@router.get("/db", summary="Database health check")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    Database health check endpoint.

    Checks if the database connection is working properly.
    """
    try:
        # Simple query to check database connection
        result = await db.execute(text("SELECT 1"))
        if result.scalar_one() == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "message": "Database connection successful"
            }
        return {
            "status": "unhealthy",
            "database": "error",
            "message": "Database connection test failed"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "message": f"Database connection error: {str(e)}"
        }
