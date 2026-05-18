from app import create_app
from app.routes.tree import tree_service


def setup_function():
    tree_service.reset()


def test_tree_demo_load_route_returns_visualization():
    app = create_app()
    client = app.test_client()

    response = client.post("/api/tree/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["metrics"]["count"] == 8
    assert len(payload["data"]["nodes"]) == 8
    assert len(payload["data"]["edges"]) == 7


def test_tree_insert_route_creates_root_and_child():
    app = create_app()
    client = app.test_client()

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


def test_tree_search_route_returns_node_level():
    app = create_app()
    client = app.test_client()
    client.post("/api/tree/demo/load")

    response = client.get("/api/tree/search?id=math-1")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is True
    assert payload["data"]["result"]["level"] == 3


def test_tree_traverse_route_returns_preorder():
    app = create_app()
    client = app.test_client()
    client.post("/api/tree/demo/load")

    response = client.get("/api/tree/traverse?type=preorder")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["traversal"]["type"] == "preorder"
    assert payload["data"]["traversal"]["order"][0] == "faculty-engineering"
