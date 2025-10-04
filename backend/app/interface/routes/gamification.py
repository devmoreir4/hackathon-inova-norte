from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.services.gamification_service import GamificationService
from app.application.dto import (
    UserStatsResponse, LeaderboardEntry, UserBadgeResponse, 
    BadgeResponse, UserPointsResponse
)

gamification_router = APIRouter(
    prefix="/gamification",
    tags=["Gamification"],
    responses={
        404: {"description": "User not found"},
        400: {"description": "Invalid data"},
    }
)

@gamification_router.get(
    "/users/{user_id}/stats",
    response_model=UserStatsResponse,
    summary="Get user gamification stats",
    description="Get comprehensive gamification statistics for a user"
)
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    service = GamificationService(db)
    return service.get_user_stats(user_id)

@gamification_router.get(
    "/leaderboard",
    response_model=List[LeaderboardEntry],
    summary="Get leaderboard",
    description="Get top users leaderboard"
)
def get_leaderboard(
    limit: int = Query(10, ge=1, le=50, description="Number of top users to return"),
    db: Session = Depends(get_db)
):
    service = GamificationService(db)
    return service.get_leaderboard(limit)

@gamification_router.get(
    "/users/{user_id}/badges",
    response_model=List[UserBadgeResponse],
    summary="Get user badges",
    description="Get all badges earned by a user"
)
def get_user_badges(user_id: int, db: Session = Depends(get_db)):
    service = GamificationService(db)
    return service.get_user_badges(user_id)

@gamification_router.get(
    "/badges",
    response_model=List[BadgeResponse],
    summary="Get all badges",
    description="Get all available badges in the system"
)
def get_all_badges(db: Session = Depends(get_db)):
    service = GamificationService(db)
    return service.get_all_badges()

@gamification_router.post(
    "/users/{user_id}/points",
    response_model=UserPointsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add points to user",
    description="Add points to user for specific action (admin only)"
)
def add_points_to_user(
    user_id: int,
    source: str = Query(..., description="Source of points (forum_post, event_attendance, etc.)"),
    source_id: int = Query(None, description="ID of the source object"),
    description: str = Query(None, description="Description of the points"),
    db: Session = Depends(get_db)
):
    service = GamificationService(db)
    return service.add_points(user_id, source, source_id, description)

@gamification_router.get(
    "/users/{user_id}/points",
    response_model=List[UserPointsResponse],
    summary="Get user points history",
    description="Get points history for a user"
)
def get_user_points_history(
    user_id: int,
    limit: int = Query(20, ge=1, le=100, description="Number of points records to return"),
    db: Session = Depends(get_db)
):
    from sqlalchemy import desc
    from app.domain.models import UserPoints
    
    points = db.query(UserPoints).filter(
        UserPoints.user_id == user_id
    ).order_by(desc(UserPoints.created_at)).limit(limit).all()
    
    return [UserPointsResponse.model_validate(point) for point in points]
