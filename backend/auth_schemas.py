from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# Authentication Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['admin', 'doctor', 'nurse', 'receptionist']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Audit Log Schemas
class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    username: Optional[str]
    action: str
    resource: str
    resource_id: Optional[int]
    details: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime
    status: Optional[str]

    class Config:
        from_attributes = True
