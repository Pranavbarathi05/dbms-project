#!/usr/bin/env python3
"""
Initialize Admin User Script
Creates the first admin user in the database
"""

from database import SessionLocal
from auth import get_password_hash
import models
from datetime import datetime

def create_admin_user():
    """Create initial admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if existing_admin:
            print("❌ Admin user already exists!")
            return
        
        # Create admin user
        admin_user = models.User(
            username="admin",
            email="admin@hospital.example.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: admin123")
        print("\n⚠️  IMPORTANT: Change the password immediately after first login!")
        
        # Create sample users for testing
        create_sample_users(db)
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

def create_sample_users(db):
    """Create sample users for testing"""
    sample_users = [
        {
            "username": "dr.smith",
            "email": "dr.smith@hospital.example.com",
            "full_name": "Dr. John Smith",
            "role": "doctor"
        },
        {
            "username": "nurse.jane",
            "email": "nurse.jane@hospital.example.com",
            "full_name": "Jane Doe",
            "role": "nurse"
        },
        {
            "username": "receptionist",
            "email": "reception@hospital.example.com",
            "full_name": "Sarah Johnson",
            "role": "receptionist"
        }
    ]
    
    for user_data in sample_users:
        existing_user = db.query(models.User).filter(
            models.User.username == user_data["username"]
        ).first()
        
        if not existing_user:
            user = models.User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash("admin123"),
                role=user_data["role"],
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(user)
    
    db.commit()
    print(f"\n✅ Created {len(sample_users)} sample users (all with password: admin123)")
    print("   - dr.smith (doctor)")
    print("   - nurse.jane (nurse)")
    print("   - receptionist (receptionist)")

if __name__ == "__main__":
    print("🏥 Hospital Management System - Admin Initialization")
    print("=" * 60)
    create_admin_user()
    print("=" * 60)
    print("\n📚 Next Steps:")
    print("1. Start the server: uvicorn main:app --reload")
    print("2. Login at: http://localhost:8000/docs")
    print("3. Change all default passwords immediately!")
