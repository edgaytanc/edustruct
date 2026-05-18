from app import create_app
from app.routes.avl import avl_service


def setup_function():
    avl_service.reset()


def create_test_client():
    app = create_app()
    return app.test_client()


def test_avl_state_route_returns_empty_tree():
    client = create_test_client()

    response = client.get("/api/avl/state")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["structure"] == "avl"
    assert payload["data"]["operation"] == "state"
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["metrics"]["height"] == 0
    assert payload["data"]["nodes"] == []
    assert payload["data"]["edges"] == []


def test_avl_insert_route_applies_ll_rotation():
    client = create_test_client()

    client.post("/api/avl/insert", json={"value": 30})
    client.post("/api/avl/insert", json={"value": 20})
    response = client.post("/api/avl/insert", json={"value": 10})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["metrics"]["count"] == 3
    assert payload["data"]["metrics"]["isBalanced"] is True
    assert payload["data"]["result"]["root"]["value"] == 20
    assert payload["data"]["result"]["lastRotation"]["type"] == "LL"
    assert payload["data"]["result"]["lastRotation"]["pivot"] == 30
    assert payload["data"]["result"]["before"] is not None
    assert payload["data"]["result"]["after"] is not None


def test_avl_insert_route_applies_rr_rotation():
    client = create_test_client()

    client.post("/api/avl/insert", json={"value": 10})
    client.post("/api/avl/insert", json={"value": 20})
    response = client.post("/api/avl/insert", json={"value": 30})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["result"]["root"]["value"] == 20
    assert payload["data"]["result"]["lastRotation"]["type"] == "RR"
    assert payload["data"]["metrics"]["height"] == 1


def test_avl_insert_route_applies_lr_rotation():
    client = create_test_client()

    client.post("/api/avl/insert", json={"value": 30})
    client.post("/api/avl/insert", json={"value": 10})
    response = client.post("/api/avl/insert", json={"value": 20})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["result"]["root"]["value"] == 20
    assert payload["data"]["result"]["lastRotation"]["type"] == "LR"


def test_avl_insert_route_applies_rl_rotation():
    client = create_test_client()

    client.post("/api/avl/insert", json={"value": 10})
    client.post("/api/avl/insert", json={"value": 30})
    response = client.post("/api/avl/insert", json={"value": 20})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["result"]["root"]["value"] == 20
    assert payload["data"]["result"]["lastRotation"]["type"] == "RL"


def test_avl_insert_route_validates_required_value():
    client = create_test_client()

    response = client.post("/api/avl/insert", json={})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_avl_insert_route_rejects_duplicate_value():
    client = create_test_client()
    client.post("/api/avl/insert", json={"value": 50})

    response = client.post("/api/avl/insert", json={"value": 50})
    payload = response.get_json()

    assert response.status_code == 409
    assert payload["success"] is False
    assert payload["error"]["code"] == "DUPLICATE_KEY"


def test_avl_demo_load_route_returns_visualization_and_rotations():
    client = create_test_client()

    response = client.post("/api/avl/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["operation"] == "demo-load"
    assert payload["data"]["metrics"]["count"] == 7
    assert payload["data"]["metrics"]["edgesCount"] == 6
    assert payload["data"]["metrics"]["isBalanced"] is True
    assert len(payload["data"]["nodes"]) == 7
    assert len(payload["data"]["edges"]) == 6
    assert payload["data"]["result"]["lastRotation"] is not None
    assert payload["data"]["result"]["context"] == "Árbol AVL de búsqueda eficiente por ID académico"


def test_avl_search_route_returns_found_node_level():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.get("/api/avl/search?value=40")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is True
    assert payload["data"]["result"]["node"]["value"] == 40
    assert isinstance(payload["data"]["result"]["level"], int)


def test_avl_search_route_returns_not_found_result():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.get("/api/avl/search?value=999")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is False
    assert payload["data"]["result"]["node"] is None


def test_avl_search_route_validates_missing_query_value():
    client = create_test_client()

    response = client.get("/api/avl/search")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_avl_delete_route_removes_value_and_keeps_tree_balanced():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.delete("/api/avl/delete", json={"value": 10})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["deleted"]["value"] == 10
    assert payload["data"]["metrics"]["count"] == 6
    assert payload["data"]["metrics"]["isBalanced"] is True

    search_response = client.get("/api/avl/search?value=10")
    assert search_response.get_json()["data"]["result"]["found"] is False


def test_avl_delete_route_accepts_query_param_value():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.delete("/api/avl/delete?value=50")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["deleted"]["value"] == 50
    assert payload["data"]["metrics"]["count"] == 6


def test_avl_delete_route_rejects_empty_tree():
    client = create_test_client()

    response = client.delete("/api/avl/delete", json={"value": 50})
    payload = response.get_json()

    assert response.status_code == 422
    assert payload["success"] is False
    assert payload["error"]["code"] == "STRUCTURE_EMPTY"


def test_avl_delete_route_returns_not_found_for_missing_value():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.delete("/api/avl/delete", json={"value": 999})
    payload = response.get_json()

    assert response.status_code == 404
    assert payload["success"] is False
    assert payload["error"]["code"] == "NOT_FOUND"


def test_avl_traverse_route_returns_inorder_sorted_values():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.get("/api/avl/traverse?type=inorder")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "inorder"
    assert payload["data"]["traversal"]["order"] == [10, 20, 25, 27, 30, 40, 50]


def test_avl_traverse_route_returns_default_levelorder():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.get("/api/avl/traverse")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "levelorder"
    assert payload["data"]["traversal"]["order"][0] == payload["data"]["result"]["root"]["value"]


def test_avl_traverse_route_rejects_invalid_type():
    client = create_test_client()

    response = client.get("/api/avl/traverse?type=dfs")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_avl_metrics_route_returns_metrics_only_result():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.get("/api/avl/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "metrics"
    assert payload["data"]["metrics"]["count"] == 7
    assert payload["data"]["metrics"]["isBalanced"] is True
    assert payload["data"]["result"]["metricsOnly"] is True


def test_avl_reset_route_clears_state():
    client = create_test_client()
    client.post("/api/avl/demo/load")

    response = client.post("/api/avl/reset")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["nodes"] == []
    assert payload["data"]["result"]["reset"] is True
