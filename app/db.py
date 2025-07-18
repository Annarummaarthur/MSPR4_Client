import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Allow fallback for CI/test environments
    if os.getenv("CI") == "true" or os.getenv("TESTING") == "true":
        DATABASE_URL = "sqlite:///:memory:"  # In-memory DB just for import safety
    else:
        raise RuntimeError(
            "❌ DATABASE_URL is not set. Add it to your .env or CI secrets."
        )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
