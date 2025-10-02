from .health import health_router
from .users import user_router
from .communities import community_router
from .events import event_router
from .forum import forum_router

__all__ = [
    "health_router",
    "user_router", 
    "community_router",
    "event_router",
    "forum_router"
]
