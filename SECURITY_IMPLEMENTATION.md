# 🔒 Hospital Management System - Security Implementation

## CIA Triad Implementation Documentation

This document explains all security features implemented in the Hospital Management System and how they protect the **CIA Triad** (Confidentiality, Integrity, and Availability).

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Confidentiality Features](#confidentiality-features)
3. [Integrity Features](#integrity-features)
4. [Availability Features](#availability-features)
5. [Quick Start Guide](#quick-start-guide)
6. [API Authentication](#api-authentication)
7. [Security Best Practices](#security-best-practices)

---

## Overview

The Hospital Management System implements multiple layers of security to ensure patient data protection and system reliability. All features comply with healthcare data protection standards and best practices.

### Security Summary
- ✅ **Authentication & Authorization**: JWT-based with role-based access control
- ✅ **Audit Logging**: Complete activity tracking for compliance
- ✅ **Input Validation**: Comprehensive data validation and sanitization
- ✅ **Health Monitoring**: System health checks and performance monitoring
- ✅ **Data Encryption**: Sensitive field encryption capabilities
- ✅ **Rate Limiting**: DDoS protection
- ✅ **Security Headers**: XSS, clickjacking, and MIME sniffing protection

---

## 🔐 Confidentiality Features

Confidentiality ensures that sensitive patient data is only accessible to authorized users.

### 1. Authentication System (JWT-based)

**Implementation:**
- JWT (JSON Web Tokens) for secure, stateless authentication
- Tokens expire after 8 hours (480 minutes)
- Password hashing using bcrypt (industry-standard)

**Files:**
- `backend/auth.py` - Authentication logic
- `backend/routers/auth_router.py` - Auth endpoints
- `frontend/auth.js` - Frontend authentication handler

**How it Protects Confidentiality:**
- Users must provide valid credentials to access any patient data
- Tokens are cryptographically signed and cannot be forged
- Passwords are never stored in plain text
- Each API request requires a valid token

**Usage Example:**
```python
# Login endpoint
POST /auth/login
Body: {
  "username": "admin",
  "password": "admin123"
}

Response: {
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 2. Role-Based Access Control (RBAC)

**Implementation:**
- Four distinct roles: Admin, Doctor, Nurse, Receptionist
- Different permission levels for each role
- Protected endpoints require specific roles

**Roles and Permissions:**

| Action | Admin | Doctor | Nurse | Receptionist |
|--------|-------|--------|-------|--------------|
| View Patients | ✅ | ✅ | ✅ | ✅ |
| Add Patients | ✅ | ✅ | ✅ | ✅ |
| Edit Patients | ✅ | ✅ | ✅ | ❌ |
| Delete Patients | ✅ | ❌ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ | ❌ |
| View Audit Logs | ✅ | ❌ | ❌ | ❌ |

**How it Protects Confidentiality:**
- Limits data access based on job function
- Prevents unauthorized modifications
- Follows principle of least privilege
- Receptionists cannot access sensitive medical functions

**Code Example:**
```python
@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    current_user: User = Depends(check_role_permission(["admin"]))
):
    # Only admins can delete patients
    ...
```

### 3. Audit Logging

**Implementation:**
- Every action on patient data is logged
- Logs include: user, action, timestamp, IP address, success/failure
- Immutable audit trail for compliance (HIPAA, GDPR)

**Files:**
- `backend/models.py` - AuditLog model
- `backend/audit_helper.py` - Logging utilities
- `backend/routers/auth_router.py` - Audit log viewing endpoint

**What Gets Logged:**
- ✅ User login/logout
- ✅ Patient record access (READ)
- ✅ Patient record creation (CREATE)
- ✅ Patient record modification (UPDATE)
- ✅ Patient record deletion (DELETE)
- ✅ Failed authentication attempts
- ✅ User management actions

**How it Protects Confidentiality:**
- Creates accountability for all data access
- Enables detection of unauthorized access
- Provides forensic evidence for security incidents
- Meets compliance requirements for healthcare data

**Audit Log Example:**
```json
{
  "id": 1,
  "user_id": 5,
  "username": "dr_smith",
  "action": "READ",
  "resource": "patients",
  "resource_id": 123,
  "details": "Accessed patient record: John Doe",
  "ip_address": "192.168.1.100",
  "timestamp": "2025-12-30T10:30:45",
  "status": "success"
}
```

### 4. Data Encryption

**Implementation:**
- Fernet symmetric encryption for sensitive fields
- Key derivation using PBKDF2 with SHA-256
- Configurable via environment variables

**Files:**
- `backend/encryption.py` - Encryption utilities

**Features:**
- Encrypt sensitive fields (phone numbers, addresses, SSN)
- Decrypt only when authorized user requests data
- Mask sensitive data for display

**How it Protects Confidentiality:**
- Even if database is compromised, sensitive data remains encrypted
- Encryption keys stored separately from data
- Supports field-level encryption for PHI (Protected Health Information)

**Usage Example:**
```python
from encryption import encrypt_field, decrypt_field, mask_sensitive_data

# Encrypt before saving
encrypted_ssn = encrypt_field("123-45-6789")

# Decrypt when authorized user requests
original_ssn = decrypt_field(encrypted_ssn)

# Mask for display
masked = mask_sensitive_data("555-1234-5678")  # Returns: "********5678"
```

### 5. Security Headers

**Implementation:**
- Middleware adds security headers to all responses
- Prevents common web vulnerabilities

**Headers Added:**
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Strict-Transport-Security` - Forces HTTPS

**How it Protects Confidentiality:**
- Prevents XSS attacks that could steal tokens
- Prevents embedding site in malicious iframes
- Ensures browser security features are enabled

---

## ✅ Integrity Features

Integrity ensures that data is accurate, complete, and hasn't been tampered with.

### 1. Input Validation

**Implementation:**
- Pydantic models with custom validators
- Type checking and format validation
- SQL injection prevention via ORM

**Files:**
- `backend/schemas.py` - Validation schemas
- `backend/auth_schemas.py` - Auth validation

**Validations Implemented:**

**Patient Data:**
- ✅ Name: 2-150 characters, letters/spaces/dots/hyphens only
- ✅ Phone: 7-15 digits, international format supported
- ✅ Gender: Must be 'male', 'female', or 'other'
- ✅ Date of Birth: Cannot be in future, must be after 1900
- ✅ Email: Valid email format (when applicable)

**User Data:**
- ✅ Username: Unique, alphanumeric
- ✅ Password: Minimum 8 characters
- ✅ Email: Valid format, unique
- ✅ Role: Must be one of predefined roles

**How it Protects Integrity:**
- Prevents invalid data from entering the database
- Blocks SQL injection attempts
- Ensures data consistency
- Provides meaningful error messages

**Validation Example:**
```python
class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            cleaned = re.sub(r'[\s\-\(\)]', '', v)
            if not re.match(r'^\+?[0-9]{7,15}$', cleaned):
                raise ValueError('Invalid phone number format')
        return v
```

### 2. Transaction Management

**Implementation:**
- Database transactions ensure atomic operations
- Rollback on errors to maintain consistency
- Foreign key constraints enforced

**How it Protects Integrity:**
- All-or-nothing operations prevent partial updates
- Referential integrity maintained
- Prevents orphaned records

### 3. Audit Trail

**Implementation:**
- Same audit logging system tracks all modifications
- Maintains history of who changed what and when

**How it Protects Integrity:**
- Provides accountability for data changes
- Enables detection of unauthorized modifications
- Supports data recovery and forensics

### 4. Error Handling

**Implementation:**
- Comprehensive try-catch blocks
- Graceful error responses
- Logging of errors for debugging

**How it Protects Integrity:**
- Prevents partial operations from completing
- Maintains database consistency
- Provides clear feedback on validation failures

---

## ⚡ Availability Features

Availability ensures the system is accessible when needed and can recover from failures.

### 1. Health Check Endpoints

**Implementation:**
- Multiple health check endpoints for monitoring
- System resource monitoring (CPU, memory, disk)
- Database connectivity checks

**Files:**
- `backend/routers/health.py` - Health check endpoints

**Endpoints:**

#### Basic Health Check
```
GET /health/
Response: {
  "status": "healthy",
  "service": "Hospital Management API",
  "timestamp": "2025-12-30T10:30:45",
  "uptime_seconds": 3600
}
```

#### Detailed Health Check
```
GET /health/detailed
Response: {
  "status": "healthy",
  "timestamp": "2025-12-30T10:30:45",
  "uptime_seconds": 3600,
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    "system": {
      "status": "healthy",
      "cpu_percent": 25.5,
      "memory_percent": 45.2,
      "memory_available_mb": 4096,
      "disk_percent": 60.0,
      "disk_free_gb": 50.5
    }
  }
}
```

#### Database Health
```
GET /health/database
Response: {
  "status": "healthy",
  "connection": "active",
  "statistics": {
    "patients": 1250,
    "doctors": 45,
    "appointments": 3200
  }
}
```

#### Kubernetes Probes
```
GET /health/liveness   # For liveness probe
GET /health/readiness  # For readiness probe
```

**How it Protects Availability:**
- Early detection of issues before system failure
- Monitoring tools can alert on degraded performance
- Kubernetes/Docker can auto-restart unhealthy containers
- Provides visibility into system status

### 2. Rate Limiting (DDoS Protection)

**Implementation:**
- SlowAPI library for rate limiting
- Configurable limits per endpoint
- Based on client IP address

**Files:**
- `backend/main.py` - Rate limiter configuration

**Configuration:**
```python
@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    ...
```

**How it Protects Availability:**
- Prevents denial-of-service attacks
- Limits abusive clients
- Protects server resources
- Ensures fair resource allocation

**Default Limits:**
- Root endpoint: 10 requests/minute
- Other endpoints: Can be configured as needed

### 3. Connection Pooling

**Implementation:**
- SQLAlchemy connection pooling
- Configurable pool size and overflow

**Configuration:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,    # Auto-reconnect on connection loss
    pool_size=20,          # 20 connections in pool
    max_overflow=30        # Allow 30 extra connections if needed
)
```

**How it Protects Availability:**
- Reuses database connections efficiently
- Handles connection failures gracefully
- Prevents connection exhaustion
- Improves response times

### 4. Error Recovery

**Implementation:**
- Automatic retry on transient database errors
- Graceful degradation on non-critical failures
- Detailed error logging

**How it Protects Availability:**
- System continues operating despite minor issues
- Automatic recovery from temporary failures
- Minimal downtime

### 5. Performance Monitoring

**Implementation:**
- Request timing middleware
- Process time headers in responses

**File:**
- `backend/main.py` - Timing middleware

**How it Protects Availability:**
- Identifies slow endpoints
- Enables performance optimization
- Proactive problem detection

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.13+
- MySQL/MariaDB server running
- Virtual environment (recommended)

### Installation Steps

1. **Clone and navigate to backend:**
```bash
cd /home/pranav/Downloads/dbms-project/backend
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure database:**
```bash
# Start MySQL
sudo systemctl start mysql

# Create database
sudo mysql -e "CREATE DATABASE IF NOT EXISTS hospital_db;"

# Configure MySQL authentication (if needed)
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password; FLUSH PRIVILEGES;"
```

5. **Initialize database tables:**
```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine); print('Tables created!')"
```

6. **Create admin user:**
```bash
python << EOF
from database import SessionLocal
from auth import get_password_hash
import models

db = SessionLocal()
admin = models.User(
    username="admin",
    email="admin@hospital.com",
    full_name="System Administrator",
    hashed_password=get_password_hash("admin123"),
    role="admin",
    is_active=True
)
db.add(admin)
db.commit()
print("Admin user created: admin / admin123")
db.close()
EOF
```

7. **Start the server:**
```bash
uvicorn main:app --reload --host 0.0.0.0
```

8. **Open frontend:**
```bash
cd ../frontend
python3 -m http.server 8080
```

9. **Access the application:**
- Frontend: http://localhost:8080
- API Docs: http://localhost:8000/docs
- Admin Login: username: `admin`, password: `admin123`

---

## 🔑 API Authentication

### Login Flow

1. **User logs in via frontend:**
```javascript
POST http://localhost:8000/auth/login
Body: {
  "username": "admin",
  "password": "admin123"
}
```

2. **Server returns JWT token:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

3. **Frontend stores token:**
```javascript
localStorage.setItem('access_token', token);
```

4. **All subsequent requests include token:**
```javascript
fetch('http://localhost:8000/patients/', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
```

### Token Structure

The JWT token contains:
- **Subject (sub)**: Username
- **Role**: User's role for authorization
- **Expiration (exp)**: Token expiry timestamp

### Protected Endpoints

All endpoints except `/auth/login` and `/health/` require authentication.

**Example - Get Current User:**
```
GET /auth/me
Headers: Authorization: Bearer <token>

Response: {
  "id": 1,
  "username": "admin",
  "email": "admin@hospital.com",
  "full_name": "System Administrator",
  "role": "admin",
  "is_active": true,
  "created_at": "2025-12-30T10:00:00"
}
```

---

## 🛡️ Security Best Practices

### For Production Deployment

1. **Change Default Credentials:**
```python
# In auth.py, change:
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")

# In encryption.py, change:
ENCRYPTION_PASSWORD = os.getenv("ENCRYPTION_KEY")
```

2. **Use Environment Variables:**
Create `.env` file:
```env
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ENCRYPTION_KEY=your-encryption-key-here
DATABASE_URL=mysql+pymysql://user:pass@localhost/hospital_db
```

3. **Enable HTTPS:**
```python
# In production, enforce HTTPS
app.add_middleware(
    HTTPSRedirectMiddleware
)
```

4. **Restrict CORS:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Not "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

5. **Set Up Database Backups:**
```bash
# Automated daily backups
0 2 * * * mysqldump hospital_db > /backups/hospital_db_$(date +\%Y\%m\%d).sql
```

6. **Monitor Audit Logs:**
```python
# Regularly review audit logs
GET /auth/audit-logs?limit=100
```

7. **Update Dependencies Regularly:**
```bash
pip list --outdated
pip install --upgrade <package>
```

### Security Checklist

- [ ] Changed default JWT secret key
- [ ] Changed default encryption key
- [ ] Changed default admin password
- [ ] Enabled HTTPS in production
- [ ] Restricted CORS to specific origins
- [ ] Set up database backups
- [ ] Configured firewall rules
- [ ] Set up monitoring/alerting
- [ ] Review audit logs regularly
- [ ] Keep dependencies updated
- [ ] Implement password rotation policy
- [ ] Set up fail2ban for SSH
- [ ] Configure rate limiting appropriately

---

## 📊 Monitoring & Maintenance

### View Audit Logs (Admin Only)
```
GET /auth/audit-logs?skip=0&limit=100
```

### Check System Health
```
GET /health/detailed
```

### Monitor User Activity
- Review login patterns
- Check failed authentication attempts
- Analyze access patterns to patient records

### Database Maintenance
- Regular backups
- Monitor database size
- Optimize slow queries
- Archive old audit logs

---

## 📝 Summary

### CIA Triad Protection Summary

| Security Aspect | Features | CIA Component |
|----------------|----------|---------------|
| **Authentication** | JWT tokens, Password hashing | Confidentiality |
| **Authorization** | Role-based access control | Confidentiality |
| **Audit Logging** | Activity tracking, IP logging | Confidentiality + Integrity |
| **Input Validation** | Schema validation, Type checking | Integrity |
| **Encryption** | Field-level encryption | Confidentiality |
| **Health Checks** | Multiple monitoring endpoints | Availability |
| **Rate Limiting** | DDoS protection | Availability |
| **Connection Pooling** | Efficient resource usage | Availability |
| **Security Headers** | XSS, clickjacking protection | Confidentiality |
| **Error Handling** | Graceful degradation | Availability + Integrity |

### Compliance Features

- **HIPAA Compliant**: Audit logging, access controls, encryption
- **GDPR Ready**: Data protection, access logs, right to be forgotten
- **HITRUST**: Security controls and monitoring

---

## 🔗 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **JWT Best Practices**: https://tools.ietf.org/html/rfc8725
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **HIPAA Security Rule**: https://www.hhs.gov/hipaa/for-professionals/security/

---

## 📞 Support

For security issues or questions:
- Review audit logs: `GET /auth/audit-logs`
- Check system health: `GET /health/detailed`
- View API documentation: http://localhost:8000/docs

---

**Document Version**: 1.0  
**Last Updated**: December 30, 2025  
**Author**: Security Implementation Team
