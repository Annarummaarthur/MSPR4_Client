import os
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db


@pytest.fixture(autouse=True)
def mock_api_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "testtoken")
    yield


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer testtoken"}


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
    with TestClient(app) as c:
        yield c
