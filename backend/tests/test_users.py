import pytest
from fastapi.testclient import TestClient

def test_create_user(client: TestClient, sample_user_data):
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_user_data["name"]
    assert data["email"] == sample_user_data["email"]
    assert data["phone"] == sample_user_data["phone"]
    assert data["user_type"] == sample_user_data["user_type"]
    assert "id" in data
    assert "created_at" in data
    assert data["active"] is True

def test_create_user_duplicate_email(client: TestClient, sample_user_data):
    # Create first user
    response1 = client.post("/api/v1/users/", json=sample_user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same email
    response2 = client.post("/api/v1/users/", json=sample_user_data)
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]

def test_get_user_by_id(client: TestClient, sample_user_data):
    # Create user
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    # Get user by ID
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == sample_user_data["name"]

def test_get_user_by_email(client: TestClient, sample_user_data):
    # Create user
    client.post("/api/v1/users/", json=sample_user_data)
    
    # Get user by email
    response = client.get(f"/api/v1/users/email/{sample_user_data['email']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]

def test_get_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert "Member not found" in response.json()["detail"]

def test_list_users(client: TestClient, sample_user_data):
    # Create multiple users
    for i in range(3):
        user_data = sample_user_data.copy()
        user_data["email"] = f"user{i}@example.com"
        user_data["name"] = f"User {i}"
        client.post("/api/v1/users/", json=user_data)
    
    # List users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_user(client: TestClient, sample_user_data):
    # Create user
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    # Update user
    update_data = {
        "name": "Updated Name",
        "phone": "11888888888"
    }
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["phone"] == "11888888888"

def test_deactivate_user(client: TestClient, sample_user_data):
    # Create user
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    # Deactivate user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert "Member deactivated successfully" in response.json()["message"]
    
    # Try to get deactivated user
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
