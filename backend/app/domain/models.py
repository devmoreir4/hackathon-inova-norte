from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserType(str, Enum):
    YOUNG = "young"
    ENTREPRENEUR = "entrepreneur"
    RETIREE = "retiree"
    GENERAL = "general"

class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class EventType(str, Enum):
    COOPERATIVE_FAIR = "cooperative_fair"
    LECTURE = "lecture"
    BUSINESS_ROUND = "business_round"
    EDUCATIONAL_ACTIVITY = "educational_activity"
    OTHER = "other"

class CommunityType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INVITE_ONLY = "invite_only"

class MembershipRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"

class User(Base):
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
    liked_by_user_1 = Column(Boolean, default=False) # For hardcoded user 1

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False)  # FK to Post
    author_id = Column(Integer, nullable=False)  # FK to User
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    parent_comment_id = Column(Integer, nullable=True)  # For nested comments

class Event(Base):
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
    __tablename__ = "event_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)  # FK to Event
    user_id = Column(Integer, nullable=False)   # FK to User
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    attended = Column(Boolean, default=False)
    feedback = Column(Text, nullable=True)

class Community(Base):
    __tablename__ = "communities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    community_type = Column(SQLEnum(CommunityType), default=CommunityType.PUBLIC)
    owner_id = Column(Integer, nullable=False)  # FK to User
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    active = Column(Boolean, default=True)
    member_count = Column(Integer, default=0)
    max_members = Column(Integer, nullable=True)
    image_url = Column(String(500), nullable=True)
    rules = Column(Text, nullable=True)

class CommunityMembership(Base):
    __tablename__ = "community_memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, nullable=False)  # FK to Community
    user_id = Column(Integer, nullable=False)       # FK to User
    role = Column(SQLEnum(MembershipRole), default=MembershipRole.MEMBER)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    active = Column(Boolean, default=True)

# ====== GAMIFICATION MODELS ======

class UserLevel(Base):
    __tablename__ = "user_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # FK to User
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(String(500), nullable=True)
    points_required = Column(Integer, default=0)
    category = Column(String(50), nullable=False)  # forum, events, community, education
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # FK to User
    badge_id = Column(Integer, nullable=False)  # FK to Badge
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    is_displayed = Column(Boolean, default=True)

class UserPoints(Base):
    __tablename__ = "user_points"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # FK to User
    points = Column(Integer, nullable=False)
    source = Column(String(50), nullable=False)  # forum_post, forum_comment, event_attendance, etc.
    source_id = Column(Integer, nullable=True)  # post_id, event_id, etc
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
