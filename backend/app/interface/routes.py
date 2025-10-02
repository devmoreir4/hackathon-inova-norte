from fastapi import APIRouter
from app.interface.user_routes import user_router
from app.interface.forum_routes import forum_router

router = APIRouter()

# Include sub-routers
router.include_router(user_router)
router.include_router(forum_router)
