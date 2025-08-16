# tests/test_items.py
import pytest
from app import app
from models import DB

@pytest.fixture(autouse=True)
def client():
    DB.clear()  # reset DB between tests
    with app.test_client() as c:
        yield c

def test_get_item_not_found(client):
    r = client.get("/items/doesnotexist")
    assert r.status_code == 404

def test_update_item_success(client):
    # create
    r = client.post("/items", json={"name":"Tea","category":"beverage","price":2.5})
    item_id = r.get_json()["id"]

    # update
    r2 = client.patch(f"/items/{item_id}", json={"price": 3.0})
    assert r2.status_code == 200
    assert r2.get_json()["price"] == 3.0

def test_delete_item_success(client):
    r = client.post("/items", json={"name":"Coffee","category":"beverage","price":4.0})
    item_id = r.get_json()["id"]

    r2 = client.delete(f"/items/{item_id}")
    assert r2.status_code == 200
    assert r2.get_json()["deleted"] == item_id

    # now it should be gone
    r3 = client.get(f"/items/{item_id}")
    assert r3.status_code == 404

def test_list_items_filter(client):
    client.post("/items", json={"name":"Tea","category":"beverage","price":2.5})
    client.post("/items", json={"name":"Apple","category":"fruit","price":1.2})

    r = client.get("/items?category=beverage")
    data = r.get_json()
    assert data["count"] == 1
    assert data["items"][0]["category"] == "beverage"
