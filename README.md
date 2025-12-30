# 🏥 Hospital Management System with CIA Triad Security

A secure, enterprise-grade Hospital Management System implementing comprehensive security measures following the **CIA Triad** (Confidentiality, Integrity, Availability) principles.

## 🌟 Features

### Core Functionality
- Patient Management (CRUD operations)
- Doctor Management
- Appointment Scheduling
- Hospital Admissions Tracking
- Prescription Management
- Invoice & Billing System

### 🔒 Security Features (CIA Triad Implementation)

#### **Confidentiality**
- ✅ JWT-based authentication with role-based access control (RBAC)
- ✅ Password hashing using bcrypt
- ✅ Field-level encryption for sensitive data
- ✅ Comprehensive audit logging (HIPAA compliant)
- ✅ Session management with token expiration

#### **Integrity**
- ✅ Input validation using Pydantic schemas
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Data type validation and sanitization
- ✅ Foreign key constraints for referential integrity
- ✅ Audit trail for all data modifications

#### **Availability**
- ✅ Health check and monitoring endpoints
- ✅ Rate limiting (DDoS protection)
- ✅ Database connection pooling
- ✅ Auto-reconnection on connection failures
- ✅ Performance monitoring with response time tracking
- ✅ Resource usage monitoring (CPU, Memory, Disk)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL/MariaDB
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
cd /path/to/dbms-project/backend
```

2. **Run the automated setup script**
```bash
./setup.sh
```

Or manually:

3. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and security keys
```

6. **Create database**
```bash
mysql -u root -p -e "CREATE DATABASE hospital_db;"
```

7. **Initialize tables**
```bash
python3 -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

8. **Create admin user**
```bash
python3 init_admin.py
```

9. **Start the server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

10. **Access the API**
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📚 Documentation

### Security Documentation
See **[SECURITY_README.md](./SECURITY_README.md)** for comprehensive security implementation details including:
- Authentication & Authorization setup
- Audit logging system
- Data encryption guidelines
- Input validation rules
- Health monitoring setup
- Security best practices
- Production deployment checklist

### API Endpoints

#### Authentication (`/auth`)
- `POST /auth/register` - Register new user (Admin only)
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `GET /auth/users` - List users (Admin only)
- `GET /auth/audit-logs` - View audit logs (Admin only)

#### Health Monitoring (`/health`)
- `GET /health` - Basic health check
- `GET /health/detailed` - Comprehensive health report
- `GET /health/database` - Database status
- `GET /health/readiness` - Readiness probe
- `GET /health/liveness` - Liveness probe

#### Patients (`/patients`)
- `POST /patients` - Create patient (Authenticated)
- `GET /patients` - List patients (Authenticated)
- `GET /patients/{id}` - Get patient (Authenticated)
- `PUT /patients/{id}` - Update patient (Doctor/Nurse/Admin)
- `DELETE /patients/{id}` - Delete patient (Admin only)

#### Doctors (`/doctors`)
- Similar CRUD operations with role-based access

#### Appointments (`/appointments`)
- Create, read, update, delete appointments
- Role-based permissions

#### Admissions (`/admissions`)
- Hospital admission management
- Bed tracking

#### Prescriptions (`/prescriptions`)
- Medical prescriptions
- Doctor authorization required

#### Invoices (`/invoices`)
- Billing and payment tracking

## 👥 User Roles & Permissions

| Role | Patient Access | Medical Records | User Management | Delete Data |
|------|---------------|-----------------|-----------------|-------------|
| **Admin** | Full | Full | Yes | Yes |
| **Doctor** | Full | Full | No | No |
| **Nurse** | Full | Limited | No | No |
| **Receptionist** | Create/Read | No | No | No |

## 🔐 Default Credentials

After running `init_admin.py`, the following test users are created:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| dr.smith | admin123 | Doctor |
| nurse.jane | admin123 | Nurse |
| receptionist | admin123 | Receptionist |

⚠️ **IMPORTANT:** Change all default passwords immediately after first login!

## 🧪 Testing

### Test Authentication
```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Use token
curl -X GET http://localhost:8000/patients \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Test Health Checks
```bash
# Basic health
curl http://localhost:8000/health

# Detailed health
curl http://localhost:8000/health/detailed
```

### Test Rate Limiting
```bash
# Make 15 requests quickly - should get rate limited
for i in {1..15}; do curl http://localhost:8000/; done
```

## 📊 Database Schema

### Security Tables
- **users** - User accounts with roles
- **audit_logs** - Complete audit trail

### Core Tables
- **patients** - Patient information
- **doctors** - Doctor profiles
- **appointments** - Appointment scheduling
- **admissions** - Hospital admissions
- **prescriptions** - Medical prescriptions
- **invoices** - Billing information

## 🛠️ Technology Stack

- **Framework:** FastAPI
- **Database:** MySQL/MariaDB with SQLAlchemy ORM
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt
- **Encryption:** Fernet (symmetric encryption)
- **Validation:** Pydantic
- **Rate Limiting:** SlowAPI
- **Monitoring:** psutil

## 📦 Dependencies

Key dependencies (see `requirements.txt` for full list):
- fastapi - Modern web framework
- uvicorn - ASGI server
- sqlalchemy - ORM
- pymysql - MySQL connector
- python-jose - JWT implementation
- passlib - Password hashing
- cryptography - Data encryption
- slowapi - Rate limiting
- psutil - System monitoring
- pydantic - Data validation

## 🚨 Security Considerations

### For Development
- All security features are enabled by default
- Rate limiting is active (10 req/min for some endpoints)
- CORS allows all origins (restrict in production)
- Detailed error messages for debugging

### For Production
See [SECURITY_README.md](./SECURITY_README.md) for complete production checklist:
- Change all default passwords and keys
- Use environment variables for secrets
- Enable HTTPS/TLS
- Restrict CORS origins
- Set up database SSL
- Configure automated backups
- Enable monitoring alerts
- Implement log aggregation
- Regular security audits

## 📈 Monitoring & Alerts

The system provides comprehensive monitoring:
- Real-time health checks
- System resource usage (CPU, Memory, Disk)
- Database connectivity status
- Response time tracking
- Audit log analysis

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check MySQL is running
sudo systemctl status mysql

# Create database if missing
mysql -u root -p -e "CREATE DATABASE hospital_db;"
```

**Authentication Errors**
```bash
# Recreate admin user
python3 init_admin.py
```

**Module Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Rate Limit Exceeded**
- Wait 1 minute or adjust rate limits in `main.py`

## 📝 License

This project is for educational purposes - Hospital Management System with CIA Triad Security Implementation.

## 👨‍💻 Development

### Project Structure
```
backend/
├── main.py                 # FastAPI application & middleware
├── database.py            # Database configuration
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic validation schemas
├── auth.py                # Authentication utilities
├── auth_schemas.py        # Auth-specific schemas
├── encryption.py          # Encryption utilities
├── audit_helper.py        # Audit logging helper
├── init_admin.py          # Admin initialization script
├── init_admin.sql         # SQL initialization script
├── setup.sh               # Automated setup script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── routers/
    ├── auth_router.py     # Authentication endpoints
    ├── health.py          # Health monitoring endpoints
    ├── patients.py        # Patient management
    ├── doctors.py         # Doctor management
    ├── appointments.py    # Appointments
    ├── admissions.py      # Hospital admissions
    ├── prescriptions.py   # Prescriptions
    └── invoices.py        # Billing
```

## 🤝 Contributing

When contributing, ensure:
1. All security features remain enabled
2. Add audit logging for new endpoints
3. Implement proper role-based access control
4. Add input validation for new schemas
5. Update documentation
6. Test all security features

## 📞 Support

For security issues or questions, refer to [SECURITY_README.md](./SECURITY_README.md).

---

**Remember:** Security is not a feature, it's a continuous process. Regular updates and audits are essential!

## ✅ CIA Triad Summary

This project demonstrates:

### ✅ Confidentiality
- JWT authentication prevents unauthorized access
- Role-based access control limits data exposure
- Encryption protects sensitive data at rest
- Audit logging tracks all data access

### ✅ Integrity
- Input validation prevents malicious data
- SQLAlchemy ORM prevents SQL injection
- Database constraints ensure data consistency
- Audit trail verifies data modifications

### ✅ Availability
- Health monitoring ensures system uptime
- Rate limiting prevents DDoS attacks
- Connection pooling handles concurrent users
- Auto-recovery from connection failures

---

**Version:** 2.0.0 (CIA Triad Implementation)  
**Last Updated:** December 2025
