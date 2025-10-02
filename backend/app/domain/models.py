from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserType(str, Enum):
    """Types of cooperative members"""
    YOUNG = "young"
    ENTREPRENEUR = "entrepreneur"
    RETIREE = "retiree"
    GENERAL = "general"

class PostStatus(str, Enum):
    """Post status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class EventType(str, Enum):
    """Event types"""
    COOPERATIVE_FAIR = "cooperative_fair"
    LECTURE = "lecture"
    BUSINESS_ROUND = "business_round"
    EDUCATIONAL_ACTIVITY = "educational_activity"
    OTHER = "other"

class User(Base):
    """Cooperative member model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    user_type = Column(SQLEnum(UserType), default=UserType.GENERAL)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Post(Base):
    """Forum post model"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(SQLEnum(PostStatus), default=PostStatus.DRAFT)
    author_id = Column(Integer, nullable=False)  # FK to User
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)

class Comment(Base):
    """Post comment model"""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False)  # FK to Post
    author_id = Column(Integer, nullable=False)  # FK to User
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    parent_comment_id = Column(Integer, nullable=True)  # For nested comments

class Event(Base):
    """Event model"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    event_type = Column(SQLEnum(EventType), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    location = Column(String(200), nullable=False)
    address = Column(String(300), nullable=True)
    max_capacity = Column(Integer, nullable=True)
    registrations_open = Column(Boolean, default=True)
    organizer_id = Column(Integer, nullable=False)  # FK to User
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EventRegistration(Base):
    """Event registration model"""
    __tablename__ = "event_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)  # FK to Event
    user_id = Column(Integer, nullable=False)   # FK to User
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    attended = Column(Boolean, default=False)
    feedback = Column(Text, nullable=True)
