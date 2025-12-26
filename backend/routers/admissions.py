from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/admissions", tags=["admissions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AdmissionOut)
def create_admission(payload: schemas.AdmissionCreate, db: Session = Depends(get_db)):
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
    return adm

@router.get("/", response_model=List[schemas.AdmissionOut])
def list_admissions(skip: int = 0, limit: int = Query(50, le=1000), db: Session = Depends(get_db)):
    rows = db.query(models.Admission).order_by(models.Admission.admitted_at.desc()).offset(skip).limit(limit).all()
    return rows

@router.get("/{admission_id}", response_model=schemas.AdmissionOut)
def get_admission(admission_id: int, db: Session = Depends(get_db)):
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    return adm

@router.put("/{admission_id}", response_model=schemas.AdmissionOut)
def update_admission(admission_id: int, payload: schemas.AdmissionUpdate, db: Session = Depends(get_db)):
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(adm, k, v)
    db.commit()
    db.refresh(adm)
    return adm

@router.delete("/{admission_id}")
def delete_admission(admission_id: int, db: Session = Depends(get_db)):
    adm = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    db.delete(adm)
    db.commit()
    return {"message": "Admission deleted"}
