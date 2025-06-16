from sqlalchemy import text
from db import SessionLocal

try:
    db = SessionLocal()
    db.execute(text("SELECT 1"))
    print("✅ Connexion à la base OK")
except Exception as e:
    print("❌ Erreur de connexion :", e)
