from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.dto import UserCreate, UserUpdate, UserResponse
from app.domain.models import User

user_router = APIRouter(
    prefix="/users",
    tags=["Cooperative Members"],
    responses={
        404: {"description": "Member not found"},
        400: {"description": "Invalid data"},
    }
)

@user_router.post(
    "/", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new member",
    description="Register a new cooperative member"
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.get(
    "/", 
    response_model=List[UserResponse],
    summary="List members",
    description="Returns list of cooperative members with pagination"
)
def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.active == True).offset(skip).limit(limit).all()
    return users

@user_router.get(
    "/{user_id}", 
    response_model=UserResponse,
    summary="Get member by ID",
    description="Returns data of a specific member"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Member not found"
        )
    return user

@user_router.put(
    "/{user_id}", 
    response_model=UserResponse,
    summary="Update member",
    description="Updates data of an existing member"
)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Member not found"
        )
    
    # Update only provided fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@user_router.delete(
    "/{user_id}",
    summary="Deactivate member",
    description="Deactivates a member (soft delete)"
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Member not found"
        )
    
    user.active = False
    db.commit()
    return {"message": "Member deactivated successfully"}

@user_router.get(
    "/email/{email}", 
    response_model=UserResponse,
    summary="Get member by email",
    description="Returns member data by email"
)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Member not found"
        )
    return user
