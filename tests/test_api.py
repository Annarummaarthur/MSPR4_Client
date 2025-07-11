import os

import pytest
from unittest.mock import MagicMock

API_TOKEN = os.getenv("API_TOKEN")


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {API_TOKEN}"}


@pytest.fixture
def mock_db_session(monkeypatch):
    mock_session = MagicMock()

    from app import db as db_module

    monkeypatch.setattr(db_module, "get_db", lambda: iter([mock_session]))

    return mock_session


def test_create_client(client, auth_headers, mock_db_session):
    mock_client_instance = MagicMock()
    mock_client_instance.id = 1
    mock_client_instance.name = "Test Client"
    mock_db_session.refresh.return_value = None

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda x: x

    response = client.post(
        "/clients",
        json={
            "name": "Test Client",
            "email": "test@example.com",
            "phone": "+33123456789",
            "username": "testuser",
            "postal_code": "75000",
            "city": "Paris",
            "profile_first_name": "Test",
            "profile_last_name": "Client",
            "company_name": "TestCorp",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Client"


def test_list_clients(client, auth_headers, mock_db_session):
    # Setup the mock query.all()
    mock_client1 = MagicMock()
    mock_client1.id = 1
    mock_client1.name = "Client 1"
    mock_client2 = MagicMock()
    mock_client2.id = 2
    mock_client2.name = "Client 2"

    mock_query = MagicMock()
    mock_query.all.return_value = [mock_client1, mock_client2]
    mock_db_session.query.return_value = mock_query

    response = client.get("/clients", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_client(client, auth_headers, mock_db_session):
    mock_client = MagicMock()
    mock_client.id = 1
    mock_client.name = "Test Client"

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_client
    mock_db_session.query.return_value = mock_query

    response = client.get("/clients/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Client"


def test_update_client(client, auth_headers, mock_db_session):
    mock_client = MagicMock()
    mock_client.id = 1
    mock_client.name = "Old Name"

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_client
    mock_db_session.query.return_value = mock_query

    response = client.put(
        "/clients/1",
        json={"name": "Updated Client"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Client"


def test_delete_client(client, auth_headers, mock_db_session):
    mock_client = MagicMock()
    mock_client.id = 1
    mock_client.name = "Client to delete"

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_client
    mock_db_session.query.return_value = mock_query

    response = client.delete("/clients/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Client supprimé avec succès"
