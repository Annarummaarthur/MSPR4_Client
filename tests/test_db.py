import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db import engine, Base


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM clients LIMIT 5;"))
            assert isinstance(result.fetchall(), list)
    except SQLAlchemyError as e:
        pytest.fail(f"❌ Erreur de connexion : {e}")
