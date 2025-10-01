from fastapi import APIRouter
from app.interface.user_routes import user_router

router = APIRouter()

# Include sub-routers
router.include_router(user_router)
