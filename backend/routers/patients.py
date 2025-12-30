from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from database import SessionLocal
from auth import get_current_active_user, check_role_permission
from audit_helper import log_audit, get_client_ip

router = APIRouter(prefix="/patients", tags=["patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.PatientOut)
def create_patient(
    request: Request,
    payload: schemas.PatientCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse", "receptionist"]))
):
    """Create a new patient (Authenticated users only)"""
    patient = models.Patient(**payload.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    # Audit log
    log_audit(db, current_user.id, current_user.username, "CREATE", "patients", 
              patient.id, f"Created patient: {patient.full_name}", get_client_ip(request))
    
    return patient

@router.get("/", response_model=List[schemas.PatientOut])
def list_patients(
    request: Request,
    skip: int = 0, 
    limit: int = Query(50, le=1000), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List patients (Authenticated users only)"""
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    
    # Audit log
    log_audit(db, current_user.id, current_user.username, "READ", "patients", 
              None, f"Listed {len(patients)} patients", get_client_ip(request))
    
    return patients

@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(
    request: Request,
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get patient by ID (Authenticated users only)"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Audit log - HIPAA compliance: log all access to patient records
    log_audit(db, current_user.id, current_user.username, "READ", "patients", 
              patient_id, f"Accessed patient record: {patient.full_name}", get_client_ip(request))
    
    return patient

@router.put("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(
    request: Request,
    patient_id: int, 
    payload: schemas.PatientUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse"]))
):
    """Update patient (Admin, Doctor, Nurse only)"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    old_data = {k: getattr(patient, k) for k in payload.dict(exclude_unset=True).keys()}
    
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(patient, k, v)
    db.commit()
    db.refresh(patient)
    
    # Audit log
    log_audit(db, current_user.id, current_user.username, "UPDATE", "patients", 
              patient_id, f"Updated patient: {patient.full_name}", get_client_ip(request))
    
    return patient

@router.delete("/{patient_id}")
def delete_patient(
    request: Request,
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Delete patient (Admin only)"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_name = patient.full_name
    db.delete(patient)
    db.commit()
    
    # Audit log
    log_audit(db, current_user.id, current_user.username, "DELETE", "patients", 
              patient_id, f"Deleted patient: {patient_name}", get_client_ip(request))
    
    return {"message": "Patient deleted"}
