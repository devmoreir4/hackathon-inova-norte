from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.domain.models import UserType, ProjectStatus, EventType

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
    id: int
    active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Project DTOs
class ProjectBase(BaseModel):
    title: str
    description: str
    category: str
    estimated_budget: Optional[str] = None
    beneficiary_community: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[ProjectStatus] = None
    estimated_budget: Optional[str] = None
    beneficiary_community: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    status: ProjectStatus
    author_id: int
    proposed_at: datetime
    voting_start: Optional[datetime] = None
    voting_end: Optional[datetime] = None
    votes_for: int
    votes_against: int

    class Config:
        from_attributes = True

# Vote DTOs
class VoteBase(BaseModel):
    vote_for: bool
    comment: Optional[str] = None

class VoteCreate(VoteBase):
    project_id: int

class VoteResponse(VoteBase):
    id: int
    project_id: int
    user_id: int
    voted_at: datetime

    class Config:
        from_attributes = True

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
    id: int
    registrations_open: bool
    organizer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Event Registration DTOs
class EventRegistrationBase(BaseModel):
    feedback: Optional[str] = None

class EventRegistrationCreate(EventRegistrationBase):
    event_id: int

class EventRegistrationResponse(EventRegistrationBase):
    id: int
    event_id: int
    user_id: int
    registered_at: datetime
    attended: bool

    class Config:
        from_attributes = True
