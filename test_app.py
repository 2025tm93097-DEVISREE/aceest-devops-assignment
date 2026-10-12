import pytest
from app import app, clients

@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    clients.clear()
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_programs(client):
    response = client.get("/programs")
    assert response.status_code == 200
    assert "beginner" in response.get_json()


def test_create_and_get_client(client):
    created = client.post("/clients", json={"name": "Devi", "goal": "beginner"})
    assert created.status_code == 201
    assert created.get_json()["program"] == "Full Body 3x per week"
    fetched = client.get("/clients/Devi")
    assert fetched.status_code == 200
    assert fetched.get_json()["name"] == "Devi"


def test_name_is_required(client):
    response = client.post("/clients", json={"goal": "beginner"})
    assert response.status_code == 400


def test_invalid_goal(client):
    response = client.post("/clients", json={"name": "Alex", "goal": "unknown"})
    assert response.status_code == 400


def test_duplicate_client(client):
    client.post("/clients", json={"name": "Sam", "goal": "fat-loss"})
    response = client.post("/clients", json={"name": "Sam", "goal": "fat-loss"})
    assert response.status_code == 409


def test_missing_client(client):
    assert client.get("/clients/Unknown").status_code == 404


def test_delete_client(client):
    client.post("/clients", json={"name": "Ravi", "goal": "muscle-gain"})
    assert client.delete("/clients/Ravi").status_code == 204
    assert client.get("/clients/Ravi").status_code == 404
