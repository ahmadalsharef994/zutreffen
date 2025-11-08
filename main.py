from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from routes.api import api_router
from core.config import config
import os

# Middleware to disable caching for frontend files
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.endswith(('.html', '.css', '.js')) or request.url.path == '/':
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

def create_app() -> FastAPI:
    app = FastAPI(
    title=config.PROJECT_NAME,
        version="1.0.0",
    openapi_url=f"{config.API_V1_STR}/openapi.json",
    )
    
    # Add no-cache middleware first
    app.add_middleware(NoCacheMiddleware)
    
    # Set up CORS - Allow frontend to access API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router, prefix=config.API_V1_STR)
    
    # Serve static files (frontend)
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.exists(frontend_path):
        app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/")
    async def root():
        # Serve the frontend index.html
        frontend_index = os.path.join(frontend_path, "index.html")
        if os.path.exists(frontend_index):
            return FileResponse(frontend_index)
        return {
            "message": "Welcome to Zutreffen API",
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "frontend_url": "/static/index.html"
        }
    
    return app

app = create_app()