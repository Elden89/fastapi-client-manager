from fastapi.testclient import TestClient
from fast import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Привет"}

def test_get_clients():
    response = client.get("/clients")
    assert response.status_code == 200

def test_get_client_not_found():
    client_id = 9999
    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 404