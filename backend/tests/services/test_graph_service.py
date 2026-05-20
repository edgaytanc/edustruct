import json
from pathlib import Path

import pytest

from app.errors.exceptions import DatasetError, DuplicateKeyError, NotFoundError, ValidationError
from app.services.graph_service import GraphService


def test_state_returns_empty_graph_visual_contract():
    service = GraphService()

    result = service.state()

    assert result["verticesCount"] == 0
    assert result["edgesCount"] == 0
    assert result["isEmpty"] is True
    assert result["nodes"] == []
    assert result["edges"] == []
    assert result["metrics"]["connectedComponents"] == 0


def test_add_node_creates_course_node_and_visual_node():
    service = GraphService()

    result = service.add_node("CUR-001", {"code": "SIS-101", "name": "Intro"})

    assert result["operation"] == "add-node"
    assert result["verticesCount"] == 1
    assert result["node"]["id"] == "CUR-001"
    assert result["nodes"][0]["id"] == "CUR-001"
    assert result["nodes"][0]["data"]["metadata"]["degree"] == 0


def test_add_node_rejects_duplicate_and_invalid_ids():
    service = GraphService()
    service.add_node("CUR-001")

    with pytest.raises(DuplicateKeyError):
        service.add_node("CUR-001")

    with pytest.raises(ValidationError):
        service.add_node("   ")


def test_add_edge_creates_directed_prerequisite_relation():
    service = GraphService()
    service.add_node("CUR-001")
    service.add_node("CUR-005")

    result = service.add_edge("CUR-001", "CUR-005")

    assert result["operation"] == "add-edge"
    assert result["edgesCount"] == 1
    assert result["edge"] == {"source": "CUR-001", "target": "CUR-005"}
    assert result["graph"]["nodes"][0]["neighbors"] == ["CUR-005"]
    assert result["metrics"]["maxOutDegree"] == 1
    assert result["metrics"]["maxInDegree"] == 1


def test_add_edge_rejects_missing_nodes_and_duplicates():
    service = GraphService()
    service.add_node("CUR-001")

    with pytest.raises(NotFoundError):
        service.add_edge("CUR-001", "CUR-005")

    service.add_node("CUR-005")
    service.add_edge("CUR-001", "CUR-005")

    with pytest.raises(DuplicateKeyError):
        service.add_edge("CUR-001", "CUR-005")


def test_search_returns_found_payload_and_highlights_node():
    service = GraphService()
    service.add_node("CUR-001", {"code": "SIS-101", "name": "Intro"})

    result = service.search("CUR-001")

    assert result["operation"] == "search"
    assert result["found"] is True
    assert result["search"]["comparisons"] == 1
    assert result["node"]["id"] == "CUR-001"
    assert result["nodes"][0]["data"]["category"] == "search-match"


def test_search_returns_not_found_without_raising():
    service = GraphService()

    result = service.search("CUR-999")

    assert result["found"] is False
    assert result["node"] is None
    assert result["search"]["found"] is False


def test_dfs_and_bfs_return_different_orders_for_branching_graph():
    service = GraphService()
    for node_id in ["A", "B", "C", "D", "E"]:
        service.add_node(node_id)
    service.add_edge("A", "B")
    service.add_edge("A", "C")
    service.add_edge("B", "D")
    service.add_edge("C", "E")

    dfs_result = service.dfs("A")
    bfs_result = service.bfs("A")

    assert dfs_result["traversal"]["algorithm"] == "DFS"
    assert bfs_result["traversal"]["algorithm"] == "BFS"
    assert dfs_result["order"] == ["A", "B", "D", "C", "E"]
    assert bfs_result["order"] == ["A", "B", "C", "D", "E"]
    assert dfs_result["order"] != bfs_result["order"]
    assert len(dfs_result["steps"]) > 0


def test_traverse_rejects_invalid_algorithm_and_missing_start():
    service = GraphService()
    service.add_node("A")

    with pytest.raises(ValidationError):
        service.traverse("inorder", "A")

    with pytest.raises(NotFoundError):
        service.traverse("DFS", "Z")


def test_load_demo_builds_graph_from_dataset(tmp_path: Path):
    courses = [
        {"id": "CUR-001", "code": "SIS-101", "name": "Intro", "credits": 5, "cycle_id": "CIC-001"},
        {"id": "CUR-005", "code": "SIS-201", "name": "Programación I", "credits": 5, "cycle_id": "CIC-002"},
        {"id": "CUR-009", "code": "SIS-301", "name": "Programación II", "credits": 5, "cycle_id": "CIC-003"},
    ]
    prerequisites = [
        {"course_id": "CUR-005", "prerequisite_id": "CUR-001"},
        {"course_id": "CUR-009", "prerequisite_id": "CUR-005"},
    ]
    (tmp_path / "courses.json").write_text(json.dumps(courses), encoding="utf-8")
    (tmp_path / "prerequisites.json").write_text(json.dumps(prerequisites), encoding="utf-8")
    service = GraphService(dataset_root=tmp_path)

    result = service.load_demo()

    assert result["operation"] == "load-demo"
    assert result["loaded"] == {"courses": 3, "prerequisites": 2}
    assert result["verticesCount"] == 3
    assert result["edgesCount"] == 2
    assert result["graph"]["edges"][0] == {"source": "CUR-001", "target": "CUR-005"}
    assert result["metrics"]["connectedComponents"] == 1


def test_load_demo_rejects_unknown_course_references(tmp_path: Path):
    (tmp_path / "courses.json").write_text(
        json.dumps([{"id": "CUR-001", "code": "SIS-101", "name": "Intro"}]),
        encoding="utf-8",
    )
    (tmp_path / "prerequisites.json").write_text(
        json.dumps([{"course_id": "CUR-404", "prerequisite_id": "CUR-001"}]),
        encoding="utf-8",
    )
    service = GraphService(dataset_root=tmp_path)

    with pytest.raises(DatasetError):
        service.load_demo()


def test_metrics_and_reset():
    service = GraphService()
    service.add_node("A")
    service.add_node("B")
    service.add_edge("A", "B")

    metrics = service.metrics()
    reset = service.reset()

    assert metrics["metricsOnly"] is True
    assert metrics["metrics"]["verticesCount"] == 2
    assert metrics["metrics"]["edgesCount"] == 1
    assert reset["reset"] is True
    assert reset["verticesCount"] == 0
    assert reset["edgesCount"] == 0
