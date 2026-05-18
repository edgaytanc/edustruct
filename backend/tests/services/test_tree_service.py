import pytest

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.services.tree_service import TreeService


def test_initial_state_is_empty_and_serializable():
    service = TreeService()

    result = service.state()

    assert result["isEmpty"] is True
    assert result["size"] == 0
    assert result["root"] is None
    assert result["tree"]["root"] is None
    assert result["nodes"] == []
    assert result["edges"] == []
    assert result["metrics"]["count"] == 0
    assert result["metrics"]["levels"] == 0


def test_load_demo_creates_academic_tree_with_metrics():
    service = TreeService()

    result = service.load_demo()

    assert result["size"] == 8
    assert result["root"]["id"] == "faculty-engineering"
    assert result["metrics"]["height"] == 3
    assert result["metrics"]["levels"] == 4
    assert result["metrics"]["leafCount"] == 4
    assert result["metrics"]["maxChildren"] == 2
    assert len(result["nodes"]) == 8
    assert len(result["edges"]) == 7
    assert result["context"] == "Pensum académico jerárquico"


def test_load_demo_is_idempotent_and_resets_previous_state():
    service = TreeService()
    service.insert("custom-root", "Raíz temporal")

    first_result = service.load_demo()
    second_result = service.load_demo()

    assert first_result["size"] == 8
    assert second_result["size"] == 8
    assert second_result["root"]["id"] == "faculty-engineering"
    assert service.search("custom-root")["found"] is False


def test_insert_child_under_existing_parent():
    service = TreeService()
    service.insert("faculty", "Facultad")

    result = service.insert("career", "Carrera", parent_id="faculty", category="career")

    assert result["inserted"]["id"] == "career"
    assert result["inserted"]["category"] == "career"
    assert result["parentId"] == "faculty"
    assert result["size"] == 2
    assert result["metrics"]["edgesCount"] == 1


def test_insert_strips_required_text_values():
    service = TreeService()

    result = service.insert(" faculty ", " Facultad ", category=" faculty ")

    assert result["inserted"]["id"] == "faculty"
    assert result["inserted"]["label"] == "Facultad"
    assert result["inserted"]["category"] == "faculty"


def test_insert_rejects_empty_id_and_label():
    service = TreeService()

    with pytest.raises(ValidationError):
        service.insert("", "Facultad")

    with pytest.raises(ValidationError):
        service.insert("faculty", "")


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


def test_insert_without_parent_when_root_exists_raises_validation_error():
    service = TreeService()
    service.insert("faculty", "Facultad")

    with pytest.raises(ValidationError):
        service.insert("career", "Carrera")


def test_search_returns_found_false_when_node_does_not_exist():
    service = TreeService()
    service.load_demo()

    result = service.search("missing")

    assert result["found"] is False
    assert result["node"] is None
    assert result["level"] is None
    assert result["query"] == "missing"


def test_search_returns_node_level_when_found():
    service = TreeService()
    service.load_demo()

    result = service.search("math-1")

    assert result["found"] is True
    assert result["node"]["id"] == "math-1"
    assert result["level"] == 3


def test_delete_removes_subtree():
    service = TreeService()
    service.load_demo()

    result = service.delete("cycle-1")

    assert result["deleted"]["id"] == "cycle-1"
    assert result["size"] == 5
    assert result["metrics"]["count"] == 5
    assert service.search("math-1")["found"] is False
    assert service.search("intro-programming")["found"] is False


def test_delete_missing_node_raises_not_found_error():
    service = TreeService()
    service.load_demo()

    with pytest.raises(NotFoundError):
        service.delete("missing")


def test_delete_empty_tree_raises_structure_empty_error():
    service = TreeService()

    with pytest.raises(StructureEmptyError):
        service.delete("missing")


def test_traverse_rejects_invalid_type():
    service = TreeService()

    with pytest.raises(ValidationError):
        service.traverse("inorder")


def test_levelorder_traversal_uses_academic_order():
    service = TreeService()
    service.load_demo()

    result = service.traverse("levelorder")

    assert result["traversal"]["type"] == "levelorder"
    assert result["traversal"]["order"] == [
        "faculty-engineering",
        "career-systems",
        "cycle-1",
        "cycle-2",
        "math-1",
        "intro-programming",
        "programming-1",
        "math-2",
    ]
    assert result["traversal"]["steps"][0]["step"] == 1


def test_preorder_and_postorder_traversals_are_available():
    service = TreeService()
    service.load_demo()

    preorder = service.traverse("preorder")
    postorder = service.traverse("postorder")

    assert preorder["traversal"]["order"][0] == "faculty-engineering"
    assert postorder["traversal"]["order"][-1] == "faculty-engineering"


def test_metrics_method_marks_metrics_only_result():
    service = TreeService()
    service.load_demo()

    result = service.metrics()

    assert result["metricsOnly"] is True
    assert result["metrics"]["count"] == 8
    assert result["metrics"]["edgesCount"] == 7


def test_reset_clears_tree_state():
    service = TreeService()
    service.load_demo()

    result = service.reset()

    assert result["reset"] is True
    assert result["isEmpty"] is True
    assert result["size"] == 0
    assert result["nodes"] == []
    assert result["edges"] == []
