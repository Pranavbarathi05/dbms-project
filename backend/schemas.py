from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# -------------------------
# Patients
# -------------------------
class PatientCreate(BaseModel):
    full_name: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class PatientOut(BaseModel):
    id: int
    full_name: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# -------------------------
# Doctors
# -------------------------
class DoctorCreate(BaseModel):
    full_name: str
    speciality: Optional[str] = None
    phone: Optional[str] = None

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    speciality: Optional[str] = None
    phone: Optional[str] = None

class DoctorOut(BaseModel):
    id: int
    full_name: str
    speciality: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# -------------------------
# Appointments
# -------------------------
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    status: Optional[str] = "scheduled"
    reason: Optional[str] = None

class AppointmentUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    reason: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    status: str
    reason: Optional[str] = None

    class Config:
        orm_mode = True


# -------------------------
# Admissions
# -------------------------
class AdmissionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    admitted_at: datetime
    discharged_at: Optional[datetime] = None
    status: Optional[str] = "admitted"
    reason: Optional[str] = None

class AdmissionUpdate(BaseModel):
    discharged_at: Optional[datetime] = None
    status: Optional[str] = None
    reason: Optional[str] = None

class AdmissionOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    admitted_at: datetime
    discharged_at: Optional[datetime]
    status: str
    reason: Optional[str] = None

    class Config:
        orm_mode = True


# -------------------------
# Prescriptions
# -------------------------
class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    medication: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    instructions: Optional[str] = None

class PrescriptionUpdate(BaseModel):
    medication: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    instructions: Optional[str] = None

class PrescriptionOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int]
    medication: str
    dosage: Optional[str]
    frequency: Optional[str]
    instructions: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# -------------------------
# Invoices
# -------------------------
class InvoiceCreate(BaseModel):
    patient_id: int
    appointment_id: Optional[int] = None
    admission_id: Optional[int] = None
    amount: float = Field(..., gt=0)
    payment_status: Optional[str] = "unpaid"

class InvoiceUpdate(BaseModel):
    amount: Optional[float] = None
    payment_status: Optional[str] = None

class InvoiceOut(BaseModel):
    id: int
    patient_id: int
    appointment_id: Optional[int]
    admission_id: Optional[int]
    amount: float
    payment_status: str
    issued_at: Optional[datetime]

    class Config:
        orm_mode = True
