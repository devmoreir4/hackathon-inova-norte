from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.application.dto import PostCreate, PostResponse, PostUpdate, CommentCreate, CommentResponse, CommentUpdate
from app.domain.models import Post, Comment, PostStatus
from app.infrastructure.database import get_db
from app.application.services.gamification_service import GamificationService

router = APIRouter()

@router.get(
    "/posts", 
    response_model=List[PostResponse],
    summary="List posts",
    description="Returns list of forum posts with pagination"
)
def list_posts(
    skip: int = 0, 
    limit: int = 100, 
    category: str = None,
    status: PostStatus = PostStatus.PUBLISHED,
    db: Session = Depends(get_db)
):
    query = db.query(Post).filter(Post.status == status)
    
    if category:
        query = query.filter(Post.category == category)
    
    posts = query.offset(skip).limit(limit).all()
    return posts

@router.get(
    "/posts/{post_id}", 
    response_model=PostResponse,
    summary="Get post by ID",
    description="Returns data of a specific post"
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    post.views_count += 1
    db.commit()
    db.refresh(post)
    
    return post

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put(
    "/posts/{post_id}", 
    response_model=PostResponse,
    summary="Update post",
    description="Updates data of an existing post"
)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    update_data = post_update.model_dump(exclude_unset=True)
    
    # If status is being changed to published, set published_at
    if 'status' in update_data and update_data['status'] == PostStatus.PUBLISHED and post.status != PostStatus.PUBLISHED:
        update_data['published_at'] = datetime.now()
    
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    return post

@router.delete(
    "/posts/{post_id}",
    summary="Delete post",
    description="Deletes a post"
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@router.post(
    "/posts/{post_id}/comments", 
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create comment",
    description="Create a new comment on a post"
)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    comment_data = comment.model_dump()
    comment_data['post_id'] = post_id
    db_comment = Comment(**comment_data)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    gamification_service = GamificationService(db)
    gamification_service.add_points(
        user_id=comment.author_id,
        source="forum_comment",
        source_id=db_comment.id,
        description=f"Comentou no post ID: {post_id}"
    )
    
    return db_comment

@router.get(
    "/posts/{post_id}/comments", 
    response_model=List[CommentResponse],
    summary="List comments",
    description="Returns list of comments for a post"
)
def list_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.put(
    "/comments/{comment_id}", 
    response_model=CommentResponse,
    summary="Update comment",
    description="Updates a comment"
)
def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Comment not found"
        )
    
    update_data = comment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    return comment

@router.delete(
    "/comments/{comment_id}",
    summary="Delete comment",
    description="Deletes a comment"
)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Comment not found"
        )
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
