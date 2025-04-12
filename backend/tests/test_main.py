from fastapi.testclient import TestClient
from backend.__init__ import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_todo():
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"

def test_read_todo():
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert "title" in response.json()

def test_update_todo():
    response = client.put("/todos/1", json={"title": "Updated Todo", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"

def test_delete_todo():
    response = client.delete("/todos/1")
    assert response.status_code == 204
    response = client.get("/todos/1")
    assert response.status_code == 404

def test_read_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)