from fastapi import APIRouter

from app.api.v1.endpoints import health, politicians, bills, votes, contributions

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(politicians.router, prefix="/politicians", tags=["politicians"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(contributions.router, prefix="/contributions", tags=["contributions"])
