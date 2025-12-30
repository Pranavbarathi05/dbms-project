from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from auth import get_current_active_user, check_role_permission
from audit_helper import log_audit, get_client_ip

router = APIRouter(prefix="/doctors", tags=["doctors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.DoctorOut)
def create_doctor(
    request: Request,
    payload: schemas.DoctorCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Create a new doctor (Admin only)"""
    doc = models.Doctor(**payload.dict())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    log_audit(db, current_user.id, current_user.username, "CREATE", "doctors", 
              doc.id, f"Created doctor: {doc.full_name}", get_client_ip(request))
    return doc

@router.get("/", response_model=List[schemas.DoctorOut])
def list_doctors(
    request: Request,
    skip: int = 0, 
    limit: int = Query(50, le=1000), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor"]))
):
    """List doctors (Admin, Doctor only)"""
    docs = db.query(models.Doctor).offset(skip).limit(limit).all()
    return docs

@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(
    request: Request,
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor"]))
):
    """Get doctor by ID (Admin, Doctor only)"""
    doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc

@router.put("/{doctor_id}", response_model=schemas.DoctorOut)
def update_doctor(
    request: Request,
    doctor_id: int, 
    payload: schemas.DoctorUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Update doctor (Admin only)"""
    doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(doc, k, v)
    db.commit()
    db.refresh(doc)
    
    log_audit(db, current_user.id, current_user.username, "UPDATE", "doctors", 
              doc.id, f"Updated doctor: {doc.full_name}", get_client_ip(request))
    return doc

@router.delete("/{doctor_id}")
def delete_doctor(
    request: Request,
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Delete doctor (Admin only)"""
    doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    log_audit(db, current_user.id, current_user.username, "DELETE", "doctors", 
              doctor_id, f"Deleted doctor: {doc.full_name}", get_client_ip(request))
    
    db.delete(doc)
    db.commit()
    return {"message": "Doctor deleted"}
