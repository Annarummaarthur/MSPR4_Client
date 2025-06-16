import pytest
from fastapi.testclient import TestClient
from main import app
import os

API_TOKEN = os.getenv("API_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

client = TestClient(app)

def test_create_client():
    response = client.post(
        "/clients",
        headers=HEADERS,
        json={
            "name": "Test Client",
            "email": "test@example.com",
            "phone": "+33123456789",
            "username": "testuser",
            "postal_code": "75000",
            "city": "Paris",
            "profile_first_name": "Test",
            "profile_last_name": "Client",
            "company_name": "TestCorp"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Client"
    global created_client_id
    created_client_id = data["id"]

def test_get_client():
    response = client.get(f"/clients/{created_client_id}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_client_id

def test_list_clients():
    response = client.get("/clients", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_client():
    response = client.put(
        f"/clients/{created_client_id}",
        headers=HEADERS,
        json={"name": "Updated Client"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Client"

def test_delete_client():
    response = client.delete(f"/clients/{created_client_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["message"] == "Client supprimé avec succès"

def test_protected_route_without_token():
    response = client.get("/clients")
    assert response.status_code == 403
