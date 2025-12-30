from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from database import Base

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150))
    role = Column(String(20), nullable=False)  # admin, doctor, nurse, receptionist
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)


class AuditLog(Base):
    """Audit log for tracking all sensitive operations"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # NULL for system actions
    username = Column(String(50))
    action = Column(String(50), nullable=False)  # CREATE, READ, UPDATE, DELETE
    resource = Column(String(50), nullable=False)  # patients, doctors, appointments, etc.
    resource_id = Column(Integer)
    details = Column(Text)  # JSON string with additional details
    ip_address = Column(String(45))  # IPv6 compatible
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(20))  # success, failed
