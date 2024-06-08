# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_student():
    response = client.post("/students/", json={"name": "John Doe", "grades": {"math": 8.0}})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_read_student():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"