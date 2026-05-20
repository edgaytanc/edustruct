from app import create_app
from app.routes.btree import btree_service


def setup_function():
    btree_service.configure(4)


def create_test_client():
    app = create_app()
    return app.test_client()


def test_btree_state_route_returns_empty_tree():
    client = create_test_client()

    response = client.get("/api/btree/state")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["structure"] == "btree"
    assert payload["data"]["operation"] == "state"
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["metrics"]["height"] == 0
    assert payload["data"]["metrics"]["levels"] == 0
    assert payload["data"]["nodes"] == []
    assert payload["data"]["edges"] == []


def test_btree_configure_route_sets_order_and_resets_tree():
    client = create_test_client()
    client.post("/api/btree/insert", json={"key": 2024008})

    response = client.post("/api/btree/configure", json={"order": 5})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "configure"
    assert payload["data"]["metrics"]["order"] == 5
    assert payload["data"]["metrics"]["maxKeys"] == 4
    assert payload["data"]["metrics"]["minKeys"] == 2
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["result"]["configured"] is True


def test_btree_configure_route_accepts_order_query_param():
    client = create_test_client()

    response = client.post("/api/btree/configure?order=6")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["order"] == 6


def test_btree_configure_route_rejects_invalid_order():
    client = create_test_client()

    response = client.post("/api/btree/configure", json={"order": 2})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_btree_insert_route_creates_root_node():
    client = create_test_client()

    response = client.post("/api/btree/insert", json={"key": 2024008})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "insert"
    assert payload["data"]["metrics"]["count"] == 1
    assert payload["data"]["metrics"]["isValid"] is True
    assert payload["data"]["result"]["root"]["keys"] == [2024008]
    assert payload["data"]["result"]["splitOccurred"] is False
    assert len(payload["data"]["nodes"]) == 1


def test_btree_insert_route_reports_split_event():
    client = create_test_client()
    client.post("/api/btree/insert", json={"key": 10})
    client.post("/api/btree/insert", json={"key": 20})
    client.post("/api/btree/insert", json={"key": 30})

    response = client.post("/api/btree/insert", json={"key": 40})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["metrics"]["count"] == 4
    assert payload["data"]["result"]["root"]["keys"] == [30]
    assert payload["data"]["result"]["splitOccurred"] is True
    assert payload["data"]["result"]["lastSplit"]["type"] == "SPLIT"
    assert payload["data"]["result"]["lastSplit"]["promotedKey"] == 30
    assert payload["data"]["result"]["before"] is not None
    assert payload["data"]["result"]["after"] is not None


def test_btree_insert_route_validates_required_key():
    client = create_test_client()

    response = client.post("/api/btree/insert", json={})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_btree_insert_route_rejects_duplicate_key():
    client = create_test_client()
    client.post("/api/btree/insert", json={"key": 50})

    response = client.post("/api/btree/insert", json={"key": 50})
    payload = response.get_json()

    assert response.status_code == 409
    assert payload["success"] is False
    assert payload["error"]["code"] == "DUPLICATE_KEY"


def test_btree_bulk_insert_route_adds_multiple_keys():
    client = create_test_client()

    response = client.post("/api/btree/bulk-insert", json={"keys": [40, 20, 60, 10, 30, 50, 70]})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "bulk-insert"
    assert payload["data"]["metrics"]["count"] == 7
    assert payload["data"]["metrics"]["isValid"] is True
    assert payload["data"]["result"]["inserted"] == [40, 20, 60, 10, 30, 50, 70]
    assert payload["data"]["result"]["splitOccurred"] is True


def test_btree_insert_route_accepts_keys_alias_for_bulk_insert():
    client = create_test_client()

    response = client.post("/api/btree/insert", json={"keys": [15, 5, 25]})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "bulk-insert"
    assert payload["data"]["metrics"]["count"] == 3


def test_btree_bulk_insert_route_rejects_non_list_payload():
    client = create_test_client()

    response = client.post("/api/btree/bulk-insert", json={"keys": "10,20"})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_btree_demo_load_route_returns_visualization_and_split_history():
    client = create_test_client()

    response = client.post("/api/btree/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["operation"] == "demo-load"
    assert payload["data"]["metrics"]["count"] == 11
    assert payload["data"]["metrics"]["height"] >= 1
    assert payload["data"]["metrics"]["levels"] == payload["data"]["metrics"]["height"] + 1
    assert payload["data"]["metrics"]["edgesCount"] == len(payload["data"]["edges"])
    assert payload["data"]["result"]["context"] == "Árbol B como índice académico de expedientes universitarios"
    assert len(payload["data"]["result"]["splitEvents"]) > 0


def test_btree_search_route_returns_found_node_level_and_path():
    client = create_test_client()
    client.post("/api/btree/demo/load")

    response = client.get("/api/btree/search?key=2024048")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "search"
    assert payload["data"]["result"]["found"] is True
    assert 2024048 in payload["data"]["result"]["node"]["keys"]
    assert isinstance(payload["data"]["result"]["level"], int)
    assert len(payload["data"]["result"]["path"]) >= 1


def test_btree_search_route_returns_not_found_result():
    client = create_test_client()
    client.post("/api/btree/demo/load")

    response = client.get("/api/btree/search?key=9999999")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is False
    assert payload["data"]["result"]["node"] is None
    assert payload["data"]["result"]["level"] is None


def test_btree_search_route_validates_missing_key():
    client = create_test_client()

    response = client.get("/api/btree/search")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_btree_traverse_route_returns_inorder_sorted_keys():
    client = create_test_client()
    client.post("/api/btree/bulk-insert", json={"keys": [30, 10, 50, 20, 40]})

    response = client.get("/api/btree/traverse?type=inorder")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "inorder"
    assert payload["data"]["traversal"]["order"] == [10, 20, 30, 40, 50]


def test_btree_traverse_route_returns_default_levelorder():
    client = create_test_client()
    client.post("/api/btree/demo/load")

    response = client.get("/api/btree/traverse")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "levelorder"
    assert payload["data"]["traversal"]["order"][0] == payload["data"]["result"]["root"]["keys"]
    assert len(payload["data"]["traversal"]["steps"]) == payload["data"]["metrics"]["nodeCount"]


def test_btree_traverse_route_rejects_invalid_type():
    client = create_test_client()

    response = client.get("/api/btree/traverse?type=preorder")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_btree_metrics_route_returns_metrics_only_result():
    client = create_test_client()
    client.post("/api/btree/demo/load")

    response = client.get("/api/btree/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "metrics"
    assert payload["data"]["metrics"]["count"] == 11
    assert payload["data"]["result"]["metricsOnly"] is True


def test_btree_reset_route_clears_state_and_keeps_configured_order():
    client = create_test_client()
    client.post("/api/btree/configure", json={"order": 5})
    client.post("/api/btree/demo/load")

    response = client.post("/api/btree/reset")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["metrics"]["order"] == 5
    assert payload["data"]["result"]["reset"] is True
    assert payload["data"]["nodes"] == []
    assert payload["data"]["edges"] == []
