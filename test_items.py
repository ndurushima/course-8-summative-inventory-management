# tests/test_items.py
import pytest
from app import app
from models import DB

@pytest.fixture(autouse=True)
def client():
    DB.clear()
    with app.test_client() as c:
        yield c

def test_create_and_get_item(client):
    r = client.post("/items", json={"name":"Tea","category":"beverage","price":2.5})
    assert r.status_code == 201
    item = r.get_json()
    r2 = client.get(f"/items/{item['id']}")
    assert r2.status_code == 200
    assert r2.get_json()["name"] == "Tea"

def test_create_missing_fields(client):
    r = client.post("/items", json={"name":"X"})
    assert r.status_code == 400
    assert "Missing required fields" in r.get_json()["error"]
