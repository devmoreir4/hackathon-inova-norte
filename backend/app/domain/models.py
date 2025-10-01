"""
Domain models for Sicoob Fluminense
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserType(str, Enum):
    """Types of cooperative members"""
    YOUNG = "young"
    ENTREPRENEUR = "entrepreneur"
    RETIREE = "retiree"
    GENERAL = "general"

class ProjectStatus(str, Enum):
    """Project status"""
    PROPOSED = "proposed"
    VOTING = "voting"
    APPROVED = "approved"
    IN_EXECUTION = "in_execution"
    COMPLETED = "completed"
    REJECTED = "rejected"

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

class Project(Base):
    """Social impact project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PROPOSED)
    author_id = Column(Integer, nullable=False)  # FK to User
    proposed_at = Column(DateTime(timezone=True), server_default=func.now())
    voting_start = Column(DateTime(timezone=True), nullable=True)
    voting_end = Column(DateTime(timezone=True), nullable=True)
    votes_for = Column(Integer, default=0)
    votes_against = Column(Integer, default=0)
    estimated_budget = Column(String(50), nullable=True)
    beneficiary_community = Column(String(200), nullable=True)

class Vote(Base):
    """Project vote model"""
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)  # FK to Project
    user_id = Column(Integer, nullable=False)     # FK to User
    vote_for = Column(Boolean, nullable=False)    # True = for, False = against
    voted_at = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(Text, nullable=True)

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
