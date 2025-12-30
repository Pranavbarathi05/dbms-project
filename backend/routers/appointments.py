from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from auth import get_current_active_user, check_role_permission
from audit_helper import log_audit, get_client_ip

router = APIRouter(prefix="/appointments", tags=["appointments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(
    request: Request,
    payload: schemas.AppointmentCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse", "receptionist"]))
):
    """Create appointment (All authenticated users)"""
    # Validate existence of patient & doctor
    p = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    d = db.query(models.Doctor).filter(models.Doctor.id == payload.doctor_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appt = models.Appointment(**payload.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    
    log_audit(db, current_user.id, current_user.username, "CREATE", "appointments", 
              appt.id, f"Created appointment for patient {payload.patient_id}", get_client_ip(request))
    return appt

@router.get("/", response_model=List[schemas.AppointmentOut])
def list_appointments(
    request: Request,
    skip: int = 0, 
    limit: int = Query(50, le=1000), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List appointments (All authenticated users)"""
    rows = db.query(models.Appointment).order_by(models.Appointment.scheduled_at.desc()).offset(skip).limit(limit).all()
    return rows

@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(
    request: Request,
    appointment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get appointment by ID (All authenticated users)"""
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(
    request: Request,
    appointment_id: int, 
    payload: schemas.AppointmentUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse"]))
):
    """Update appointment (Admin, Doctor, Nurse only)"""
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(appt, k, v)
    db.commit()
    db.refresh(appt)
    
    log_audit(db, current_user.id, current_user.username, "UPDATE", "appointments", 
              appointment_id, f"Updated appointment", get_client_ip(request))
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(
    request: Request,
    appointment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Delete appointment (Admin only)"""
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    log_audit(db, current_user.id, current_user.username, "DELETE", "appointments", 
              appointment_id, f"Deleted appointment", get_client_ip(request))
    
    db.delete(appt)
    db.commit()
    return {"message": "Appointment deleted"}
