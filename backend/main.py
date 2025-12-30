import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from database import Base, engine
from routers import patients, doctors, appointments, admissions, prescriptions, invoices, health, auth_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

# Initialize rate limiter for DDoS protection
limiter = Limiter(key_func=get_remote_address)

# create tables (if models are defined)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Management API",
    description="Secure Hospital Management System with CIA Triad Implementation",
    version="2.0.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration - Restrict in production!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware for monitoring
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# include routers
app.include_router(auth_router.router)  # Authentication endpoints
app.include_router(health.router)       # Health check endpoints
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(admissions.router)
app.include_router(prescriptions.router)
app.include_router(invoices.router)

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    return {
        "status": "ok", 
        "service": "Hospital Management API",
        "version": "2.0.0",
        "security": "CIA Triad Implemented",
        "documentation": "/docs"
    }
