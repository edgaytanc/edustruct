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


def test_list_courses_endpoint_returns_dataset_courses(client):
    response = client.get("/api/list/courses")

    assert response.status_code == 200
    body = response.get_json()
    result = body["data"]["result"]

    assert result["count"] >= 2
    assert result["courses"][0]["courseId"]
    assert result["courses"][0]["studentsCount"] >= 1


def test_list_load_course_endpoint_builds_real_enrollment_list(client):
    response = client.post("/api/list/demo/load-course", json={"courseId": "CUR-013"})

    assert response.status_code == 200
    body = response.get_json()
    result = body["data"]["result"]

    assert result["courseId"] == "CUR-013"
    assert result["size"] == 3
    assert result["items"] == [
        "2024001 - Ana López",
        "2024002 - Carlos Pérez",
        "2024003 - María García",
    ]
    assert body["data"]["metrics"]["count"] == 3


def test_list_load_course_endpoint_returns_not_found_for_unknown_course(client):
    response = client.post("/api/list/demo/load-course", json={"courseId": "CUR-999"})

    assert response.status_code == 404
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "NOT_FOUND"


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


def test_queue_advisory_turns_endpoint_returns_real_dataset(client):
    response = client.get("/api/queue/advisory-turns")

    assert response.status_code == 200
    body = response.get_json()
    result = body["data"]["result"]

    assert result["count"] == 4
    assert result["turns"][0]["id"] == "TURN-001"
    assert result["turns"][0]["studentName"] == "Ana López"
    assert result["turns"][0]["reason"] == "Asignación de curso"


def test_queue_load_advisory_endpoint_builds_fifo_queue(client):
    response = client.post("/api/queue/demo/load-advisory")

    assert response.status_code == 200
    body = response.get_json()
    result = body["data"]["result"]

    assert result["size"] == 4
    assert result["queuePolicy"] == "FIFO"
    assert result["front"].startswith("TURN-001 - 2024001 - Ana López")
    assert result["rear"].startswith("TURN-004 - 2024004 - Luis Ramírez")
    assert body["data"]["metrics"]["count"] == 4


def test_stack_load_history_endpoint_builds_contextual_stack(client):
    response = client.post("/api/stack/demo/load-history")

    assert response.status_code == 200
    body = response.get_json()
    result = body["data"]["result"]

    assert result["size"] == 5
    assert result["navigationPolicy"] == "LIFO"
    assert result["top"] == "Expediente Estudiantil"
    assert result["items"][0] == "Expediente Estudiantil"
    assert body["data"]["metrics"]["count"] == 5


def test_stack_navigation_push_and_back_endpoints(client):
    push_response = client.post(
        "/api/stack/navigation/push",
        json={"module": "Dashboard Académico"},
    )
    assert push_response.status_code == 201
    assert push_response.get_json()["data"]["result"]["top"] == "Dashboard Académico"

    second_push_response = client.post(
        "/api/stack/navigation/push",
        json={"module": "Curso CUR-013"},
    )
    assert second_push_response.status_code == 201
    assert second_push_response.get_json()["data"]["result"]["top"] == "Curso CUR-013"

    back_response = client.delete("/api/stack/navigation/back")
    assert back_response.status_code == 200
    result = back_response.get_json()["data"]["result"]
    assert result["backFrom"] == "Curso CUR-013"
    assert result["currentModule"] == "Dashboard Académico"


def test_stack_navigation_push_requires_module(client):
    response = client.post("/api/stack/navigation/push", json={})

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


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
