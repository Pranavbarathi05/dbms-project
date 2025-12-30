from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import auth_schemas
import models
from auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_active_user,
    check_role_permission,
    get_db
)
import json

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=auth_schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: auth_schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Register a new user (Admin only)"""
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Log the action
    log_audit(db, current_user.id, current_user.username, "CREATE", "users", db_user.id, 
              f"Created new user: {user.username} with role {user.role}", None, "success")
    
    return db_user

@router.post("/login", response_model=auth_schemas.Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Log failed login attempt
        log_audit(db, None, form_data.username, "LOGIN", "auth", None, 
                 "Failed login attempt", request.client.host if request.client else None, "failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=480)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    
    # Log successful login
    log_audit(db, user.id, user.username, "LOGIN", "auth", user.id, 
             "Successful login", request.client.host if request.client else None, "success")
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=auth_schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@router.get("/users", response_model=List[auth_schemas.UserOut])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """List all users (Admin only)"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    
    # Log the action
    log_audit(db, current_user.id, current_user.username, "READ", "users", None, 
             f"Listed {len(users)} users", None, "success")
    
    return users

@router.put("/users/{user_id}", response_model=auth_schemas.UserOut)
async def update_user(
    user_id: int,
    user_update: auth_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Update user (Admin only)"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    # Log the action
    log_audit(db, current_user.id, current_user.username, "UPDATE", "users", user_id, 
             f"Updated user: {db_user.username}", None, "success")
    
    return db_user

@router.get("/audit-logs", response_model=List[auth_schemas.AuditLogOut])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Get audit logs (Admin only)"""
    logs = db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

def log_audit(db: Session, user_id: int, username: str, action: str, resource: str, 
              resource_id: int, details: str, ip_address: str, status: str):
    """Helper function to log audit entries"""
    audit_log = models.AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        resource=resource,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        status=status
    )
    db.add(audit_log)
    db.commit()
