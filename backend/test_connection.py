from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:@localhost/hospital_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Connected successfully:", conn)
except Exception as e:
    print("Connection failed:", e)
