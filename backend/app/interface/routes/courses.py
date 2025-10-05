from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.models import Course, CourseEnrollment, User
from app.application.dto import (
    CourseCreate, CourseUpdate, CourseResponse,
    CourseEnrollmentCreate, CourseEnrollmentResponse
)
from app.application.services.gamification_service import GamificationService


course_router = APIRouter(prefix="/courses", tags=["Courses"])


@course_router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create course",
    description="Create a new course"
)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    instructor = db.query(User).filter(User.id == course.instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@course_router.get(
    "/",
    response_model=List[CourseResponse],
    summary="List courses",
    description="Get list of courses with optional filters"
)
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    
    if category:
        query = query.filter(Course.category == category)
    
    courses = query.offset(skip).limit(limit).all()
    return courses


@course_router.get(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Get course by ID",
    description="Get course details by ID"
)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


@course_router.put(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Update course",
    description="Update course information"
)
def update_course(
    course_id: int, 
    course_update: CourseUpdate, 
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course


@course_router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete course",
    description="Delete a course"
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    db.delete(course)
    db.commit()


@course_router.post(
    "/{course_id}/enroll",
    response_model=CourseEnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll in course",
    description="Enroll a user in a course"
)
def enroll_in_course(
    course_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    existing_enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.user_id == user_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already enrolled in this course"
        )
    
    enrollment = CourseEnrollment(course_id=course_id, user_id=user_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    gamification_service = GamificationService(db)
    gamification_service.add_points(
        user_id=user_id,
        source="course_enrollment",
        source_id=course_id,
        description=f"Inscrito no curso: {course.title}"
    )
    
    return enrollment


@course_router.get(
    "/user/{user_id}/enrollments",
    response_model=List[CourseEnrollmentResponse],
    summary="Get user enrollments",
    description="Get courses that a user is enrolled in"
)
def get_user_enrollments(
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
    
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return enrollments


@course_router.put(
    "/enrollments/{enrollment_id}/complete",
    response_model=CourseEnrollmentResponse,
    summary="Complete course",
    description="Mark a course enrollment as completed"
)
def complete_course(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.id == enrollment_id
    ).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    if enrollment.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course already completed"
        )
    
    enrollment.is_completed = True
    enrollment.completed_at = datetime.now()
    
    db.commit()
    db.refresh(enrollment)
    
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    course_title = course.title if course else "Curso"
    
    gamification_service = GamificationService(db)
    gamification_service.add_points(
        user_id=enrollment.user_id,
        source="course_completion",
        source_id=enrollment.course_id,
        description=f"Concluiu curso: {course_title}"
    )
    
    return enrollment


@course_router.get(
    "/{course_id}/enrollments",
    response_model=List[CourseEnrollmentResponse],
    summary="Get course enrollments",
    description="Get list of enrollments for a course"
)
def get_course_enrollments(
    course_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id
    ).offset(skip).limit(limit).all()
    
    return enrollments
