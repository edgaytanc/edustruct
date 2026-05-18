import pytest

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.services.avl_service import AVLService


def test_initial_state_is_empty_and_serializable():
    service = AVLService()

    result = service.state()

    assert result["isEmpty"] is True
    assert result["isBalanced"] is True
    assert result["size"] == 0
    assert result["root"] is None
    assert result["tree"]["root"] is None
    assert result["nodes"] == []
    assert result["edges"] == []
    assert result["metrics"]["count"] == 0
    assert result["metrics"]["levels"] == 0
    assert result["rotationEvents"] == []


def test_insert_value_into_avl_tree():
    service = AVLService()

    result = service.insert(50)

    assert result["inserted"]["value"] == 50
    assert result["root"]["value"] == 50
    assert result["size"] == 1
    assert result["isBalanced"] is True
    assert result["metrics"]["edgesCount"] == 0
    assert result["before"] == {"nodes": [], "edges": []}
    assert len(result["after"]["nodes"]) == 1


def test_insert_ll_rotation_reports_event_and_after_state():
    service = AVLService()
    service.insert(30)
    service.insert(20)

    result = service.insert(10)

    assert result["root"]["value"] == 20
    assert result["rotationEvents"][0]["type"] == "LL"
    assert result["lastRotation"]["pivot"] == 30
    assert result["metrics"]["rotationCount"] == 1
    assert result["before"] is not None
    assert len(result["after"]["nodes"]) == 3


def test_insert_rr_rotation_reports_event():
    service = AVLService()
    service.insert(10)
    service.insert(20)

    result = service.insert(30)

    assert result["root"]["value"] == 20
    assert result["rotationEvents"][0]["type"] == "RR"
    assert result["lastRotation"]["pivot"] == 10


def test_insert_lr_rotation_reports_event():
    service = AVLService()
    service.insert(30)
    service.insert(10)

    result = service.insert(20)

    assert result["root"]["value"] == 20
    assert result["rotationEvents"][0]["type"] == "LR"
    assert result["lastRotation"]["before"]["value"] == 30
    assert result["lastRotation"]["after"]["value"] == 20


def test_insert_rl_rotation_reports_event():
    service = AVLService()
    service.insert(10)
    service.insert(30)

    result = service.insert(20)

    assert result["root"]["value"] == 20
    assert result["rotationEvents"][0]["type"] == "RL"
    assert result["lastRotation"]["before"]["value"] == 10
    assert result["lastRotation"]["after"]["value"] == 20


def test_load_demo_creates_balanced_avl_tree_with_rotations():
    service = AVLService()

    result = service.load_demo()

    assert result["size"] == 7
    assert result["isBalanced"] is True
    assert result["metrics"]["height"] == 2
    assert result["metrics"]["levels"] == 3
    assert result["metrics"]["leafCount"] == 4
    assert result["metrics"]["edgesCount"] == 6
    assert result["context"] == "Árbol AVL de búsqueda eficiente por ID académico"
    assert {event["type"] for event in result["rotationEvents"]} >= {"LL", "RR", "LR"}


def test_load_demo_is_idempotent_and_resets_previous_state():
    service = AVLService()
    service.insert(999)

    first_result = service.load_demo()
    second_result = service.load_demo()

    assert first_result["size"] == 7
    assert second_result["size"] == 7
    assert service.search(999)["found"] is False


def test_insert_strips_string_values():
    service = AVLService()

    result = service.insert("  B  ")

    assert result["inserted"]["value"] == "B"
    assert result["inserted"]["label"] == "B"


def test_insert_rejects_empty_value():
    service = AVLService()

    with pytest.raises(ValidationError):
        service.insert("")

    with pytest.raises(ValidationError):
        service.insert(None)


def test_insert_duplicate_value_raises_duplicate_key_error():
    service = AVLService()
    service.insert(50)

    with pytest.raises(DuplicateKeyError):
        service.insert(50)


def test_insert_incomparable_value_raises_validation_error():
    service = AVLService()
    service.insert(50)

    with pytest.raises(ValidationError):
        service.insert({"value": 25})


def test_search_returns_found_false_when_value_does_not_exist():
    service = AVLService()
    service.load_demo()

    result = service.search(999)

    assert result["found"] is False
    assert result["node"] is None
    assert result["level"] is None
    assert result["query"] == 999


def test_search_returns_node_level_when_found():
    service = AVLService()
    service.load_demo()

    result = service.search(25)

    assert result["found"] is True
    assert result["node"]["value"] == 25
    assert isinstance(result["level"], int)
    assert result["node"]["balanceFactor"] in {-1, 0, 1}


def test_delete_removes_value_and_keeps_tree_balanced():
    service = AVLService()
    service.load_demo()

    result = service.delete(10)

    assert result["deleted"]["value"] == 10
    assert result["size"] == 6
    assert result["metrics"]["count"] == 6
    assert result["isBalanced"] is True
    assert service.search(10)["found"] is False
    assert result["before"] is not None
    assert result["after"] is not None


def test_delete_missing_value_raises_not_found_error():
    service = AVLService()
    service.load_demo()

    with pytest.raises(NotFoundError):
        service.delete(999)


def test_delete_empty_tree_raises_structure_empty_error():
    service = AVLService()

    with pytest.raises(StructureEmptyError):
        service.delete(999)


def test_traverse_rejects_invalid_type():
    service = AVLService()

    with pytest.raises(ValidationError):
        service.traverse("dfs")


def test_traversals_are_available():
    service = AVLService()
    for value in [30, 20, 10, 40, 50]:
        service.insert(value)

    assert service.traverse("inorder")["traversal"]["order"] == [10, 20, 30, 40, 50]
    assert service.traverse("preorder")["traversal"]["order"][0] == service.state()["root"]["value"]
    assert len(service.traverse("postorder")["traversal"]["order"]) == 5
    assert len(service.traverse("levelorder")["traversal"]["steps"]) == 5


def test_traversal_steps_include_avl_metadata_when_available():
    service = AVLService()
    service.load_demo()

    result = service.traverse("levelorder")
    first_step = result["traversal"]["steps"][0]

    assert first_step["height"] is not None
    assert first_step["balanceFactor"] in {-1, 0, 1}
    assert first_step["level"] == 0


def test_metrics_method_marks_metrics_only_result():
    service = AVLService()
    service.load_demo()

    result = service.metrics()

    assert result["metricsOnly"] is True
    assert result["metrics"]["count"] == 7
    assert result["metrics"]["edgesCount"] == 6
    assert result["metrics"]["isBalanced"] is True


def test_reset_clears_tree_state():
    service = AVLService()
    service.load_demo()

    result = service.reset()

    assert result["reset"] is True
    assert result["isEmpty"] is True
    assert result["size"] == 0
    assert result["nodes"] == []
    assert result["edges"] == []
