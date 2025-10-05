from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.domain.models import UserLevel, Badge, UserBadge, UserPoints, User
from app.application.dto import (
    UserLevelResponse, BadgeResponse, UserBadgeResponse, 
    UserPointsResponse, UserStatsResponse, LeaderboardEntry
)

class GamificationService:
    
    POINTS_CONFIG = {
        'forum_post': 10,
        'forum_comment': 5,
        'forum_like': 2,
        'event_attendance': 15,
        'event_registration': 5,
        'community_join': 8,
        'community_create': 20,
        'first_post': 25,
        'active_member': 30,
        'course_enrollment': 10,
        'course_completion': 50,
    }
    
    LEVEL_REQUIREMENTS = [
        0,      # Level 1
        100,    # Level 2
        250,    # Level 3
        500,    # Level 4
        1000,   # Level 5
        2000,   # Level 6
        3500,   # Level 7
        5500,   # Level 8
        8000,   # Level 9
        12000,  # Level 10
    ]
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_points(self, user_id: int, source: str, source_id: Optional[int] = None, 
                   description: Optional[str] = None) -> UserPointsResponse:
        points = self.POINTS_CONFIG.get(source, 0)
        
        user_points = UserPoints(
            user_id=user_id,
            points=points,
            source=source,
            source_id=source_id,
            description=description
        )
        self.db.add(user_points)
        
        self._update_user_level(user_id, points)
        
        self._check_badges(user_id)
        
        self.db.commit()
        self.db.refresh(user_points)
        
        return UserPointsResponse.model_validate(user_points)
    
    def _update_user_level(self, user_id: int, points: int):
        user_level = self.db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
        
        if not user_level:
            user_level = UserLevel(
                user_id=user_id,
                level=1,
                experience_points=0,
                total_points=0
            )
            self.db.add(user_level)
        
        if user_level.total_points is None:
            user_level.total_points = 0
        if user_level.experience_points is None:
            user_level.experience_points = 0
        
        user_level.total_points += points
        user_level.experience_points += points
        
        new_level = self._calculate_level(user_level.total_points)
        if new_level > user_level.level:
            user_level.level = new_level
        
        self.db.commit()
    
    def _calculate_level(self, total_points: int) -> int:
        level = 1
        for i, requirement in enumerate(self.LEVEL_REQUIREMENTS):
            if total_points >= requirement:
                level = i + 1
            else:
                break
        return min(level, len(self.LEVEL_REQUIREMENTS))
    
    def _check_badges(self, user_id: int):
        user_level = self.db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
        if not user_level:
            return
        
        user_badges = self.db.query(UserBadge.badge_id).filter(UserBadge.user_id == user_id).all()
        user_badge_ids = [ub.badge_id for ub in user_badges]
        
        eligible_badges = self.db.query(Badge).filter(
            Badge.points_required <= user_level.total_points,
            ~Badge.id.in_(user_badge_ids)
        ).all()
        
        for badge in eligible_badges:
            user_badge = UserBadge(
                user_id=user_id,
                badge_id=badge.id
            )
            self.db.add(user_badge)
    
    def get_user_stats(self, user_id: int) -> UserStatsResponse:
        user_level = self.db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
        if not user_level:
            user_level = UserLevel(user_id=user_id, level=1, experience_points=0, total_points=0)
            self.db.add(user_level)
            self.db.commit()
        
        badges_count = self.db.query(UserBadge).filter(UserBadge.user_id == user_id).count()
        
        recent_badges = self.db.query(Badge).join(
            UserBadge, Badge.id == UserBadge.badge_id
        ).filter(
            UserBadge.user_id == user_id
        ).order_by(desc(UserBadge.earned_at)).limit(5).all()
        
        recent_points = self.db.query(UserPoints).filter(
            UserPoints.user_id == user_id
        ).order_by(desc(UserPoints.created_at)).limit(10).all()
        
        return UserStatsResponse(
            user_id=user_id,
            level=user_level.level,
            experience_points=user_level.experience_points,
            total_points=user_level.total_points,
            badges_count=badges_count,
            recent_badges=[BadgeResponse.model_validate(badge) for badge in recent_badges],
            recent_points=[UserPointsResponse.model_validate(point) for point in recent_points]
        )
    
    def get_leaderboard(self, limit: int = 10) -> List[LeaderboardEntry]:
        leaderboard = self.db.query(
            User.id,
            User.name,
            UserLevel.level,
            UserLevel.total_points,
            func.count(UserBadge.id).label('badges_count')
        ).join(UserLevel, User.id == UserLevel.user_id)\
         .outerjoin(UserBadge, User.id == UserBadge.user_id)\
         .group_by(User.id, User.name, UserLevel.level, UserLevel.total_points)\
         .order_by(desc(UserLevel.total_points))\
         .limit(limit).all()
        
        result = []
        for rank, (user_id, user_name, level, total_points, badges_count) in enumerate(leaderboard, 1):
            result.append(LeaderboardEntry(
                user_id=user_id,
                user_name=user_name,
                level=level,
                total_points=total_points,
                badges_count=badges_count or 0,
                rank=rank
            ))
        
        return result
    
    def get_user_badges(self, user_id: int) -> List[UserBadgeResponse]:
        user_badges = self.db.query(UserBadge).filter(
            UserBadge.user_id == user_id
        ).order_by(desc(UserBadge.earned_at)).all()
        
        return [UserBadgeResponse.model_validate(ub) for ub in user_badges]
    
    def get_all_badges(self) -> List[BadgeResponse]:
        badges = self.db.query(Badge).all()
        return [BadgeResponse.model_validate(badge) for badge in badges]
