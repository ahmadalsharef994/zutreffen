from fastapi import APIRouter
from app.api.v1.routes import users, places, checkins, health, auth

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(checkins.router, prefix="/checkins", tags=["checkins"])