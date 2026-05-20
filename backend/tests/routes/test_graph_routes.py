from app import create_app
from app.routes.graph import graph_service


def setup_function():
    graph_service.reset()


def create_test_client():
    app = create_app()
    return app.test_client()


def test_graph_state_route_returns_empty_graph_contract():
    client = create_test_client()

    response = client.get("/api/graph/state")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["structure"] == "graph"
    assert payload["data"]["operation"] == "state"
    assert payload["data"]["nodes"] == []
    assert payload["data"]["edges"] == []
    assert payload["data"]["metrics"]["verticesCount"] == 0
    assert payload["data"]["metrics"]["edgesCount"] == 0
    assert payload["data"]["result"]["isEmpty"] is True


def test_graph_add_node_route_creates_course_node():
    client = create_test_client()

    response = client.post(
        "/api/graph/nodes",
        json={"id": "CUR-001", "value": {"code": "SIS-101", "name": "Introducción a Sistemas"}},
    )
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "add-node"
    assert payload["data"]["metrics"]["verticesCount"] == 1
    assert payload["data"]["result"]["node"]["id"] == "CUR-001"
    assert payload["data"]["nodes"][0]["id"] == "CUR-001"


def test_graph_insert_route_accepts_node_alias():
    client = create_test_client()

    response = client.post("/api/graph/insert", json={"nodeId": "CUR-002", "value": {"name": "Lógica"}})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "add-node"
    assert payload["data"]["result"]["node"]["id"] == "CUR-002"


def test_graph_add_node_route_rejects_duplicate_node():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "CUR-001"})

    response = client.post("/api/graph/nodes", json={"id": "CUR-001"})
    payload = response.get_json()

    assert response.status_code == 409
    assert payload["success"] is False
    assert payload["error"]["code"] == "DUPLICATE_KEY"


def test_graph_add_node_route_validates_required_id():
    client = create_test_client()

    response = client.post("/api/graph/nodes", json={"value": {"name": "Sin id"}})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_graph_add_edge_route_creates_directed_prerequisite_relation():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "CUR-001"})
    client.post("/api/graph/nodes", json={"id": "CUR-005"})

    response = client.post("/api/graph/edges", json={"source": "CUR-001", "target": "CUR-005"})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "add-edge"
    assert payload["data"]["metrics"]["edgesCount"] == 1
    assert payload["data"]["metrics"]["maxOutDegree"] == 1
    assert payload["data"]["result"]["edge"] == {"source": "CUR-001", "target": "CUR-005"}
    assert payload["data"]["edges"][0]["source"] == "CUR-001"
    assert payload["data"]["edges"][0]["target"] == "CUR-005"


def test_graph_insert_route_accepts_edge_aliases():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "CUR-001"})
    client.post("/api/graph/nodes", json={"id": "CUR-005"})

    response = client.post("/api/graph/insert", json={"prerequisiteId": "CUR-001", "courseId": "CUR-005"})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "add-edge"
    assert payload["data"]["result"]["edge"] == {"source": "CUR-001", "target": "CUR-005"}


def test_graph_add_edge_route_rejects_missing_target_node():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "CUR-001"})

    response = client.post("/api/graph/edges", json={"source": "CUR-001", "target": "CUR-999"})
    payload = response.get_json()

    assert response.status_code == 404
    assert payload["success"] is False
    assert payload["error"]["code"] == "NOT_FOUND"


def test_graph_search_route_returns_found_and_not_found_results():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "CUR-001", "value": {"name": "Programación I"}})

    found_response = client.get("/api/graph/search?id=CUR-001")
    missing_response = client.get("/api/graph/search?id=CUR-404")
    found_payload = found_response.get_json()
    missing_payload = missing_response.get_json()

    assert found_response.status_code == 200
    assert found_payload["data"]["result"]["found"] is True
    assert found_payload["data"]["result"]["node"]["id"] == "CUR-001"
    assert missing_response.status_code == 200
    assert missing_payload["data"]["result"]["found"] is False
    assert missing_payload["data"]["result"]["node"] is None


def test_graph_search_route_validates_missing_id():
    client = create_test_client()

    response = client.get("/api/graph/search")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_graph_traverse_route_executes_dfs_and_bfs_with_different_orders():
    client = create_test_client()
    for node_id in ["A", "B", "C", "D", "E"]:
        client.post("/api/graph/nodes", json={"id": node_id})
    client.post("/api/graph/edges", json={"source": "A", "target": "B"})
    client.post("/api/graph/edges", json={"source": "A", "target": "C"})
    client.post("/api/graph/edges", json={"source": "B", "target": "D"})
    client.post("/api/graph/edges", json={"source": "C", "target": "E"})

    dfs_response = client.get("/api/graph/traverse?algorithm=DFS&start=A")
    bfs_response = client.get("/api/graph/traverse?algorithm=BFS&start=A")
    dfs_payload = dfs_response.get_json()
    bfs_payload = bfs_response.get_json()

    assert dfs_response.status_code == 200
    assert bfs_response.status_code == 200
    assert dfs_payload["data"]["traversal"]["algorithm"] == "DFS"
    assert bfs_payload["data"]["traversal"]["algorithm"] == "BFS"
    assert dfs_payload["data"]["traversal"]["order"] == ["A", "B", "D", "C", "E"]
    assert bfs_payload["data"]["traversal"]["order"] == ["A", "B", "C", "D", "E"]
    assert dfs_payload["data"]["traversal"]["order"] != bfs_payload["data"]["traversal"]["order"]


def test_graph_dfs_and_bfs_shortcut_routes():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "A"})
    client.post("/api/graph/nodes", json={"id": "B"})
    client.post("/api/graph/edges", json={"source": "A", "target": "B"})

    dfs_response = client.get("/api/graph/dfs?start=A")
    bfs_response = client.get("/api/graph/bfs?start=A")

    assert dfs_response.status_code == 200
    assert bfs_response.status_code == 200
    assert dfs_response.get_json()["data"]["traversal"]["algorithm"] == "DFS"
    assert bfs_response.get_json()["data"]["traversal"]["algorithm"] == "BFS"


def test_graph_traverse_route_validates_algorithm_and_start_node():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "A"})

    invalid_algorithm = client.get("/api/graph/traverse?algorithm=inorder&start=A")
    missing_start = client.get("/api/graph/traverse?algorithm=DFS&start=Z")

    assert invalid_algorithm.status_code == 400
    assert invalid_algorithm.get_json()["error"]["code"] == "VALIDATION_ERROR"
    assert missing_start.status_code == 404
    assert missing_start.get_json()["error"]["code"] == "NOT_FOUND"


def test_graph_demo_load_route_builds_prerequisite_graph_from_dataset():
    client = create_test_client()

    response = client.post("/api/graph/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "demo-load"
    assert payload["data"]["metrics"]["verticesCount"] > 0
    assert payload["data"]["metrics"]["edgesCount"] > 0
    assert payload["data"]["result"]["loaded"]["courses"] > 0
    assert payload["data"]["result"]["loaded"]["prerequisites"] > 0


def test_graph_metrics_route_returns_degree_and_connectivity_metrics():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "A"})
    client.post("/api/graph/nodes", json={"id": "B"})
    client.post("/api/graph/edges", json={"source": "A", "target": "B"})

    response = client.get("/api/graph/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "metrics"
    assert payload["data"]["metrics"]["verticesCount"] == 2
    assert payload["data"]["metrics"]["edgesCount"] == 1
    assert payload["data"]["metrics"]["connectedComponents"] == 1
    assert payload["data"]["result"]["metricsOnly"] is True


def test_graph_reset_route_clears_graph_state():
    client = create_test_client()
    client.post("/api/graph/nodes", json={"id": "A"})

    response = client.post("/api/graph/reset")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "reset"
    assert payload["data"]["metrics"]["verticesCount"] == 0
    assert payload["data"]["metrics"]["edgesCount"] == 0
    assert payload["data"]["result"]["reset"] is True
