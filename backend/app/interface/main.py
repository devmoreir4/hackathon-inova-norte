from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interface.routes import router
from app.infrastructure.database import create_tables

# Create database tables on startup
create_tables()

app = FastAPI(
    title="Sicoob Fluminense API",
    description="""
    ## Community Engagement and Sustainable Development API
    
    This API was developed for the Sicoob Fluminense challenge, focusing on:
    
    * **Social Impact Projects** - Members can propose and vote on projects
    * **Community Events** - Calendar of events and cooperative fairs
    * **Discussion Forum** - Space for knowledge exchange
    * **AI Chatbot** - Financial education and member support
    
    ### Cooperative Principles
    - Community Interest
    - Education, Training and Information
    
    ### Main Features
    - Member Management
    - Project Voting System
    - Event Calendar
    - Community Forum
    - AI Chatbot
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware to allow requests from Flutter frontend
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
        "message": "Sicoob Fluminense API - Community Engagement",
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
        "database": "connected"
    }

