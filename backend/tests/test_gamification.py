import pytest
from fastapi.testclient import TestClient

def test_gamification_basic_flow(client: TestClient):
    # Create a user
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "11999999999",
        "user_type": "general"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create a course
    course_data = {
        "title": "Gamification Test Course",
        "description": "A course to test gamification",
        "category": "financial_education",
        "instructor_id": user_id,  # User is also the instructor
        "points_reward": 50
    }
    course_response = client.post("/api/v1/courses/", json=course_data)
    course_id = course_response.json()["id"]
    
    # 1. Check initial stats (should be level 1, 0 points)
    stats_response = client.get(f"/api/v1/gamification/users/{user_id}/stats")
    assert stats_response.status_code == 200
    initial_stats = stats_response.json()
    assert initial_stats["level"] == 1
    assert initial_stats["total_points"] == 0
    assert initial_stats["badges_count"] == 0
    
    # 2. Enroll in course (should get 10 points)
    enrollment_response = client.post(f"/api/v1/courses/{course_id}/enroll?user_id={user_id}")
    assert enrollment_response.status_code == 201
    enrollment_id = enrollment_response.json()["id"]
    
    # Check stats after enrollment
    stats_response = client.get(f"/api/v1/gamification/users/{user_id}/stats")
    enrollment_stats = stats_response.json()
    assert enrollment_stats["total_points"] == 10
    
    # 3. Complete course (should get 50 points)
    complete_response = client.put(f"/api/v1/courses/enrollments/{enrollment_id}/complete")
    assert complete_response.status_code == 200
    
    # Check final stats
    stats_response = client.get(f"/api/v1/gamification/users/{user_id}/stats")
    final_stats = stats_response.json()
    assert final_stats["total_points"] == 60  # 10 + 50
    assert final_stats["level"] == 1  # Still level 1 (need 100 points for level 2)
    
    # 4. Check points history
    points_response = client.get(f"/api/v1/gamification/users/{user_id}/points")
    assert points_response.status_code == 200
    points_data = points_response.json()
    assert len(points_data) == 2
    
    # Verify the points are correct
    enrollment_point = next(p for p in points_data if p["source"] == "course_enrollment")
    completion_point = next(p for p in points_data if p["source"] == "course_completion")
    
    assert enrollment_point["points"] == 10
    assert completion_point["points"] == 50
    assert "Inscrito no curso" in enrollment_point["description"]
    assert "Concluiu curso" in completion_point["description"]

def test_gamification_level_up(client: TestClient):
    # Create a user
    user_data = {
        "name": "Level Up User",
        "email": "levelup@example.com",
        "phone": "11888888888",
        "user_type": "young"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create multiple courses to get enough points for level up
    courses_data = [
        {
            "title": "Course 1",
            "description": "First course",
            "category": "financial_education",
            "instructor_id": user_id,
            "points_reward": 50
        },
        {
            "title": "Course 2", 
            "description": "Second course",
            "category": "cooperativism",
            "instructor_id": user_id,
            "points_reward": 60
        }
    ]
    
    course_ids = []
    for course_data in courses_data:
        course_response = client.post("/api/v1/courses/", json=course_data)
        course_ids.append(course_response.json()["id"])
    
    # Enroll and complete both courses
    total_points = 0
    for course_id in course_ids:
        # Enroll (10 points)
        enrollment_response = client.post(f"/api/v1/courses/{course_id}/enroll?user_id={user_id}")
        enrollment_id = enrollment_response.json()["id"]
        total_points += 10
        
        # Complete (50 points for both courses)
        complete_response = client.put(f"/api/v1/courses/enrollments/{enrollment_id}/complete")
        assert complete_response.status_code == 200
        total_points += 50  # Fixed 50 points for completion
    
    # Check final stats (should be level 2 with 120+ points)
    stats_response = client.get(f"/api/v1/gamification/users/{user_id}/stats")
    final_stats = stats_response.json()
    assert final_stats["total_points"] == total_points
    assert final_stats["level"] >= 2  # Should have leveled up

def test_gamification_leaderboard(client: TestClient):
    # Create multiple users
    users_data = [
        {
            "name": "User 1",
            "email": "user1@example.com",
            "phone": "11111111111",
            "user_type": "general"
        },
        {
            "name": "User 2", 
            "email": "user2@example.com",
            "phone": "22222222222",
            "user_type": "entrepreneur"
        }
    ]
    
    user_ids = []
    for user_data in users_data:
        user_response = client.post("/api/v1/users/", json=user_data)
        user_ids.append(user_response.json()["id"])
    
    # Create courses
    course_data = {
        "title": "Leaderboard Test Course",
        "description": "Course for leaderboard test",
        "category": "financial_education",
        "instructor_id": user_ids[0],
        "points_reward": 50
    }
    course_response = client.post("/api/v1/courses/", json=course_data)
    course_id = course_response.json()["id"]
    
    # User 1 enrolls and completes course (60 points total)
    enrollment_response = client.post(f"/api/v1/courses/{course_id}/enroll?user_id={user_ids[0]}")
    enrollment_id = enrollment_response.json()["id"]
    client.put(f"/api/v1/courses/enrollments/{enrollment_id}/complete")
    
    # User 2 enrolls but doesn't complete (10 points total)
    client.post(f"/api/v1/courses/{course_id}/enroll?user_id={user_ids[1]}")
    
    # Check leaderboard
    leaderboard_response = client.get("/api/v1/gamification/leaderboard")
    assert leaderboard_response.status_code == 200
    leaderboard = leaderboard_response.json()
    
    # Should have at least 2 users
    assert len(leaderboard) >= 2
    
    # User 1 should be ranked higher than User 2
    user1_rank = next(u["rank"] for u in leaderboard if u["user_id"] == user_ids[0])
    user2_rank = next(u["rank"] for u in leaderboard if u["user_id"] == user_ids[1])
    assert user1_rank < user2_rank  # Lower rank number = higher position
    
    # Verify points
    user1_entry = next(u for u in leaderboard if u["user_id"] == user_ids[0])
    user2_entry = next(u for u in leaderboard if u["user_id"] == user_ids[1])
    assert user1_entry["total_points"] == 60
    assert user2_entry["total_points"] == 10
