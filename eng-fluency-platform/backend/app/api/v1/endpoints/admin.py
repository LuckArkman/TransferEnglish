from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.auth import UserCreate, User as UserSchema
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def list_tenant_users(
    db: Session = Depends(deps.get_db_with_tenant),
    current_admin: User = Depends(deps.get_current_admin)
) -> Any:
    """
    List all users belonging to the current tenant.
    """
    return db.query(User).filter(User.tenant_id == current_admin.tenant_id).all()

@router.post("/users", response_model=UserSchema)
def create_tenant_user(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    current_admin: User = Depends(deps.get_current_admin),
    user_in: UserCreate
) -> Any:
    """
    Create a new user within the same tenant.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    db_obj = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        tenant_id=current_admin.tenant_id,
        role="student" # Default role
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/users/{user_id}/toggle-active", response_model=UserSchema)
def toggle_user_active(
    user_id: str,
    db: Session = Depends(deps.get_db_with_tenant),
    current_admin: User = Depends(deps.get_current_admin)
) -> Any:
    """
    Toggle user active status.
    """
    user = db.query(User).filter(User.id == user_id, User.tenant_id == current_admin.tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in your tenant")
    
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user
