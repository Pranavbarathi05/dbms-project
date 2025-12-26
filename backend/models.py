from sqlalchemy import (
    Column, Integer, BigInteger, String, Date, DateTime,
    Enum, ForeignKey, DECIMAL, Text
)
from sqlalchemy.orm import relationship
from .database import Base


# ===============================
# 1) PATIENTS
# ===============================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    dob = Column(Date)
    gender = Column(Enum("male", "female", "other"))
    phone = Column(String(20))
    address = Column(String(255))
    created_at = Column(DateTime)

    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    admissions = relationship("Admission", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    invoices = relationship("Invoice", back_populates="patient")


# ===============================
# 2) DOCTORS
# ===============================
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    speciality = Column(String(120))
    phone = Column(String(20))
    created_at = Column(DateTime)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    admissions = relationship("Admission", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")


# ===============================
# 3) APPOINTMENTS
# ===============================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(Enum("scheduled", "completed", "cancelled", "no-show"), default="scheduled")
    reason = Column(String(255))

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    prescriptions = relationship("Prescription", back_populates="appointment")
    invoices = relationship("Invoice", back_populates="appointment")


# ===============================
# 4) ADMISSIONS
# ===============================
class Admission(Base):
    __tablename__ = "admissions"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    admitted_at = Column(DateTime, nullable=False)
    discharged_at = Column(DateTime)
    status = Column(Enum("admitted", "discharged"), default="admitted")
    reason = Column(Text)

    # Relationships
    patient = relationship("Patient", back_populates="admissions")
    doctor = relationship("Doctor", back_populates="admissions")
    invoices = relationship("Invoice", back_populates="admission")


# ===============================
# 5) PRESCRIPTIONS
# ===============================
class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id"))
    medication = Column(String(150), nullable=False)
    dosage = Column(String(80))
    frequency = Column(String(80))
    instructions = Column(Text)
    created_at = Column(DateTime)

    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    appointment = relationship("Appointment", back_populates="prescriptions")


# ===============================
# 6) INVOICES
# ===============================
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id"))
    admission_id = Column(BigInteger, ForeignKey("admissions.id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(Enum("unpaid", "partial", "paid"), default="unpaid")
    issued_at = Column(DateTime)

    # Relationships
    patient = relationship("Patient", back_populates="invoices")
    appointment = relationship("Appointment", back_populates="invoices")
    admission = relationship("Admission", back_populates="invoices")
