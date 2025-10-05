from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from app.domain.models import UserType, PostStatus, EventType, CommunityType, MembershipRole, CourseCategory


T = TypeVar('T')


class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of items to return")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(cls, items: List[T], total: int, skip: int, limit: int):
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_next=skip + limit < total,
            has_previous=skip > 0
        )


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    user_type: UserType = UserType.GENERAL


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    user_type: Optional[UserType] = None
    active: Optional[bool] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class PostBase(BaseModel):
    title: str
    content: str
    category: str


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    status: Optional[PostStatus] = None


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    category: str
    status: PostStatus
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    views_count: int
    likes_count: int
    liked_by_user_1: bool


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int
    author_id: int
    parent_comment_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    parent_comment_id: Optional[int] = None


class EventBase(BaseModel):
    title: str
    description: str
    event_type: EventType
    start_date: datetime
    end_date: Optional[datetime] = None
    location: str
    address: Optional[str] = None
    max_capacity: Optional[int] = None


class EventCreate(EventBase):
    organizer_id: int


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    address: Optional[str] = None
    max_capacity: Optional[int] = None
    registrations_open: Optional[bool] = None


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    registrations_open: bool
    organizer_id: int
    created_at: datetime


class EventRegistrationBase(BaseModel):
    feedback: Optional[str] = None


class EventRegistrationCreate(EventRegistrationBase):
    event_id: int


class EventRegistrationResponse(EventRegistrationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    event_id: int
    user_id: int
    registered_at: datetime
    attended: bool


class CommunityBase(BaseModel):
    name: str
    description: str
    community_type: CommunityType = CommunityType.PUBLIC
    max_members: Optional[int] = None
    image_url: Optional[str] = None
    rules: Optional[str] = None


class CommunityCreate(CommunityBase):
    owner_id: int


class CommunityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    community_type: Optional[CommunityType] = None
    max_members: Optional[int] = None
    image_url: Optional[str] = None
    rules: Optional[str] = None
    active: Optional[bool] = None


class CommunityResponse(CommunityBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    active: bool
    member_count: int


class CommunityMembershipBase(BaseModel):
    pass


class CommunityMembershipCreate(CommunityMembershipBase):
    community_id: int
    user_id: int
    role: MembershipRole = MembershipRole.MEMBER


class CommunityMembershipUpdate(BaseModel):
    role: Optional[MembershipRole] = None
    active: Optional[bool] = None


class CommunityMembershipResponse(CommunityMembershipBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    community_id: int
    user_id: int
    role: MembershipRole
    joined_at: datetime
    active: bool


class UserLevelBase(BaseModel):
    level: int
    experience_points: int
    total_points: int


class UserLevelResponse(UserLevelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class BadgeBase(BaseModel):
    name: str
    description: str
    icon_url: Optional[str] = None
    points_required: int
    category: str


class BadgeResponse(BadgeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class UserBadgeBase(BaseModel):
    is_displayed: bool = True


class UserBadgeResponse(UserBadgeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    badge_id: int
    earned_at: datetime


class UserPointsBase(BaseModel):
    points: int
    source: str
    source_id: Optional[int] = None
    description: Optional[str] = None


class UserPointsResponse(UserPointsBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime


class UserStatsResponse(BaseModel):
    user_id: int
    level: int
    experience_points: int
    total_points: int
    badges_count: int
    recent_badges: List[BadgeResponse]
    recent_points: List[UserPointsResponse]


class LeaderboardEntry(BaseModel):
    user_id: int
    user_name: str
    level: int
    total_points: int
    badges_count: int
    rank: int


class CourseBase(BaseModel):
    title: str
    description: str
    category: CourseCategory
    points_reward: int = 50
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    content: Optional[str] = None


class CourseCreate(CourseBase):
    instructor_id: int


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[CourseCategory] = None
    points_reward: Optional[int] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    content: Optional[str] = None


class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    instructor_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class CourseEnrollmentBase(BaseModel):
    pass


class CourseEnrollmentCreate(CourseEnrollmentBase):
    course_id: int
    user_id: int


class CourseEnrollmentResponse(CourseEnrollmentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    course_id: int
    user_id: int
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    is_completed: bool
