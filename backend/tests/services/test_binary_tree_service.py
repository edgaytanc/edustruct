import pytest

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.services.binary_tree_service import BinaryTreeService


def test_initial_state_is_empty_and_serializable():
    service = BinaryTreeService()

    result = service.state()

    assert result["isEmpty"] is True
    assert result["size"] == 0
    assert result["root"] is None
    assert result["tree"]["root"] is None
    assert result["nodes"] == []
    assert result["edges"] == []
    assert result["metrics"]["count"] == 0
    assert result["metrics"]["levels"] == 0


def test_load_demo_creates_binary_tree_with_metrics():
    service = BinaryTreeService()

    result = service.load_demo()

    assert result["size"] == 7
    assert result["root"]["value"] == 50
    assert result["metrics"]["height"] == 2
    assert result["metrics"]["levels"] == 3
    assert result["metrics"]["leafCount"] == 4
    assert result["metrics"]["edgesCount"] == 6
    assert len(result["nodes"]) == 7
    assert len(result["edges"]) == 6
    assert result["context"] == "Árbol binario de decisión académica por prioridad numérica"


def test_load_demo_is_idempotent_and_resets_previous_state():
    service = BinaryTreeService()
    service.insert(999)

    first_result = service.load_demo()
    second_result = service.load_demo()

    assert first_result["size"] == 7
    assert second_result["size"] == 7
    assert second_result["root"]["value"] == 50
    assert service.search(999)["found"] is False


def test_insert_value_into_tree():
    service = BinaryTreeService()

    result = service.insert(50)

    assert result["inserted"]["value"] == 50
    assert result["root"]["value"] == 50
    assert result["size"] == 1
    assert result["metrics"]["edgesCount"] == 0


def test_insert_strips_string_values():
    service = BinaryTreeService()

    result = service.insert("  B  ")

    assert result["inserted"]["value"] == "B"
    assert result["inserted"]["label"] == "B"


def test_insert_rejects_empty_value():
    service = BinaryTreeService()

    with pytest.raises(ValidationError):
        service.insert("")

    with pytest.raises(ValidationError):
        service.insert(None)


def test_insert_duplicate_value_raises_duplicate_key_error():
    service = BinaryTreeService()
    service.insert(50)

    with pytest.raises(DuplicateKeyError):
        service.insert(50)


def test_insert_incomparable_value_raises_validation_error():
    service = BinaryTreeService()
    service.insert(50)

    with pytest.raises(ValidationError):
        service.insert({"value": 25})


def test_search_returns_found_false_when_value_does_not_exist():
    service = BinaryTreeService()
    service.load_demo()

    result = service.search(999)

    assert result["found"] is False
    assert result["node"] is None
    assert result["level"] is None
    assert result["query"] == 999


def test_search_returns_node_level_when_found():
    service = BinaryTreeService()
    service.load_demo()

    result = service.search(40)

    assert result["found"] is True
    assert result["node"]["value"] == 40
    assert result["level"] == 2


def test_delete_removes_leaf_value():
    service = BinaryTreeService()
    service.load_demo()

    result = service.delete(10)

    assert result["deleted"]["value"] == 10
    assert result["size"] == 6
    assert result["metrics"]["count"] == 6
    assert service.search(10)["found"] is False


def test_delete_missing_value_raises_not_found_error():
    service = BinaryTreeService()
    service.load_demo()

    with pytest.raises(NotFoundError):
        service.delete(999)


def test_delete_empty_tree_raises_structure_empty_error():
    service = BinaryTreeService()

    with pytest.raises(StructureEmptyError):
        service.delete(999)


def test_traverse_rejects_invalid_type():
    service = BinaryTreeService()

    with pytest.raises(ValidationError):
        service.traverse("dfs")


def test_traversals_are_available():
    service = BinaryTreeService()
    service.load_demo()

    assert service.traverse("preorder")["traversal"]["order"] == [50, 25, 10, 40, 75, 60, 90]
    assert service.traverse("inorder")["traversal"]["order"] == [10, 25, 40, 50, 60, 75, 90]
    assert service.traverse("postorder")["traversal"]["order"] == [10, 40, 25, 60, 90, 75, 50]
    assert service.traverse("levelorder")["traversal"]["order"] == [50, 25, 75, 10, 40, 60, 90]


def test_traversal_steps_include_visual_metadata_when_available():
    service = BinaryTreeService()
    service.load_demo()

    result = service.traverse("levelorder")
    step_for_40 = next(step for step in result["traversal"]["steps"] if step["value"] == 40)

    assert step_for_40["step"] == 5
    assert step_for_40["level"] == 2
    assert step_for_40["direction"] == "right"


def test_metrics_method_marks_metrics_only_result():
    service = BinaryTreeService()
    service.load_demo()

    result = service.metrics()

    assert result["metricsOnly"] is True
    assert result["metrics"]["count"] == 7
    assert result["metrics"]["edgesCount"] == 6
    assert result["metrics"]["balanceFactor"] == 0


def test_reset_clears_tree_state():
    service = BinaryTreeService()
    service.load_demo()

    result = service.reset()

    assert result["reset"] is True
    assert result["isEmpty"] is True
    assert result["size"] == 0
    assert result["nodes"] == []
    assert result["edges"] == []
