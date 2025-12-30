from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
import psutil
import time
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health & Monitoring"])

start_time = time.time()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Hospital Management API",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": int(time.time() - start_time)
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check including database connectivity"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": int(time.time() - start_time),
        "checks": {}
    }
    
    # Database connectivity check
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
    
    # System resources check
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status["checks"]["system"] = {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_mb": memory.available / (1024 * 1024),
            "disk_percent": disk.percent,
            "disk_free_gb": disk.free / (1024 * 1024 * 1024)
        }
        
        # Alert if resources are critical
        if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
            health_status["status"] = "degraded"
            health_status["checks"]["system"]["warning"] = "High resource usage detected"
            
    except Exception as e:
        health_status["checks"]["system"] = {
            "status": "unknown",
            "message": f"Could not retrieve system metrics: {str(e)}"
        }
    
    return health_status

@router.get("/database")
async def database_health(db: Session = Depends(get_db)):
    """Check database health and statistics"""
    try:
        # Test query
        result = db.execute(text("SELECT 1")).fetchone()
        
        # Get table counts
        patients_count = db.execute(text("SELECT COUNT(*) FROM patients")).fetchone()[0]
        doctors_count = db.execute(text("SELECT COUNT(*) FROM doctors")).fetchone()[0]
        appointments_count = db.execute(text("SELECT COUNT(*) FROM appointments")).fetchone()[0]
        
        return {
            "status": "healthy",
            "connection": "active",
            "statistics": {
                "patients": patients_count,
                "doctors": doctors_count,
                "appointments": appointments_count
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database health check failed: {str(e)}")

@router.get("/readiness")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe for Kubernetes/container orchestration"""
    try:
        # Check if database is ready
        db.execute(text("SELECT 1"))
        return {"ready": True, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service not ready")

@router.get("/liveness")
async def liveness_check():
    """Liveness probe for Kubernetes/container orchestration"""
    return {"alive": True, "timestamp": datetime.utcnow().isoformat()}
