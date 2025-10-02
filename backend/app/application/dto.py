from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from app.domain.models import UserType, PostStatus, EventType

# User DTOs
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

# Post DTOs
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
    status: PostStatus
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    views_count: int
    likes_count: int

# Comment DTOs
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

# Event DTOs
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
    pass

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

# Event Registration DTOs
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
