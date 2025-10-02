import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_community(client: TestClient, sample_user_data):
    # Create user first (as owner)
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    community_data = {
        "name": "Test Community",
        "description": "This is a test community",
        "community_type": "public",
        "max_members": 100,
        "owner_id": user_id
    }
    
    response = client.post("/api/v1/communities/", json=community_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == community_data["name"]
    assert data["owner_id"] == user_id
    assert data["member_count"] == 1
    assert data["active"] == True

def test_get_community_by_id(client: TestClient, sample_user_data):
    # Create user and community
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    community_data = {
        "name": "Test Community",
        "description": "This is a test community",
        "community_type": "public",
        "owner_id": user_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Get community by ID
    response = client.get(f"/api/v1/communities/{community_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == community_id
    assert data["name"] == community_data["name"]

def test_get_community_not_found(client: TestClient):
    response = client.get("/api/v1/communities/99999")
    assert response.status_code == 404
    assert "Community not found" in response.json()["detail"]

def test_list_communities(client: TestClient, sample_user_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create multiple communities
    for i in range(3):
        community_data = {
            "name": f"Community {i}",
            "description": f"Description for community {i}",
            "community_type": "public",
            "owner_id": user_id
        }
        client.post("/api/v1/communities/", json=community_data)
    
    # List communities
    response = client.get("/api/v1/communities/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_community(client: TestClient, sample_user_data):
    # Create user and community
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    community_data = {
        "name": "Original Community",
        "description": "Original description",
        "community_type": "public",
        "owner_id": user_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Update community
    update_data = {
        "name": "Updated Community",
        "description": "Updated description",
        "community_type": "private"
    }
    
    response = client.put(f"/api/v1/communities/{community_id}?user_id={user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Community"
    assert data["description"] == "Updated description"
    assert data["community_type"] == "private"

def test_update_community_unauthorized(client: TestClient, sample_user_data):
    # Create users
    user1_response = client.post("/api/v1/users/", json=sample_user_data)
    user1_id = user1_response.json()["id"]
    
    user2_data = sample_user_data.copy()
    user2_data["email"] = "user2@example.com"
    user2_response = client.post("/api/v1/users/", json=user2_data)
    user2_id = user2_response.json()["id"]
    
    # Create community with user1
    community_data = {
        "name": "Test Community",
        "description": "Test description",
        "community_type": "public",
        "owner_id": user1_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Try to update with user2 (should fail)
    update_data = {"name": "Hacked Community"}
    response = client.put(f"/api/v1/communities/{community_id}?user_id={user2_id}", json=update_data)
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]

def test_delete_community(client: TestClient, sample_user_data):
    # Create user and community
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    community_data = {
        "name": "Community to Delete",
        "description": "This community will be deleted",
        "community_type": "public",
        "owner_id": user_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Delete community
    response = client.delete(f"/api/v1/communities/{community_id}?user_id={user_id}")
    assert response.status_code == 204
    
    # Verify community is soft deleted (inactive)
    get_response = client.get(f"/api/v1/communities/{community_id}")
    assert get_response.json()["active"] == False

def test_join_community(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Create community
    community_data = {
        "name": "Join Test Community",
        "description": "Community for testing join functionality",
        "community_type": "public",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Join community
    response = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    assert response.status_code == 201
    data = response.json()
    assert data["community_id"] == community_id
    assert data["user_id"] == member_id
    assert data["role"] == "member"
    assert data["active"] == True

def test_join_community_duplicate(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Create community
    community_data = {
        "name": "Duplicate Join Test",
        "description": "Community for testing duplicate join",
        "community_type": "public",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # First join
    response1 = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    assert response1.status_code == 201
    
    # Duplicate join
    response2 = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    assert response2.status_code == 400
    assert "already a member" in response2.json()["detail"]

def test_join_private_community(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Create private community
    community_data = {
        "name": "Private Community",
        "description": "This is a private community",
        "community_type": "private",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Try to join private community
    response = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    assert response.status_code == 403
    assert "private community" in response.json()["detail"]

def test_list_community_members(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    # Create additional members
    member_ids = []
    for i in range(2):
        member_data = sample_user_data.copy()
        member_data["email"] = f"member{i}@example.com"
        member_response = client.post("/api/v1/users/", json=member_data)
        member_ids.append(member_response.json()["id"])
    
    # Create community
    community_data = {
        "name": "Members Test Community",
        "description": "Community for testing member listing",
        "community_type": "public",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Add members
    for member_id in member_ids:
        client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    
    # List members
    response = client.get(f"/api/v1/communities/{community_id}/members")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # Owner + 2 members

def test_update_member_role(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Create community
    community_data = {
        "name": "Role Update Test",
        "description": "Community for testing role updates",
        "community_type": "public",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Join community
    join_response = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    membership_id = join_response.json()["id"]
    
    # Update role to admin
    update_data = {"role": "admin"}
    response = client.put(
        f"/api/v1/communities/{community_id}/members/{membership_id}?user_id={owner_id}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "admin"

def test_remove_member(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Create community
    community_data = {
        "name": "Remove Member Test",
        "description": "Community for testing member removal",
        "community_type": "public",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Join community
    join_response = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    membership_id = join_response.json()["id"]
    
    # Remove member
    response = client.delete(
        f"/api/v1/communities/{community_id}/members/{membership_id}?user_id={owner_id}"
    )
    assert response.status_code == 204
    
    # Verify member count decreased
    community_response = client.get(f"/api/v1/communities/{community_id}")
    assert community_response.json()["member_count"] == 1  # Only owner left

def test_leave_community(client: TestClient, sample_user_data):
    # Create users
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Create community
    community_data = {
        "name": "Leave Community Test",
        "description": "Community for testing self-removal",
        "community_type": "public",
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Join community
    join_response = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    membership_id = join_response.json()["id"]
    
    # Leave community (member removes themselves)
    response = client.delete(
        f"/api/v1/communities/{community_id}/members/{membership_id}?user_id={member_id}"
    )
    assert response.status_code == 204

def test_get_user_communities(client: TestClient, sample_user_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create communities where user is owner
    for i in range(2):
        community_data = {
            "name": f"User Community {i}",
            "description": f"Community owned by user - {i}",
            "community_type": "public",
            "owner_id": user_id
        }
        client.post("/api/v1/communities/", json=community_data)
    
    # Create another community and join it
    other_user_data = sample_user_data.copy()
    other_user_data["email"] = "other@example.com"
    other_user_response = client.post("/api/v1/users/", json=other_user_data)
    other_user_id = other_user_response.json()["id"]
    
    community_data = {
        "name": "Other Community",
        "description": "Community owned by other user",
        "community_type": "public",
        "owner_id": other_user_id
    }
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Join the other community
    client.post(f"/api/v1/communities/{community_id}/join?user_id={user_id}")
    
    # Get user's communities
    response = client.get(f"/api/v1/communities/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # 2 owned + 1 joined

def test_get_user_communities_not_found(client: TestClient):
    response = client.get("/api/v1/communities/user/99999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_community_capacity_limit(client: TestClient, sample_user_data):
    # Create owner
    owner_response = client.post("/api/v1/users/", json=sample_user_data)
    owner_id = owner_response.json()["id"]
    
    # Create community with max 2 members
    community_data = {
        "name": "Capacity Test Community",
        "description": "Community for testing capacity limits",
        "community_type": "public",
        "max_members": 2,
        "owner_id": owner_id
    }
    
    create_response = client.post("/api/v1/communities/", json=community_data)
    community_id = create_response.json()["id"]
    
    # Create member
    member_data = sample_user_data.copy()
    member_data["email"] = "member@example.com"
    member_response = client.post("/api/v1/users/", json=member_data)
    member_id = member_response.json()["id"]
    
    # Join community (should work - 2 total)
    response1 = client.post(f"/api/v1/communities/{community_id}/join?user_id={member_id}")
    assert response1.status_code == 201
    
    # Create another member
    member2_data = sample_user_data.copy()
    member2_data["email"] = "member2@example.com"
    member2_response = client.post("/api/v1/users/", json=member2_data)
    member2_id = member2_response.json()["id"]
    
    # Try to join when at capacity (should fail)
    response2 = client.post(f"/api/v1/communities/{community_id}/join?user_id={member2_id}")
    assert response2.status_code == 400
    assert "full capacity" in response2.json()["detail"]
