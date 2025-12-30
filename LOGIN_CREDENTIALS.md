# 🔐 Login Credentials - Hospital Management System

## Access the System
**Frontend URL**: http://localhost:8080/login.html  
**API Documentation**: http://localhost:8000/docs

---

## 👥 User Accounts

### 1. ADMIN (Full System Access)
```
Username: admin
Password: admin123
Role: Administrator
```

**Permissions:**
- ✅ View/Add/Edit/Delete Patients
- ✅ View/Add/Edit/Delete Doctors
- ✅ Manage all appointments, admissions, prescriptions, invoices
- ✅ Create and manage users
- ✅ View audit logs
- ✅ Full system access

---

### 2. DOCTOR
```
Username: dr.smith
Password: doctor123
Role: Doctor
```

**Permissions:**
- ✅ View/Add/Edit Patients
- ✅ View Doctors
- ✅ Create and manage prescriptions
- ✅ Manage appointments
- ✅ Manage admissions
- ✅ Create invoices
- ❌ Cannot delete patients
- ❌ Cannot manage users
- ❌ Cannot view audit logs

---

### 3. NURSE
```
Username: nurse.jane
Password: nurse123
Role: Nurse
```

**Permissions:**
- ✅ View/Add/Edit Patients
- ✅ View Doctors
- ✅ Manage admissions
- ✅ Manage appointments
- ✅ Manage invoices
- ❌ Cannot create prescriptions
- ❌ Cannot delete patients
- ❌ Cannot manage users
- ❌ Cannot view audit logs

---

### 4. RECEPTIONIST
```
Username: receptionist
Password: reception123
Role: Receptionist
```

**Permissions:**
- ✅ View/Add Patients
- ✅ View Doctors
- ✅ Schedule appointments
- ✅ Manage invoices
- ❌ Cannot edit patients
- ❌ Cannot delete patients
- ❌ Cannot create prescriptions
- ❌ Cannot manage admissions
- ❌ Cannot manage users
- ❌ Cannot view audit logs

---

## 🚀 How to Login

1. **Start the frontend server** (if not running):
   ```bash
   cd /home/pranav/Downloads/dbms-project/frontend
   python3 -m http.server 8080
   ```

2. **Open your browser** to: http://localhost:8080/login.html

3. **Enter credentials** from the list above

4. **You'll be redirected** to the dashboard after successful login

---

## 🔒 Security Features

All user sessions are secured with:
- JWT token authentication (8-hour expiry)
- Password hashing with bcrypt
- Role-based access control
- Audit logging of all actions
- IP address tracking
- Session management

---

## 🔄 Changing Passwords

To change a user's password, login as **admin** and use the user management features, or contact the system administrator.

---

## 📊 Testing Different Roles

1. **Test as Admin**: Login with admin credentials - you'll have full access to all features
2. **Test as Doctor**: Login with dr.smith - notice you can't delete patients or manage users
3. **Test as Nurse**: Login with nurse.jane - notice you can't create prescriptions
4. **Test as Receptionist**: Login with receptionist - notice limited edit capabilities

---

## 🐛 Troubleshooting

### Can't Login?
- Check if backend server is running on port 8000
- Check if frontend is running on port 8080
- Verify username/password (case-sensitive)
- Check browser console for errors (F12)

### Server Not Running?
```bash
# Backend
cd /home/pranav/Downloads/dbms-project/backend
/home/pranav/Downloads/dbms-project/backend/venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0

# Frontend (in new terminal)
cd /home/pranav/Downloads/dbms-project/frontend
python3 -m http.server 8080
```

### Forgot Password?
Run this script to reset admin password:
```bash
cd /home/pranav/Downloads/dbms-project/backend
python3 << 'EOF'
from database import SessionLocal
from auth import get_password_hash
import models

db = SessionLocal()
user = db.query(models.User).filter(models.User.username == "admin").first()
user.hashed_password = get_password_hash("admin123")
db.commit()
print("Admin password reset to: admin123")
db.close()
EOF
```

---

## 📝 Notes

- All passwords are hashed and securely stored
- Each login attempt is logged in the audit trail
- Failed login attempts are tracked
- Tokens expire after 8 hours of inactivity
- All API requests require authentication

---

**Last Updated**: December 30, 2025  
**System Status**: ✅ Operational
