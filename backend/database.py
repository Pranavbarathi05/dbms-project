from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# IMPORTANT: If your XAMPP MySQL root has NO password use this:
DATABASE_URL = "mysql+pymysql://root:@localhost/hospital_db"

# If you set a password, use:
# DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost/hospital_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Auto-reconnect
    pool_size=20,         # Handles many queries
    max_overflow=30
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
