def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_client(client):
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
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Client"
    global created_client_id
    created_client_id = data["id"]


def test_get_client(client):
    response = client.get(f"/clients/{created_client_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_client_id


def test_list_clients(client):
    response = client.get("/clients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_client(client):
    response = client.put(
        f"/clients/{created_client_id}",
        json={"name": "Updated Client"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Client"


def test_delete_client(client):
    response = client.delete(f"/clients/{created_client_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Client supprimé avec succès"
