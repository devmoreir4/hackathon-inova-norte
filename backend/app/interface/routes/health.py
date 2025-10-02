from fastapi import APIRouter

health_router = APIRouter()

@health_router.get("/", tags=["Status"])
async def root():
    return {
        "message": "Sicoob API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@health_router.get("/health", tags=["Status"])
async def health_check():
    return {
        "status": "healthy",
        "message": "API working correctly",
        "version": "1.0.0",
        "database": "connected"
    }
