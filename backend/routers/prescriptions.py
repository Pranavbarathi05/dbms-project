from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.PrescriptionOut)
def create_prescription(payload: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    # validate patient + doctor (appointment optional)
    p = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    d = db.query(models.Doctor).filter(models.Doctor.id == payload.doctor_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if payload.appointment_id:
        appt = db.query(models.Appointment).filter(models.Appointment.id == payload.appointment_id).first()
        if not appt:
            raise HTTPException(status_code=404, detail="Appointment not found")

    pres = models.Prescription(**payload.dict())
    db.add(pres)
    db.commit()
    db.refresh(pres)
    return pres

@router.get("/", response_model=List[schemas.PrescriptionOut])
def list_prescriptions(skip: int = 0, limit: int = Query(50, le=1000), db: Session = Depends(get_db)):
    rows = db.query(models.Prescription).order_by(models.Prescription.created_at.desc()).offset(skip).limit(limit).all()
    return rows

@router.get("/{prescription_id}", response_model=schemas.PrescriptionOut)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    pres = db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pres

@router.put("/{prescription_id}", response_model=schemas.PrescriptionOut)
def update_prescription(prescription_id: int, payload: schemas.PrescriptionUpdate, db: Session = Depends(get_db)):
    pres = db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(pres, k, v)
    db.commit()
    db.refresh(pres)
    return pres

@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    pres = db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    db.delete(pres)
    db.commit()
    return {"message": "Prescription deleted"}
