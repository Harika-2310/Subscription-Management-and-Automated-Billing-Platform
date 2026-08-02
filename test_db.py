from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:vani03106@localhost:5432/subscription_db"

try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("✅ Connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)