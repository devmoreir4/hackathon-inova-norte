from .health import health_router
from .users import user_router
from .communities import community_router
from .events import event_router
from . import forum
from .gamification import gamification_router
from .courses import course_router

__all__ = [
    "health_router",
    "user_router", 
    "community_router",
    "event_router",
    "forum",
    "gamification_router",
    "course_router"
]
