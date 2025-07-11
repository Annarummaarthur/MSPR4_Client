import os

import pytest
from unittest.mock import MagicMock
from app.db import get_db
from app.main import app

API_TOKEN = os.getenv("API_TOKEN")


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {API_TOKEN}"}


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture(autouse=True)
def override_get_db(mock_db_session):
    def _get_db_override():
        yield mock_db_session

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c
