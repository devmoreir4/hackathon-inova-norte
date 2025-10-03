import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interface.routes import (
    health_router,
    user_router,
    community_router,
    event_router,
    forum_router
)
from app.interface.routes.rag import rag_router
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
app.include_router(health_router)
app.include_router(user_router, prefix="/api/v1")
app.include_router(community_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")
app.include_router(forum_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/api/v1")
