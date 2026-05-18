from app import create_app
from app.routes.binary_tree import binary_tree_service


def setup_function():
    binary_tree_service.reset()


def create_test_client():
    app = create_app()
    return app.test_client()


def test_binary_tree_state_route_returns_empty_tree():
    client = create_test_client()

    response = client.get("/api/binary-tree/state")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["structure"] == "binary-tree"
    assert payload["data"]["operation"] == "state"
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["nodes"] == []
    assert payload["data"]["edges"] == []


def test_binary_tree_demo_load_route_returns_visualization_contract():
    client = create_test_client()

    response = client.post("/api/binary-tree/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["operation"] == "demo-load"
    assert payload["data"]["metrics"]["count"] == 7
    assert payload["data"]["metrics"]["edgesCount"] == 6
    assert len(payload["data"]["nodes"]) == 7
    assert len(payload["data"]["edges"]) == 6
    assert payload["data"]["result"]["root"]["value"] == 50


def test_binary_tree_insert_route_creates_root_and_children():
    client = create_test_client()

    root_response = client.post("/api/binary-tree/insert", json={"value": 50})
    left_response = client.post("/api/binary-tree/insert", json={"value": 25})
    right_response = client.post("/api/binary-tree/insert", json={"value": 75})

    assert root_response.status_code == 201
    assert left_response.status_code == 201
    assert right_response.status_code == 201
    assert right_response.get_json()["data"]["metrics"]["count"] == 3
    assert right_response.get_json()["data"]["result"]["inserted"]["value"] == 75


def test_binary_tree_insert_route_validates_required_value():
    client = create_test_client()

    response = client.post("/api/binary-tree/insert", json={})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_binary_tree_insert_route_rejects_duplicate_value():
    client = create_test_client()
    client.post("/api/binary-tree/insert", json={"value": 50})

    response = client.post("/api/binary-tree/insert", json={"value": 50})
    payload = response.get_json()

    assert response.status_code == 409
    assert payload["success"] is False
    assert payload["error"]["code"] == "DUPLICATE_KEY"


def test_binary_tree_search_route_returns_found_node_level():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.get("/api/binary-tree/search?value=40")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is True
    assert payload["data"]["result"]["node"]["value"] == 40
    assert payload["data"]["result"]["level"] == 2


def test_binary_tree_search_route_returns_not_found_result():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.get("/api/binary-tree/search?value=999")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is False
    assert payload["data"]["result"]["node"] is None


def test_binary_tree_search_route_validates_missing_query_value():
    client = create_test_client()

    response = client.get("/api/binary-tree/search")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_binary_tree_delete_route_removes_leaf_value():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.delete("/api/binary-tree/delete", json={"value": 10})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["deleted"]["value"] == 10
    assert payload["data"]["metrics"]["count"] == 6

    search_response = client.get("/api/binary-tree/search?value=10")
    assert search_response.get_json()["data"]["result"]["found"] is False


def test_binary_tree_delete_route_accepts_query_param_value():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.delete("/api/binary-tree/delete?value=90")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["count"] == 6


def test_binary_tree_delete_route_rejects_empty_tree():
    client = create_test_client()

    response = client.delete("/api/binary-tree/delete", json={"value": 50})
    payload = response.get_json()

    assert response.status_code == 422
    assert payload["success"] is False
    assert payload["error"]["code"] == "STRUCTURE_EMPTY"


def test_binary_tree_traverse_route_returns_inorder():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.get("/api/binary-tree/traverse?type=inorder")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "inorder"
    assert payload["data"]["traversal"]["order"] == [10, 25, 40, 50, 60, 75, 90]


def test_binary_tree_traverse_route_returns_default_levelorder():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.get("/api/binary-tree/traverse")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "levelorder"
    assert payload["data"]["traversal"]["order"] == [50, 25, 75, 10, 40, 60, 90]


def test_binary_tree_traverse_route_rejects_invalid_type():
    client = create_test_client()

    response = client.get("/api/binary-tree/traverse?type=dfs")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_binary_tree_metrics_route_returns_metrics_only_result():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.get("/api/binary-tree/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "metrics"
    assert payload["data"]["metrics"]["count"] == 7
    assert payload["data"]["result"]["metricsOnly"] is True


def test_binary_tree_reset_route_clears_state():
    client = create_test_client()
    client.post("/api/binary-tree/demo/load")

    response = client.post("/api/binary-tree/reset")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["result"]["reset"] is True
