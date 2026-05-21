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


def test_list_state_response_includes_nodes_edges_and_metrics(client):
    client.post("/api/list/insert", json={"value": "MAT101"})

    response = client.get("/api/list/state")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["nodes"][0]["data"]["label"] == "HEAD"
    assert body["data"]["nodes"][-1]["data"]["label"] == "TAIL"
    assert body["data"]["metrics"]["count"] == 1
    assert body["data"]["metrics"]["edgesCount"] == 2


def test_stack_state_response_includes_visual_top_marker(client):
    client.post("/api/stack/insert", json={"value": "Dashboard"})

    response = client.get("/api/stack/state")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["nodes"][0]["data"]["label"] == "TOP"
    assert body["data"]["metrics"]["count"] == 1
    assert body["data"]["metrics"]["edgesCount"] == 1


def test_queue_state_response_includes_front_rear_markers(client):
    client.post("/api/queue/insert", json={"value": "Turno 1"})

    response = client.get("/api/queue/state")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["nodes"][0]["data"]["label"] == "FRONT"
    assert body["data"]["nodes"][-1]["data"]["label"] == "REAR"
    assert body["data"]["metrics"]["count"] == 1
    assert body["data"]["metrics"]["edgesCount"] == 2


def test_queue_advisory_demo_response_includes_front_rear_markers(client):
    response = client.post("/api/queue/demo/load-advisory")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["nodes"][0]["data"]["label"] == "FRONT"
    assert body["data"]["nodes"][1]["data"]["label"].startswith("TURN-001")
    assert body["data"]["nodes"][-1]["data"]["label"] == "REAR"
    assert body["data"]["metrics"]["count"] == 4
    assert body["data"]["metrics"]["edgesCount"] == 5


def test_stack_history_demo_response_includes_top_marker(client):
    response = client.post("/api/stack/demo/load-history")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["nodes"][0]["data"]["label"] == "TOP"
    assert body["data"]["nodes"][1]["data"]["label"] == "Expediente Estudiantil"
    assert body["data"]["metrics"]["count"] == 5
    assert body["data"]["metrics"]["edgesCount"] == 5
