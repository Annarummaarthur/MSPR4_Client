# tests/test_clients.py


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_create_and_get_client(client, auth_headers):
    data = {"name": "Jean Dupont"}
    response = client.post("/clients", json=data, headers=auth_headers)
    assert response.status_code == 200
    client_id = response.json()["id"]

    response = client.get(f"/clients/{client_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Jean Dupont"
