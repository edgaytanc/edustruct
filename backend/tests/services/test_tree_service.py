import pytest

from app.errors.exceptions import DuplicateKeyError, NotFoundError, ValidationError
from app.services.tree_service import TreeService


def test_load_demo_creates_academic_tree_with_metrics():
    service = TreeService()

    result = service.load_demo()

    assert result["size"] == 8
    assert result["root"]["id"] == "faculty-engineering"
    assert result["metrics"]["height"] == 3
    assert result["metrics"]["levels"] == 4
    assert len(result["nodes"]) == 8
    assert len(result["edges"]) == 7


def test_insert_child_under_existing_parent():
    service = TreeService()
    service.insert("faculty", "Facultad")

    result = service.insert("career", "Carrera", parent_id="faculty", category="career")

    assert result["inserted"]["id"] == "career"
    assert result["size"] == 2
    assert result["metrics"]["edgesCount"] == 1


def test_insert_duplicate_id_raises_duplicate_key_error():
    service = TreeService()
    service.insert("faculty", "Facultad")

    with pytest.raises(DuplicateKeyError):
        service.insert("faculty", "Facultad repetida", parent_id="faculty")


def test_insert_with_missing_parent_raises_not_found_error():
    service = TreeService()
    service.insert("faculty", "Facultad")

    with pytest.raises(NotFoundError):
        service.insert("career", "Carrera", parent_id="missing")


def test_search_returns_found_false_when_node_does_not_exist():
    service = TreeService()
    service.load_demo()

    result = service.search("missing")

    assert result["found"] is False
    assert result["node"] is None


def test_delete_removes_subtree():
    service = TreeService()
    service.load_demo()

    result = service.delete("cycle-1")

    assert result["deleted"]["id"] == "cycle-1"
    assert result["size"] == 5
    assert service.search("math-1")["found"] is False


def test_traverse_rejects_invalid_type():
    service = TreeService()

    with pytest.raises(ValidationError):
        service.traverse("inorder")


def test_levelorder_traversal_uses_academic_order():
    service = TreeService()
    service.load_demo()

    result = service.traverse("levelorder")

    assert result["traversal"]["type"] == "levelorder"
    assert result["traversal"]["order"][0] == "faculty-engineering"
    assert "career-systems" in result["traversal"]["order"]
