from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interface.routes import router
from app.infrastructure.database import create_tables

create_tables()

app = FastAPI(
    title="Sicoob API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Sicoob API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "message": "API working correctly",
        "version": "1.0.0",
    }
