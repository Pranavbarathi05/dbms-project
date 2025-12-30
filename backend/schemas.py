from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime, date
import re

# -------------------------
# Patients
# -------------------------
class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150, description="Patient full name")
    dob: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender: male, female, or other")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    address: Optional[str] = Field(None, max_length=255, description="Address")
    
    @validator('full_name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if not re.match(r'^[a-zA-Z\s\.\-]+$', v):
            raise ValueError('Name can only contain letters, spaces, dots, and hyphens')
        return v.strip()
    
    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be male, female, or other')
        return v.lower() if v else None
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            # Remove common separators
            cleaned = re.sub(r'[\s\-\(\)]', '', v)
            if not re.match(r'^\+?[0-9]{7,15}$', cleaned):
                raise ValueError('Invalid phone number format')
        return v
    
    @validator('dob')
    def validate_dob(cls, v):
        if v and v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        if v and v.year < 1900:
            raise ValueError('Date of birth cannot be before 1900')
        return v

class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    
    @validator('full_name')
    def validate_name(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if v and not re.match(r'^[a-zA-Z\s\.\-]+$', v):
            raise ValueError('Name can only contain letters, spaces, dots, and hyphens')
        return v.strip() if v else None
    
    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be male, female, or other')
        return v.lower() if v else None
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            cleaned = re.sub(r'[\s\-\(\)]', '', v)
            if not re.match(r'^\+?[0-9]{7,15}$', cleaned):
                raise ValueError('Invalid phone number format')
        return v
    
    @validator('dob')
    def validate_dob(cls, v):
        if v and v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        if v and v.year < 1900:
            raise ValueError('Date of birth cannot be before 1900')
        return v

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
    full_name: str = Field(..., min_length=2, max_length=150)
    speciality: Optional[str] = Field(None, max_length=120)
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
