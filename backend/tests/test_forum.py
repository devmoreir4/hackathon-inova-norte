import pytest
from fastapi.testclient import TestClient

def test_create_post(client: TestClient, sample_user_data, sample_post_data):
    # Create user first
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Update post data with user ID
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    # Create post
    response = client.post("/api/v1/forum/posts", json=post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert data["category"] == post_data["category"]
    assert data["author_id"] == user_id
    assert "id" in data
    assert "created_at" in data

def test_get_post_by_id(client: TestClient, sample_user_data, sample_post_data):
    # Create user and post
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    create_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = create_response.json()["id"]
    
    # Get post by ID
    response = client.get(f"/api/v1/forum/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["views_count"] == 1  # Should increment views

def test_get_post_not_found(client: TestClient):
    response = client.get("/api/v1/forum/posts/99999")
    assert response.status_code == 404
    assert "Post not found" in response.json()["detail"]

def test_list_posts(client: TestClient, sample_user_data, sample_post_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create multiple posts
    for i in range(3):
        post_data = sample_post_data.copy()
        post_data["title"] = f"Post {i}"
        post_data["author_id"] = user_id
        create_response = client.post("/api/v1/forum/posts", json=post_data)
        post_id = create_response.json()["id"]
        
        # Publish the post
        client.put(f"/api/v1/forum/posts/{post_id}", json={"status": "published"})
    
    # List posts
    response = client.get("/api/v1/forum/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_post(client: TestClient, sample_user_data, sample_post_data):
    # Create user and post
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    create_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = create_response.json()["id"]
    
    # Update post
    update_data = {
        "title": "Updated Post Title",
        "content": "Updated content",
        "status": "published"
    }
    response = client.put(f"/api/v1/forum/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Post Title"
    assert data["content"] == "Updated content"
    assert data["status"] == "published"

def test_delete_post(client: TestClient, sample_user_data, sample_post_data):
    # Create user and post
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    create_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = create_response.json()["id"]
    
    # Delete post
    response = client.delete(f"/api/v1/forum/posts/{post_id}")
    assert response.status_code == 200
    assert "Post deleted successfully" in response.json()["message"]
    
    # Try to get deleted post
    get_response = client.get(f"/api/v1/forum/posts/{post_id}")
    assert get_response.status_code == 404

def test_create_comment(client: TestClient, sample_user_data, sample_post_data, sample_comment_data):
    # Create user and post
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    post_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = post_response.json()["id"]
    
    # Create comment
    comment_data = sample_comment_data.copy()
    comment_data["post_id"] = post_id
    comment_data["author_id"] = user_id
    
    response = client.post(f"/api/v1/forum/posts/{post_id}/comments", json=comment_data)
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == comment_data["content"]
    assert data["post_id"] == post_id
    assert data["author_id"] == user_id
    assert "id" in data
    assert "created_at" in data

def test_list_comments(client: TestClient, sample_user_data, sample_post_data, sample_comment_data):
    # Create user and post
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    post_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = post_response.json()["id"]
    
    # Create multiple comments
    for i in range(3):
        comment_data = sample_comment_data.copy()
        comment_data["content"] = f"Comment {i}"
        comment_data["post_id"] = post_id
        comment_data["author_id"] = user_id
        client.post(f"/api/v1/forum/posts/{post_id}/comments", json=comment_data)
    
    # List comments
    response = client.get(f"/api/v1/forum/posts/{post_id}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_comment(client: TestClient, sample_user_data, sample_post_data, sample_comment_data):
    # Create user, post and comment
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    post_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = post_response.json()["id"]
    
    comment_data = sample_comment_data.copy()
    comment_data["post_id"] = post_id
    comment_data["author_id"] = user_id
    
    comment_response = client.post(f"/api/v1/forum/posts/{post_id}/comments", json=comment_data)
    comment_id = comment_response.json()["id"]
    
    # Update comment
    update_data = {"content": "Updated comment content"}
    response = client.put(f"/api/v1/forum/comments/{comment_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated comment content"

def test_delete_comment(client: TestClient, sample_user_data, sample_post_data, sample_comment_data):
    # Create user, post and comment
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    post_data = sample_post_data.copy()
    post_data["author_id"] = user_id
    
    post_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = post_response.json()["id"]
    
    comment_data = sample_comment_data.copy()
    comment_data["post_id"] = post_id
    comment_data["author_id"] = user_id
    
    comment_response = client.post(f"/api/v1/forum/posts/{post_id}/comments", json=comment_data)
    comment_id = comment_response.json()["id"]
    
    # Delete comment
    response = client.delete(f"/api/v1/forum/comments/{comment_id}")
    assert response.status_code == 200
    assert "Comment deleted successfully" in response.json()["message"]
    
    # Try to get deleted comment
    get_response = client.get(f"/api/v1/forum/posts/{post_id}/comments")
    assert get_response.status_code == 200
    data = get_response.json()
    assert len(data) == 0
