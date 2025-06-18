import os
import pytest

API_TOKEN = os.getenv("API_TOKEN")


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {API_TOKEN}"}


@pytest.fixture
def created_client_id(client, auth_headers):
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
    return response.json()["id"]


def test_create_client(client, auth_headers):
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
    data = response.json()
    assert data["name"] == "Test Client"


def test_get_client(client, auth_headers, created_client_id):
    response = client.get(f"/clients/{created_client_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Client"


def test_list_clients(client, auth_headers):  # <- fix: added auth_headers
    response = client.get("/clients", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_client(client, auth_headers, created_client_id):
    response = client.put(
        f"/clients/{created_client_id}",
        json={"name": "Updated Client"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Client"


def test_delete_client(client, auth_headers, created_client_id):
    response = client.delete(f"/clients/{created_client_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Client supprimé avec succès"
