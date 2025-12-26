from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/appointments", tags=["appointments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
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
    return appt

@router.get("/", response_model=List[schemas.AppointmentOut])
def list_appointments(skip: int = 0, limit: int = Query(50, le=1000), db: Session = Depends(get_db)):
    rows = db.query(models.Appointment).order_by(models.Appointment.scheduled_at.desc()).offset(skip).limit(limit).all()
    return rows

@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(appointment_id: int, payload: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(appt, k, v)
    db.commit()
    db.refresh(appt)
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"message": "Appointment deleted"}
