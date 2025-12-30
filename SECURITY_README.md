# Hospital Management System - Security Implementation
## CIA Triad Security Features

This document details the comprehensive security implementation protecting the **Confidentiality**, **Integrity**, and **Availability** of the Hospital Management System.

---

## 🔒 CONFIDENTIALITY (Protecting Sensitive Data)

### 1. **Authentication & Authorization System**
**Implementation:** JWT-based authentication with role-based access control (RBAC)

**Files:**
- `backend/auth.py` - Authentication utilities
- `backend/routers/auth_router.py` - Authentication endpoints
- `backend/models.py` - User model with roles

**Features:**
- **JWT Tokens:** Secure token-based authentication with 8-hour expiration
- **Password Hashing:** Bcrypt hashing for password storage (never store plain text)
- **Role-Based Access Control:** Four user roles with different permissions:
  - **Admin:** Full system access, user management
  - **Doctor:** Access to patient records, prescriptions, medical data
  - **Nurse:** Limited patient access, appointment management
  - **Receptionist:** Patient registration, appointment scheduling

**How it Protects CIA:**
- ✅ **Confidentiality:** Only authenticated users can access sensitive patient data
- ✅ **Integrity:** Role-based permissions prevent unauthorized data modifications
- ✅ **Availability:** Prevents unauthorized users from disrupting services

**Endpoints:**
```
POST /auth/register - Register new user (Admin only)
POST /auth/login - User authentication
GET /auth/me - Get current user info
GET /auth/users - List all users (Admin only)
PUT /auth/users/{id} - Update user (Admin only)
```

**Example Usage:**
```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=securepass123"

# Use token for authenticated requests
curl -X GET http://localhost:8000/patients \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### 2. **Audit Logging System**
**Implementation:** Comprehensive logging of all sensitive operations

**Files:**
- `backend/models.py` - AuditLog model
- `backend/audit_helper.py` - Audit logging utilities
- `backend/routers/patients.py` - Example implementation in routers

**Features:**
- **Complete Activity Tracking:** Every action (CREATE, READ, UPDATE, DELETE) is logged
- **User Attribution:** Records who performed each action
- **IP Address Logging:** Tracks source of requests for security analysis
- **Timestamp Precision:** Exact time of each operation
- **Status Tracking:** Success/failure of operations
- **HIPAA Compliance:** Meets healthcare data access logging requirements

**What Gets Logged:**
- Patient record access (READ operations)
- Data modifications (CREATE, UPDATE, DELETE)
- Login attempts (successful and failed)
- Administrative actions
- User management operations

**How it Protects CIA:**
- ✅ **Confidentiality:** Tracks who accessed sensitive data (HIPAA requirement)
- ✅ **Integrity:** Creates audit trail to detect unauthorized modifications
- ✅ **Availability:** Helps identify and respond to security incidents

**Database Schema:**
```sql
audit_logs:
- id: Auto-increment primary key
- user_id: User who performed action
- username: Username for quick reference
- action: CREATE, READ, UPDATE, DELETE
- resource: patients, doctors, appointments, etc.
- resource_id: ID of affected record
- details: JSON string with additional information
- ip_address: Source IP address
- timestamp: When action occurred
- status: success/failed
```

**View Audit Logs:**
```bash
# Admin only
curl -X GET http://localhost:8000/auth/audit-logs \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

### 3. **Data Encryption**
**Implementation:** Field-level encryption for sensitive data

**Files:**
- `backend/encryption.py` - Encryption utilities using Fernet (symmetric encryption)

**Features:**
- **Symmetric Encryption:** Uses Fernet encryption (AES-128 in CBC mode)
- **Key Derivation:** PBKDF2 with SHA-256 for secure key generation
- **Selective Encryption:** Can encrypt sensitive fields (phone, SSN, medical records)
- **Data Masking:** Ability to mask sensitive data for display

**Supported Operations:**
```python
from encryption import encrypt_field, decrypt_field, mask_sensitive_data

# Encrypt sensitive data before storage
encrypted_phone = encrypt_field("555-1234-5678")

# Decrypt when authorized user needs it
original_phone = decrypt_field(encrypted_phone)

# Mask for display purposes
masked_phone = mask_sensitive_data("555-1234-5678")  # Returns "********5678"
```

**How it Protects CIA:**
- ✅ **Confidentiality:** Encrypts sensitive data at rest
- ✅ **Integrity:** Tampered encrypted data won't decrypt properly
- ✅ **Availability:** Ensures data remains usable when needed

**Best Practices:**
- Store encryption key in environment variable (not in code)
- Use different keys for different environments (dev/staging/prod)
- Regularly rotate encryption keys
- Consider using AWS KMS or Azure Key Vault for production

---

## 🛡️ INTEGRITY (Ensuring Data Accuracy & Consistency)

### 1. **Input Validation**
**Implementation:** Comprehensive Pydantic validation schemas

**Files:**
- `backend/schemas.py` - Validation schemas for all data models
- `backend/auth_schemas.py` - Authentication-specific schemas

**Features:**
- **Type Validation:** Ensures correct data types (string, int, date, etc.)
- **Format Validation:** Validates phone numbers, emails, dates
- **Range Validation:** Age validation, date ranges, string lengths
- **Regex Patterns:** Name validation, phone format checking
- **Custom Validators:** Business logic validation

**Examples:**
```python
# Patient validation
- Name: 2-150 chars, letters/spaces/dots/hyphens only
- Phone: 7-15 digits with optional country code
- Gender: Must be 'male', 'female', or 'other'
- Date of Birth: Cannot be in future or before 1900
- Email: Valid email format

# Password validation
- Minimum 8 characters
- Required complexity (can be enhanced)
```

**How it Protects CIA:**
- ✅ **Integrity:** Prevents invalid/malicious data entry
- ✅ **Confidentiality:** Prevents injection attacks
- ✅ **Availability:** Prevents data that could crash the system

**SQL Injection Protection:**
- Uses SQLAlchemy ORM (parameterized queries)
- Never constructs raw SQL from user input
- Input validation as additional layer

---

### 2. **Database Constraints**
**Implementation:** Foreign keys, unique constraints, and proper indexes

**Features:**
- **Foreign Key Constraints:** Maintains referential integrity
- **Unique Constraints:** Prevents duplicate usernames/emails
- **NOT NULL Constraints:** Ensures required fields are present
- **Indexes:** Improves query performance and data lookups

**How it Protects CIA:**
- ✅ **Integrity:** Database enforces data consistency rules
- ✅ **Availability:** Indexes improve performance

---

### 3. **Audit Trail & Versioning**
**Implementation:** Timestamp tracking and modification history

**Features:**
- **created_at:** When record was created
- **last_login:** Last user login timestamp
- **Audit logs:** Complete history of changes

**How it Protects CIA:**
- ✅ **Integrity:** Can track and verify changes over time
- ✅ **Confidentiality:** Identify when data was accessed

---

## ⚡ AVAILABILITY (Ensuring System Uptime & Reliability)

### 1. **Health Check & Monitoring System**
**Implementation:** Comprehensive health check endpoints

**Files:**
- `backend/routers/health.py` - Health monitoring endpoints

**Features:**
- **Basic Health Check:** Simple liveness probe
- **Detailed Health Check:** System resources, database connectivity
- **Database Health:** Connection status and table statistics
- **Readiness Probe:** Kubernetes-ready endpoint
- **Liveness Probe:** Container orchestration support

**Endpoints:**
```
GET /health - Basic health status
GET /health/detailed - Comprehensive health report
GET /health/database - Database connectivity and stats
GET /health/readiness - Readiness probe
GET /health/liveness - Liveness probe
```

**Monitored Metrics:**
- CPU usage percentage
- Memory usage and availability
- Disk space usage
- Database connectivity
- System uptime
- Active connections
- Table row counts

**How it Protects CIA:**
- ✅ **Availability:** Early detection of system issues
- ✅ **Integrity:** Monitors data consistency
- ✅ **Confidentiality:** Ensures security systems are operational

**Example Response:**
```json
{
  "status": "healthy",
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
      "disk_percent": 60.1
    }
  }
}
```

---

### 2. **Rate Limiting (DDoS Protection)**
**Implementation:** SlowAPI rate limiter

**Files:**
- `backend/main.py` - Rate limiter configuration

**Features:**
- **Per-IP Rate Limiting:** Prevents single source from overwhelming system
- **Configurable Limits:** Different limits for different endpoints
- **Automatic 429 Responses:** Returns "Too Many Requests" when exceeded

**Configuration:**
```python
@app.get("/")
@limiter.limit("10/minute")  # Max 10 requests per minute per IP
```

**How it Protects CIA:**
- ✅ **Availability:** Prevents denial-of-service attacks
- ✅ **Integrity:** Prevents brute-force attacks on authentication
- ✅ **Confidentiality:** Limits enumeration attacks

---

### 3. **Connection Pooling & Error Handling**
**Implementation:** SQLAlchemy connection pooling

**Files:**
- `backend/database.py` - Database configuration

**Features:**
- **Connection Pool:** 20 connections, 30 max overflow
- **Auto-reconnect:** `pool_pre_ping=True` detects stale connections
- **Graceful Degradation:** Proper error handling and responses

**Configuration:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Auto-reconnect on stale connections
    pool_size=20,         # Handle 20 concurrent connections
    max_overflow=30       # Allow 30 additional connections if needed
)
```

**How it Protects CIA:**
- ✅ **Availability:** Handles multiple concurrent users
- ✅ **Availability:** Auto-recovers from connection failures
- ✅ **Integrity:** Prevents data corruption from connection issues

---

### 4. **Security Headers**
**Implementation:** HTTP security headers middleware

**Files:**
- `backend/main.py` - Security headers middleware

**Features:**
```
X-Content-Type-Options: nosniff - Prevents MIME-type sniffing
X-Frame-Options: DENY - Prevents clickjacking attacks
X-XSS-Protection: 1; mode=block - Enables XSS filtering
Strict-Transport-Security - Forces HTTPS connections
X-Process-Time - Response time monitoring
```

**How it Protects CIA:**
- ✅ **Confidentiality:** Prevents data theft via XSS/clickjacking
- ✅ **Integrity:** Prevents content manipulation
- ✅ **Availability:** Performance monitoring via process time

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```env
ENCRYPTION_KEY=your-secure-encryption-key-change-in-production
SECRET_KEY=your-jwt-secret-key-change-in-production
DATABASE_URL=mysql+pymysql://root:password@localhost/hospital_db
```

### 3. Create Database Tables
```bash
# Tables are auto-created when you start the server
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 4. Create First Admin User
```bash
# Start server first, then use SQL or create via API
# You need to manually create first admin in database or via SQL script
```

### 5. Start Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# API documentation
Open browser: http://localhost:8000/docs
```

---

## 📊 Security Testing Checklist

- ✅ **Authentication:** Can only authenticated users access patient data?
- ✅ **Authorization:** Can receptionist access admin functions? (Should fail)
- ✅ **Audit Logging:** Are all patient accesses logged?
- ✅ **Input Validation:** Does system reject invalid phone numbers/dates?
- ✅ **Rate Limiting:** Does system block after 10 requests in 1 minute?
- ✅ **Health Monitoring:** Is /health endpoint responsive?
- ✅ **Encryption:** Can you encrypt/decrypt sensitive fields?
- ✅ **SQL Injection:** Does system reject malicious SQL in inputs?
- ✅ **Password Security:** Are passwords hashed (not stored plain)?
- ✅ **Session Management:** Do tokens expire properly?

---

## 🔐 Production Deployment Checklist

### Security Hardening:
- [ ] Change SECRET_KEY and ENCRYPTION_KEY to strong random values
- [ ] Store secrets in environment variables or key vault
- [ ] Enable HTTPS/TLS (use nginx or load balancer)
- [ ] Restrict CORS origins to specific domains
- [ ] Enable database SSL connections
- [ ] Set up automated backups
- [ ] Configure log aggregation (ELK stack, CloudWatch)
- [ ] Set up monitoring alerts (PagerDuty, OpsGenie)
- [ ] Implement API versioning
- [ ] Add request/response logging
- [ ] Configure firewall rules
- [ ] Enable IP whitelisting for admin functions
- [ ] Set up intrusion detection system
- [ ] Regular security audits and penetration testing

### Database Security:
- [ ] Use strong database passwords
- [ ] Enable database audit logging
- [ ] Configure automated backups
- [ ] Test backup restoration
- [ ] Implement point-in-time recovery
- [ ] Set up database replication
- [ ] Enable query logging for audit

---

## 📚 Additional Security Resources

### Compliance:
- **HIPAA Compliance:** Audit logging meets PHI access requirements
- **GDPR:** Data encryption and access controls
- **PCI DSS:** If handling payment data, additional measures needed

### Best Practices:
- Regularly update dependencies (`pip install --upgrade`)
- Monitor security advisories for vulnerabilities
- Conduct regular security audits
- Implement security training for developers
- Use secure coding practices
- Follow principle of least privilege

---

## 🆘 Incident Response

### If Security Breach Detected:
1. **Immediately:** Disable affected user accounts
2. **Review:** Check audit logs for breach timeline
3. **Contain:** Isolate affected systems
4. **Notify:** Inform security team and compliance officer
5. **Investigate:** Determine scope and impact
6. **Remediate:** Fix vulnerability, rotate keys
7. **Document:** Complete incident report
8. **Notify:** Inform affected patients if PHI compromised (HIPAA)

---

## 📞 Contact & Support

For security concerns or questions:
- Security Team: security@hospital.example.com
- Emergency: +1-XXX-XXX-XXXX

**Remember:** Security is an ongoing process, not a one-time implementation. Regular reviews and updates are essential!

---

## Version History

- **v2.0.0** - Complete CIA Triad Implementation (December 2025)
  - Added JWT authentication & RBAC
  - Implemented audit logging
  - Added input validation
  - Created health monitoring
  - Added field encryption
  - Implemented rate limiting

- **v1.0.0** - Initial Release (Basic CRUD operations)
