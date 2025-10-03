from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.infrastructure.database import get_db
from app.domain.models import Community, CommunityMembership, User, MembershipRole, CommunityType
from app.application.dto import (
    CommunityCreate, CommunityUpdate, CommunityResponse,
    CommunityMembershipCreate, CommunityMembershipUpdate, CommunityMembershipResponse
)
from app.application.services.gamification_service import GamificationService

community_router = APIRouter(prefix="/communities", tags=["Communities"])

@community_router.post(
    "/",
    response_model=CommunityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create community",
    description="Create a new community"
)
def create_community(community: CommunityCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == community.owner_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_community = Community(**community.model_dump())
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    
    # Add owner as member with OWNER role
    membership = CommunityMembership(
        community_id=db_community.id,
        user_id=community.owner_id,
        role=MembershipRole.OWNER
    )
    db.add(membership)
    
    # Update member count
    db_community.member_count = 1
    db.commit()
    db.refresh(db_community)
    
    gamification_service = GamificationService(db)
    gamification_service.add_points(
        user_id=community.owner_id,
        source="community_create",
        source_id=db_community.id,
        description=f"Criou comunidade: {db_community.name}"
    )
    
    return db_community

@community_router.get(
    "/",
    response_model=List[CommunityResponse],
    summary="List communities",
    description="Get list of communities with optional filters"
)
def list_communities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    community_type: Optional[CommunityType] = None,
    active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(Community).filter(Community.active == active)
    
    if community_type:
        query = query.filter(Community.community_type == community_type)
    
    communities = query.offset(skip).limit(limit).all()
    return communities

@community_router.get(
    "/{community_id}",
    response_model=CommunityResponse,
    summary="Get community by ID",
    description="Get community details by ID"
)
def get_community(community_id: int, db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    return community

@community_router.put(
    "/{community_id}",
    response_model=CommunityResponse,
    summary="Update community",
    description="Update community information"
)
def update_community(
    community_id: int, 
    community_update: CommunityUpdate, 
    user_id: int = Query(..., description="User ID making the request"),
    db: Session = Depends(get_db)
):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    
    # Check if user has permission (owner or admin)
    membership = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.user_id == user_id,
        CommunityMembership.role.in_([MembershipRole.OWNER, MembershipRole.ADMIN])
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this community"
        )
    
    update_data = community_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(community, field, value)
    
    db.commit()
    db.refresh(community)
    return community

@community_router.delete(
    "/{community_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete community",
    description="Delete a community (only owner can delete)"
)
def delete_community(
    community_id: int,
    user_id: int = Query(..., description="User ID making the request"),
    db: Session = Depends(get_db)
):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    
    # Only owner can delete
    if community.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only community owner can delete the community"
        )
    
    # Soft delete
    community.active = False
    db.commit()

# Membership endpoints
@community_router.post(
    "/{community_id}/join",
    response_model=CommunityMembershipResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join community",
    description="Join a community"
)
def join_community(
    community_id: int,
    user_id: int = Query(..., description="User ID joining the community"),
    db: Session = Depends(get_db)
):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    
    if not community.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Community is not active"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already a member
    existing_membership = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.user_id == user_id,
        CommunityMembership.active == True
    ).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this community"
        )
    
    # Check capacity
    if community.max_members:
        current_members = db.query(CommunityMembership).filter(
            CommunityMembership.community_id == community_id,
            CommunityMembership.active == True
        ).count()
        
        if current_members >= community.max_members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Community is at full capacity"
            )
    
    # Check community type permissions
    if community.community_type == CommunityType.PRIVATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is a private community. Invitation required."
        )
    
    # Create membership
    membership = CommunityMembership(
        community_id=community_id,
        user_id=user_id,
        role=MembershipRole.MEMBER
    )
    db.add(membership)
    
    # Update member count
    community.member_count = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.active == True
    ).count() + 1
    
    db.commit()
    db.refresh(membership)
    
    gamification_service = GamificationService(db)
    gamification_service.add_points(
        user_id=user_id,
        source="community_join",
        source_id=community_id,
        description=f"Entrou na comunidade: {community.name}"
    )
    
    return membership

@community_router.get(
    "/{community_id}/members",
    response_model=List[CommunityMembershipResponse],
    summary="List community members",
    description="Get list of community members"
)
def list_community_members(
    community_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[MembershipRole] = None,
    db: Session = Depends(get_db)
):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    
    query = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.active == True
    )
    
    if role:
        query = query.filter(CommunityMembership.role == role)
    
    members = query.offset(skip).limit(limit).all()
    return members

@community_router.put(
    "/{community_id}/members/{membership_id}",
    response_model=CommunityMembershipResponse,
    summary="Update member role",
    description="Update a member's role in the community"
)
def update_member_role(
    community_id: int,
    membership_id: int,
    membership_update: CommunityMembershipUpdate,
    user_id: int = Query(..., description="User ID making the request"),
    db: Session = Depends(get_db)
):
    # Check if requester has permission
    requester_membership = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.user_id == user_id,
        CommunityMembership.role.in_([MembershipRole.OWNER, MembershipRole.ADMIN])
    ).first()
    
    if not requester_membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update member roles"
        )
    
    membership = db.query(CommunityMembership).filter(
        CommunityMembership.id == membership_id,
        CommunityMembership.community_id == community_id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Prevent changing owner role
    if membership.role == MembershipRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change owner role"
        )
    
    update_data = membership_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(membership, field, value)
    
    db.commit()
    db.refresh(membership)
    return membership

@community_router.delete(
    "/{community_id}/members/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove member",
    description="Remove a member from the community"
)
def remove_member(
    community_id: int,
    membership_id: int,
    user_id: int = Query(..., description="User ID making the request"),
    db: Session = Depends(get_db)
):
    membership = db.query(CommunityMembership).filter(
        CommunityMembership.id == membership_id,
        CommunityMembership.community_id == community_id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Check permissions (owner, admin, or the member themselves)
    if membership.user_id != user_id:
        requester_membership = db.query(CommunityMembership).filter(
            CommunityMembership.community_id == community_id,
            CommunityMembership.user_id == user_id,
            CommunityMembership.role.in_([MembershipRole.OWNER, MembershipRole.ADMIN])
        ).first()
        
        if not requester_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to remove this member"
            )
    
    # Cannot remove owner
    if membership.role == MembershipRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove community owner"
        )
    
    # Soft delete membership
    membership.active = False
    
    # Update member count
    community = db.query(Community).filter(Community.id == community_id).first()
    community.member_count = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.active == True
    ).count() - 1
    
    db.commit()

@community_router.get(
    "/user/{user_id}",
    response_model=List[CommunityMembershipResponse],
    summary="Get user's communities",
    description="Get communities that a user is a member of"
)
def get_user_communities(
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
    
    memberships = db.query(CommunityMembership).filter(
        CommunityMembership.user_id == user_id,
        CommunityMembership.active == True
    ).offset(skip).limit(limit).all()
    
    return memberships
