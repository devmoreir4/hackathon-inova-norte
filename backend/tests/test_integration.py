import pytest
from fastapi.testclient import TestClient

def test_complete_forum_workflow(client: TestClient):
    
    # 1. Create user
    user_data = {
        "name": "Forum User",
        "email": "forum@test.com",
        "user_type": "entrepreneur"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]
    
    # 2. Create post
    post_data = {
        "title": "Integration Test Post",
        "content": "This is a test post for integration testing",
        "category": "general",
        "author_id": user_id
    }
    post_response = client.post("/api/v1/forum/posts", json=post_data)
    assert post_response.status_code == 201
    post_id = post_response.json()["id"]
    
    # 3. View post (should increment views)
    view_response = client.get(f"/api/v1/forum/posts/{post_id}")
    assert view_response.status_code == 200
    assert view_response.json()["views_count"] == 1
    
    # 4. Create comment
    comment_data = {
        "content": "Great post!",
        "post_id": post_id,
        "author_id": user_id
    }
    comment_response = client.post(f"/api/v1/forum/posts/{post_id}/comments", json=comment_data)
    assert comment_response.status_code == 201
    comment_id = comment_response.json()["id"]
    
    # 5. List comments
    comments_response = client.get(f"/api/v1/forum/posts/{post_id}/comments")
    assert comments_response.status_code == 200
    assert len(comments_response.json()) == 1
    
    # 6. Update comment
    update_comment_data = {"content": "Updated comment"}
    update_comment_response = client.put(f"/api/v1/forum/comments/{comment_id}", json=update_comment_data)
    assert update_comment_response.status_code == 200
    
    # 7. Update post status to published
    update_post_data = {"status": "published"}
    update_post_response = client.put(f"/api/v1/forum/posts/{post_id}", json=update_post_data)
    assert update_post_response.status_code == 200
    assert update_post_response.json()["status"] == "published"
    
    # 8. List published posts
    list_posts_response = client.get("/api/v1/forum/posts?status=published")
    assert list_posts_response.status_code == 200
    assert len(list_posts_response.json()) == 1
    
    # 9. Delete comment
    delete_comment_response = client.delete(f"/api/v1/forum/comments/{comment_id}")
    assert delete_comment_response.status_code == 200
    
    # 10. Delete post
    delete_post_response = client.delete(f"/api/v1/forum/posts/{post_id}")
    assert delete_post_response.status_code == 200
    
    # 11. Delete user
    delete_user_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_user_response.status_code == 200

def test_multiple_users_forum_interaction(client: TestClient):
    
    # Create two users
    user1_data = {"name": "User 1", "email": "user1@test.com", "user_type": "general"}
    user2_data = {"name": "User 2", "email": "user2@test.com", "user_type": "entrepreneur"}
    
    user1_response = client.post("/api/v1/users/", json=user1_data)
    user2_response = client.post("/api/v1/users/", json=user2_data)
    
    user1_id = user1_response.json()["id"]
    user2_id = user2_response.json()["id"]
    
    # User 1 creates a post
    post_data = {
        "title": "Discussion Post",
        "content": "What do you think about this topic?",
        "category": "discussion",
        "author_id": user1_id
    }
    post_response = client.post("/api/v1/forum/posts", json=post_data)
    post_id = post_response.json()["id"]
    
    # User 2 comments on the post
    comment_data = {
        "content": "I think this is interesting!",
        "post_id": post_id,
        "author_id": user2_id
    }
    comment_response = client.post(f"/api/v1/forum/posts/{post_id}/comments", json=comment_data)
    assert comment_response.status_code == 201
    
    # User 1 replies to the comment
    reply_data = {
        "content": "Thanks for your input!",
        "post_id": post_id,
        "author_id": user1_id,
        "parent_comment_id": comment_response.json()["id"]
    }
    reply_response = client.post(f"/api/v1/forum/posts/{post_id}/comments", json=reply_data)
    assert reply_response.status_code == 201
    
    # Verify all comments are present
    comments_response = client.get(f"/api/v1/forum/posts/{post_id}/comments")
    assert comments_response.status_code == 200
    assert len(comments_response.json()) == 2
    
    # Cleanup
    client.delete(f"/api/v1/forum/posts/{post_id}")
    client.delete(f"/api/v1/users/{user1_id}")
    client.delete(f"/api/v1/users/{user2_id}")

def test_pagination_and_filtering(client: TestClient):
    
    # Create user
    user_data = {"name": "Test User", "email": "test@example.com", "user_type": "general"}
    user_response = client.post("/api/v1/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create multiple posts with different categories
    categories = ["general", "discussion", "general", "announcement"]
    for i, category in enumerate(categories):
        post_data = {
            "title": f"Post {i}",
            "content": f"Content for post {i}",
            "category": category,
            "author_id": user_id
        }
        create_response = client.post("/api/v1/forum/posts", json=post_data)
        post_id = create_response.json()["id"]
        
        # Publish the post
        client.put(f"/api/v1/forum/posts/{post_id}", json={"status": "published"})
    
    # Test pagination
    response = client.get("/api/v1/forum/posts?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    response = client.get("/api/v1/forum/posts?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Test category filtering
    response = client.get("/api/v1/forum/posts?category=general")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Cleanup
    client.delete(f"/api/v1/users/{user_id}")
