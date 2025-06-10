from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API online"}

def test_get_produtores():
    response = client.get("/produtores/produtores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
