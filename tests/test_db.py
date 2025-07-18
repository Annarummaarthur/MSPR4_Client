import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import pytest

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if os.getenv("CI") == "true" or os.getenv("TESTING") == "true":
        DATABASE_URL = "sqlite:///:memory:"
        print("Falling back to in-memory SQLite for testing.")
    else:
        pytest.skip(
            "DATABASE_URL not set. Skipping DB connection test.",
            allow_module_level=True,
        )

# Safe to initialize engine now
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM clients LIMIT 5;"))
            print("✅ Connexion réussie à la base Supabase")
            for row in result:
                print(row)
    except SQLAlchemyError as e:
        pytest.fail(f"❌ Erreur de connexion : {e}")
