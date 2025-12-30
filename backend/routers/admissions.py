from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from auth import get_current_active_user, check_role_permission
from audit_helper import log_audit, get_client_ip

router = APIRouter(prefix="/admissions", tags=["admissions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AdmissionOut)
def create_admission(
    request: Request,
    payload: schemas.AdmissionCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse"]))
):
    """Create admission (Admin, Doctor, Nurse only)"""
    # Validate patient & doctor
    p = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    d = db.query(models.Doctor).filter(models.Doctor.id == payload.doctor_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Doctor not found")

    adm = models.Admission(**payload.dict())
    db.add(adm)
    db.commit()
    db.refresh(adm)
    
    log_audit(db, current_user.id, current_user.username, "CREATE", "admissions", 
              adm.id, f"Admitted patient {payload.patient_id}", get_client_ip(request))
    return adm

@router.get("/", response_model=List[schemas.AdmissionOut])
def list_admissions(
    request: Request,
    skip: int = 0, 
    limit: int = Query(50, le=1000), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse"]))
):
    """List admissions (Admin, Doctor, Nurse only)"""
    rows = db.query(models.Admission).order_by(models.Admission.admitted_at.desc()).offset(skip).limit(limit).all()
    return rows

@router.get("/{admission_id}", response_model=schemas.AdmissionOut)
def get_admission(
    request: Request,
    admission_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse"]))
):
    """Get admission by ID (Admin, Doctor, Nurse only)"""
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    return adm

@router.put("/{admission_id}", response_model=schemas.AdmissionOut)
def update_admission(
    request: Request,
    admission_id: int, 
    payload: schemas.AdmissionUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin", "doctor", "nurse"]))
):
    """Update admission (Admin, Doctor, Nurse only)"""
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(adm, k, v)
    db.commit()
    db.refresh(adm)
    
    log_audit(db, current_user.id, current_user.username, "UPDATE", "admissions", 
              admission_id, f"Updated admission", get_client_ip(request))
    return adm

@router.delete("/{admission_id}")
def delete_admission(
    request: Request,
    admission_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_role_permission(["admin"]))
):
    """Delete admission (Admin only)"""
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    
    log_audit(db, current_user.id, current_user.username, "DELETE", "admissions", 
              admission_id, f"Deleted admission", get_client_ip(request))
    
    db.delete(adm)
    db.commit()
    return {"message": "Admission deleted"}
