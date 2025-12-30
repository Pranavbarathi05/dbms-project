from sqlalchemy.orm import Session
from datetime import datetime
import models
import json

def log_audit(
    db: Session, 
    user_id: int, 
    username: str, 
    action: str, 
    resource: str, 
    resource_id: int, 
    details: str, 
    ip_address: str = None, 
    status: str = "success"
):
    """Helper function to log audit entries"""
    try:
        audit_log = models.AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            status=status,
            timestamp=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
    except Exception as e:
        print(f"Error logging audit: {str(e)}")
        db.rollback()

def get_client_ip(request):
    """Extract client IP from request"""
    if not request:
        return None
    if request.client:
        return request.client.host
    return None
