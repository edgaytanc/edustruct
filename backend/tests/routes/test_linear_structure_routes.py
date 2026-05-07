import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        test_client.post("/api/list/reset")
        test_client.post("/api/stack/reset")
        test_client.post("/api/queue/reset")
        yield test_client


def test_list_insert_state_search_and_delete(client):
    insert_response = client.post("/api/list/insert", json={"value": "MAT101"})
    assert insert_response.status_code == 201

    state_response = client.get("/api/list/state")
    assert state_response.status_code == 200
    assert state_response.get_json()["data"]["result"]["items"] == ["MAT101"]

    search_response = client.get("/api/list/search?value=MAT101")
    assert search_response.status_code == 200
    assert search_response.get_json()["data"]["result"]["found"] is True

    delete_response = client.delete("/api/list/delete", json={"value": "MAT101"})
    assert delete_response.status_code == 200
    assert delete_response.get_json()["data"]["result"]["items"] == []


def test_stack_insert_peek_and_delete(client):
    client.post("/api/stack/insert", json={"value": "Dashboard"})
    client.post("/api/stack/insert", json={"value": "Curso"})

    peek_response = client.get("/api/stack/peek")
    assert peek_response.status_code == 200
    assert peek_response.get_json()["data"]["result"]["peek"] == "Curso"

    delete_response = client.delete("/api/stack/delete")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["data"]["result"]["popped"] == "Curso"


def test_queue_insert_front_and_delete(client):
    client.post("/api/queue/insert", json={"value": "Turno 1"})
    client.post("/api/queue/insert", json={"value": "Turno 2"})

    front_response = client.get("/api/queue/front")
    assert front_response.status_code == 200
    assert front_response.get_json()["data"]["result"]["front"] == "Turno 1"

    delete_response = client.delete("/api/queue/delete")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["data"]["result"]["dequeued"] == "Turno 1"


def test_missing_value_returns_validation_error(client):
    response = client.post("/api/list/insert", json={})

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_empty_stack_delete_returns_structure_empty_error(client):
    response = client.delete("/api/stack/delete")

    assert response.status_code == 422
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "STRUCTURE_EMPTY"
