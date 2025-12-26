from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import SessionLocal
from decimal import Decimal

router = APIRouter(prefix="/invoices", tags=["invoices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.InvoiceOut)
def create_invoice(payload: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    # validate patient
    p = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    if payload.appointment_id:
        appt = db.query(models.Appointment).filter(models.Appointment.id == payload.appointment_id).first()
        if not appt:
            raise HTTPException(status_code=404, detail="Appointment not found")
    if payload.admission_id:
        adm = db.query(models.Admission).filter(models.Admission.id == payload.admission_id).first()
        if not adm:
            raise HTTPException(status_code=404, detail="Admission not found")

    inv = models.Invoice(
        patient_id=payload.patient_id,
        appointment_id=payload.appointment_id,
        admission_id=payload.admission_id,
        amount=Decimal(str(payload.amount)),
        payment_status=payload.payment_status
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/", response_model=List[schemas.InvoiceOut])
def list_invoices(skip: int = 0, limit: int = Query(50, le=1000), db: Session = Depends(get_db)):
    rows = db.query(models.Invoice).order_by(models.Invoice.issued_at.desc()).offset(skip).limit(limit).all()
    return rows

@router.get("/{invoice_id}", response_model=schemas.InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

@router.put("/{invoice_id}", response_model=schemas.InvoiceOut)
def update_invoice(invoice_id: int, payload: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    for k, v in payload.dict(exclude_unset=True).items():
        if k == "amount":
            setattr(inv, k, Decimal(str(v)))
        else:
            setattr(inv, k, v)
    db.commit()
    db.refresh(inv)
    return inv

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(inv)
    db.commit()
    return {"message": "Invoice deleted"}
