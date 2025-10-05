import pytest
from fastapi.testclient import TestClient

def test_create_course(client: TestClient):
    # Create instructor
    user_data = {
        "name": "Test Instructor",
        "email": "instructor@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    instructor_id = user_response.json()["id"]
    
    course_data = {
        "title": "Test Course",
        "description": "This is a test course description",
        "category": "financial_education",
        "instructor_id": instructor_id,
        "points_reward": 50
    }
    
    response = client.post("/api/v1/courses/", json=course_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == course_data["title"]
    assert data["instructor_id"] == instructor_id

def test_get_courses_list(client: TestClient):
    # Create instructor
    user_data = {
        "name": "Test Instructor",
        "email": "instructor@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    instructor_id = user_response.json()["id"]
    
    # Create course
    course_data = {
        "title": "Test Course",
        "description": "Test description",
        "category": "financial_education",
        "instructor_id": instructor_id,
        "points_reward": 50
    }
    client.post("/api/v1/courses/", json=course_data)
    
    # Get courses
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Course"

def test_enroll_in_course(client: TestClient):
    # Create instructor and student
    instructor_data = {
        "name": "Test Instructor",
        "email": "instructor@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }
    instructor_response = client.post("/api/v1/users/", json=instructor_data)
    instructor_id = instructor_response.json()["id"]
    
    student_data = {
        "name": "Test Student",
        "email": "student@example.com",
        "phone": "11888888888",
        "user_type": "young"
    }
    student_response = client.post("/api/v1/users/", json=student_data)
    student_id = student_response.json()["id"]
    
    # Create course
    course_data = {
        "title": "Test Course",
        "description": "Test description",
        "category": "financial_education",
        "instructor_id": instructor_id,
        "points_reward": 50
    }
    course_response = client.post("/api/v1/courses/", json=course_data)
    course_id = course_response.json()["id"]
    
    # Enroll student
    response = client.post(f"/api/v1/courses/{course_id}/enroll?user_id={student_id}")
    assert response.status_code == 201
    data = response.json()
    assert data["course_id"] == course_id
    assert data["user_id"] == student_id
    assert data["is_completed"] is False

def test_complete_course(client: TestClient):
    # Create instructor and student
    instructor_data = {
        "name": "Test Instructor",
        "email": "instructor@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }
    instructor_response = client.post("/api/v1/users/", json=instructor_data)
    instructor_id = instructor_response.json()["id"]
    
    student_data = {
        "name": "Test Student",
        "email": "student@example.com",
        "phone": "11888888888",
        "user_type": "young"
    }
    student_response = client.post("/api/v1/users/", json=student_data)
    student_id = student_response.json()["id"]
    
    # Create course
    course_data = {
        "title": "Test Course",
        "description": "Test description",
        "category": "financial_education",
        "instructor_id": instructor_id,
        "points_reward": 50
    }
    course_response = client.post("/api/v1/courses/", json=course_data)
    course_id = course_response.json()["id"]
    
    # Enroll and complete
    enrollment_response = client.post(f"/api/v1/courses/{course_id}/enroll?user_id={student_id}")
    enrollment_id = enrollment_response.json()["id"]
    
    response = client.put(f"/api/v1/courses/enrollments/{enrollment_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] is True
    assert data["completed_at"] is not None

def test_course_gamification_points(client: TestClient):
    # Create instructor and student
    instructor_data = {
        "name": "Test Instructor",
        "email": "instructor@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }
    instructor_response = client.post("/api/v1/users/", json=instructor_data)
    instructor_id = instructor_response.json()["id"]
    
    student_data = {
        "name": "Test Student",
        "email": "student@example.com",
        "phone": "11888888888",
        "user_type": "young"
    }
    student_response = client.post("/api/v1/users/", json=student_data)
    student_id = student_response.json()["id"]
    
    # Create course
    course_data = {
        "title": "Test Course",
        "description": "Test description",
        "category": "financial_education",
        "instructor_id": instructor_id,
        "points_reward": 50
    }
    course_response = client.post("/api/v1/courses/", json=course_data)
    course_id = course_response.json()["id"]
    
    # Check initial stats
    stats_response = client.get(f"/api/v1/gamification/users/{student_id}/stats")
    initial_stats = stats_response.json()
    assert initial_stats["total_points"] == 0
    
    # Enroll (10 points)
    enrollment_response = client.post(f"/api/v1/courses/{course_id}/enroll?user_id={student_id}")
    enrollment_id = enrollment_response.json()["id"]
    
    stats_response = client.get(f"/api/v1/gamification/users/{student_id}/stats")
    enrollment_stats = stats_response.json()
    assert enrollment_stats["total_points"] == 10
    
    # Complete (50 points)
    client.put(f"/api/v1/courses/enrollments/{enrollment_id}/complete")
    
    stats_response = client.get(f"/api/v1/gamification/users/{student_id}/stats")
    final_stats = stats_response.json()
    assert final_stats["total_points"] == 60  # 10 + 50
