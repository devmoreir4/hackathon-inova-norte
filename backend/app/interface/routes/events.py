from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.infrastructure.database import get_db
from app.domain.models import Event, EventRegistration, User
from app.application.dto import (
    EventCreate, EventUpdate, EventResponse,
    EventRegistrationCreate, EventRegistrationResponse
)
from app.application.services.gamification_service import GamificationService

event_router = APIRouter(prefix="/events", tags=["Events"])

@event_router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new event",
    description="Create a new community event"
)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@event_router.get(
    "/",
    response_model=List[EventResponse],
    summary="List events",
    description="Get list of events with optional filters"
)
def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: Optional[str] = None,
    registrations_open: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    if registrations_open is not None:
        query = query.filter(Event.registrations_open == registrations_open)
    
    events = query.offset(skip).limit(limit).all()
    return events

@event_router.get(
    "/user/{user_id}",
    response_model=List[EventResponse],
    summary="Get user's events",
    description="Get events organized by a specific user"
)
def get_user_events(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    events = db.query(Event).filter(
        Event.organizer_id == user_id
    ).offset(skip).limit(limit).all()
    return events

@event_router.get(
    "/user/{user_id}/registrations",
    response_model=List[EventRegistrationResponse],
    summary="Get user's event registrations",
    description="Get events that a user is registered for"
)
def get_user_registrations(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    registrations = db.query(EventRegistration).filter(
        EventRegistration.user_id == user_id
    ).offset(skip).limit(limit).all()
    return registrations

@event_router.get(
    "/calendar/range",
    response_model=List[EventResponse],
    summary="Get events by date range",
    description="Get events within a date range (calendar view)"
)
def get_events_by_range(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    events = db.query(Event).filter(
        and_(
            func.date(Event.start_date) >= start_date,
            func.date(Event.start_date) <= end_date
        )
    ).order_by(Event.start_date).all()
    return events

@event_router.get(
    "/calendar/month/{year}/{month}",
    response_model=List[EventResponse],
    summary="Get events by month",
    description="Get all events for a specific month (calendar view)"
)
def get_events_by_month(year: int, month: int, db: Session = Depends(get_db)):
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )
    
    # Get first and last day of the month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    start_date = datetime(year, month, 1).date()
    end_date = datetime(next_year, next_month, 1).date()
    
    events = db.query(Event).filter(
        and_(
            func.date(Event.start_date) >= start_date,
            func.date(Event.start_date) < end_date
        )
    ).order_by(Event.start_date).all()
    return events

@event_router.get(
    "/calendar/{date}",
    response_model=List[EventResponse],
    summary="Get events by date",
    description="Get events for a specific date (calendar view)"
)
def get_events_by_date(date: date, db: Session = Depends(get_db)):
    events = db.query(Event).filter(
        func.date(Event.start_date) == date
    ).all()
    return events

@event_router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event by ID",
    description="Get event details by ID"
)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@event_router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update event",
    description="Update event information"
)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event

@event_router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete event",
    description="Delete an event"
)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(event)
    db.commit()

# Event Registration endpoints
@event_router.post(
    "/{event_id}/register",
    response_model=EventRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register for event",
    description="Register a user for an event"
)
def register_for_event(
    event_id: int,
    user_id: int,
    registration: EventRegistrationCreate,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not event.registrations_open:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registrations are closed for this event"
        )
    
    existing_registration = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id,
        EventRegistration.user_id == user_id
    ).first()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered for this event"
        )
    
    if event.max_capacity:
        current_registrations = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id
        ).count()
        
        if current_registrations >= event.max_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is at full capacity"
            )
    
    # Create registration
    registration_data = registration.model_dump()
    registration_data['event_id'] = event_id
    registration_data['user_id'] = user_id
    
    db_registration = EventRegistration(**registration_data)
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    
    gamification_service = GamificationService(db)
    gamification_service.add_points(
        user_id=user_id,
        source="event_registration",
        source_id=event_id,
        description=f"Inscreveu-se no evento: {event.title}"
    )
    
    return db_registration

@event_router.get(
    "/{event_id}/registrations",
    response_model=List[EventRegistrationResponse],
    summary="List event registrations",
    description="Get list of registrations for an event"
)
def list_event_registrations(
    event_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    registrations = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id
    ).offset(skip).limit(limit).all()
    
    return registrations

@event_router.put(
    "/{event_id}/registrations/{registration_id}",
    response_model=EventRegistrationResponse,
    summary="Update event registration",
    description="Update registration details (e.g., mark as attended)"
)
def update_registration(
    event_id: int,
    registration_id: int,
    attended: bool,
    feedback: Optional[str] = None,
    db: Session = Depends(get_db)
):
    registration = db.query(EventRegistration).filter(
        EventRegistration.id == registration_id,
        EventRegistration.event_id == event_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    registration.attended = attended
    if feedback is not None:
        registration.feedback = feedback
    
    db.commit()
    db.refresh(registration)
    return registration

@event_router.delete(
    "/{event_id}/registrations/{registration_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel registration",
    description="Cancel a user's registration for an event"
)
def cancel_registration(
    event_id: int,
    registration_id: int,
    db: Session = Depends(get_db)
):
    registration = db.query(EventRegistration).filter(
        EventRegistration.id == registration_id,
        EventRegistration.event_id == event_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    db.delete(registration)
    db.commit()
