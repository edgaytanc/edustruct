from app import create_app
from app.routes.tree import tree_service


def setup_function():
    tree_service.reset()


def create_test_client():
    app = create_app()
    return app.test_client()


def test_tree_state_route_returns_empty_tree():
    client = create_test_client()

    response = client.get("/api/tree/state")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["operation"] == "state"
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["nodes"] == []
    assert payload["data"]["edges"] == []


def test_tree_demo_load_route_returns_visualization():
    client = create_test_client()

    response = client.post("/api/tree/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["metrics"]["count"] == 8
    assert len(payload["data"]["nodes"]) == 8
    assert len(payload["data"]["edges"]) == 7


def test_tree_insert_route_creates_root_and_child():
    client = create_test_client()

    root_response = client.post(
        "/api/tree/insert",
        json={"id": "faculty", "label": "Facultad", "category": "faculty"},
    )
    child_response = client.post(
        "/api/tree/insert",
        json={"id": "career", "label": "Carrera", "parentId": "faculty", "category": "career"},
    )

    assert root_response.status_code == 201
    assert child_response.status_code == 201
    assert child_response.get_json()["data"]["metrics"]["count"] == 2
    assert child_response.get_json()["data"]["result"]["inserted"]["id"] == "career"


def test_tree_insert_route_validates_required_id():
    client = create_test_client()

    response = client.post("/api/tree/insert", json={"label": "Sin id"})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_tree_insert_route_rejects_duplicate_id():
    client = create_test_client()
    client.post("/api/tree/insert", json={"id": "faculty", "label": "Facultad"})

    response = client.post(
        "/api/tree/insert",
        json={"id": "faculty", "label": "Facultad repetida", "parentId": "faculty"},
    )
    payload = response.get_json()

    assert response.status_code == 409
    assert payload["success"] is False
    assert payload["error"]["code"] == "DUPLICATE_KEY"


def test_tree_search_route_returns_node_level():
    client = create_test_client()
    client.post("/api/tree/demo/load")

    response = client.get("/api/tree/search?id=math-1")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is True
    assert payload["data"]["result"]["level"] == 3


def test_tree_search_route_validates_missing_query_id():
    client = create_test_client()

    response = client.get("/api/tree/search")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_tree_delete_route_removes_node_and_subtree():
    client = create_test_client()
    client.post("/api/tree/demo/load")

    response = client.delete("/api/tree/delete", json={"id": "cycle-1"})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["deleted"]["id"] == "cycle-1"
    assert payload["data"]["metrics"]["count"] == 5

    search_response = client.get("/api/tree/search?id=math-1")
    assert search_response.get_json()["data"]["result"]["found"] is False


def test_tree_delete_route_accepts_query_param_id():
    client = create_test_client()
    client.post("/api/tree/demo/load")

    response = client.delete("/api/tree/delete?id=math-2")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["count"] == 7


def test_tree_delete_route_rejects_empty_tree():
    client = create_test_client()

    response = client.delete("/api/tree/delete", json={"id": "faculty"})
    payload = response.get_json()

    assert response.status_code == 422
    assert payload["success"] is False
    assert payload["error"]["code"] == "STRUCTURE_EMPTY"


def test_tree_traverse_route_returns_preorder():
    client = create_test_client()
    client.post("/api/tree/demo/load")

    response = client.get("/api/tree/traverse?type=preorder")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "preorder"
    assert payload["data"]["traversal"]["order"][0] == "faculty-engineering"


def test_tree_traverse_route_rejects_invalid_type():
    client = create_test_client()

    response = client.get("/api/tree/traverse?type=inorder")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_tree_metrics_route_returns_metrics_only_result():
    client = create_test_client()
    client.post("/api/tree/demo/load")

    response = client.get("/api/tree/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "metrics"
    assert payload["data"]["metrics"]["count"] == 8
    assert payload["data"]["result"]["metricsOnly"] is True


def test_tree_reset_route_clears_state():
    client = create_test_client()
    client.post("/api/tree/demo/load")

    response = client.post("/api/tree/reset")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["result"]["reset"] is True
