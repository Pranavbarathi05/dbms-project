import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

from fastapi import FastAPI
from .database import Base, engine
from .routers import patients, doctors, appointments, admissions, prescriptions, invoices
from fastapi.middleware.cors import CORSMiddleware

# create tables (if models are defined)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ALLOW ALL FRONTENDS (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# include routers
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(admissions.router)
app.include_router(prescriptions.router)
app.include_router(invoices.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "Hospital Management API"}
