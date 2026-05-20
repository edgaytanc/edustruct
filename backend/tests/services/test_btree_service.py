import pytest

from app.errors.exceptions import DuplicateKeyError, ValidationError
from app.services.btree_service import BTreeService


def test_initial_state_is_empty_and_serializable():
    service = BTreeService()

    result = service.state()

    assert result["isEmpty"] is True
    assert result["isValid"] is True
    assert result["order"] == 4
    assert result["maxKeys"] == 3
    assert result["minKeys"] == 1
    assert result["size"] == 0
    assert result["root"] is None
    assert result["nodes"] == []
    assert result["edges"] == []
    assert result["metrics"]["count"] == 0
    assert result["metrics"]["levels"] == 0
    assert result["splitEvents"] == []


def test_configure_resets_tree_with_new_order():
    service = BTreeService()
    service.insert(10)

    result = service.configure(5)

    assert result["configured"] is True
    assert result["operation"] == "configure"
    assert result["operationOrder"] == 5
    assert result["order"] == 5
    assert result["maxKeys"] == 4
    assert result["minKeys"] == 2
    assert result["size"] == 0


def test_configure_rejects_invalid_order():
    with pytest.raises(ValidationError):
        BTreeService(order="4")

    service = BTreeService()
    with pytest.raises(ValidationError):
        service.configure(2)


def test_insert_key_into_btree():
    service = BTreeService()

    result = service.insert(2024008)

    assert result["inserted"] == 2024008
    assert result["root"]["keys"] == [2024008]
    assert result["size"] == 1
    assert result["isValid"] is True
    assert result["metrics"]["edgesCount"] == 0
    assert result["before"] == {"nodes": [], "edges": []}
    assert len(result["after"]["nodes"]) == 1
    assert result["splitOccurred"] is False


def test_insert_split_reports_event_and_after_state():
    service = BTreeService(order=4)
    service.insert(10)
    service.insert(20)
    service.insert(30)

    result = service.insert(40)

    assert result["root"]["keys"] == [30]
    assert result["splitOccurred"] is True
    assert result["lastSplit"]["type"] == "SPLIT"
    assert result["lastSplit"]["promotedKey"] == 30
    assert result["lastSplit"]["createdNewRoot"] is True
    assert result["metrics"]["splitCount"] == 1
    assert result["before"] is not None
    assert len(result["after"]["nodes"]) == 3


def test_bulk_insert_adds_multiple_keys_and_reports_splits():
    service = BTreeService()

    result = service.bulk_insert([40, 20, 60, 10, 30, 50, 70])

    assert result["inserted"] == [40, 20, 60, 10, 30, 50, 70]
    assert result["operation"] == "bulk-insert"
    assert result["splitOccurred"] is True
    assert result["size"] == 7
    assert result["isValid"] is True
    assert result["metrics"]["nodeCount"] == len(result["nodes"])


def test_bulk_insert_rejects_non_list_payload():
    service = BTreeService()

    with pytest.raises(ValidationError):
        service.bulk_insert("10,20")


def test_insert_strips_string_keys():
    service = BTreeService()

    result = service.insert("  EXP-2024-001  ")

    assert result["inserted"] == "EXP-2024-001"
    assert result["root"]["keys"] == ["EXP-2024-001"]


def test_insert_rejects_empty_key():
    service = BTreeService()

    with pytest.raises(ValidationError):
        service.insert("")

    with pytest.raises(ValidationError):
        service.insert(None)


def test_insert_duplicate_key_raises_duplicate_key_error():
    service = BTreeService()
    service.insert(50)

    with pytest.raises(DuplicateKeyError):
        service.insert(50)


def test_insert_incomparable_key_raises_validation_error():
    service = BTreeService()
    service.insert(50)

    with pytest.raises(ValidationError):
        service.insert({"record": 25})


def test_search_returns_found_false_when_key_does_not_exist():
    service = BTreeService()
    service.load_demo()

    result = service.search(9999999)

    assert result["found"] is False
    assert result["node"] is None
    assert result["level"] is None
    assert result["query"] == 9999999
    assert len(result["path"]) >= 1


def test_search_returns_node_level_and_path_when_found():
    service = BTreeService()
    service.load_demo()

    result = service.search(2024048)

    assert result["found"] is True
    assert 2024048 in result["node"]["keys"]
    assert isinstance(result["level"], int)
    assert result["search"]["found"] is True
    assert result["search"]["path"][0] == result["tree"]["levelorder"][0]["keys"]


def test_traverse_rejects_invalid_type():
    service = BTreeService()

    with pytest.raises(ValidationError):
        service.traverse("preorder")


def test_traversals_are_available():
    service = BTreeService()
    service.bulk_insert([30, 10, 50, 20, 40])

    assert service.traverse("inorder")["traversal"]["order"] == [10, 20, 30, 40, 50]
    assert len(service.traverse("levelorder")["traversal"]["steps"]) == service.state()["metrics"]["nodeCount"]


def test_load_demo_creates_valid_academic_index_with_splits():
    service = BTreeService()

    result = service.load_demo()

    assert result["size"] == 11
    assert result["isValid"] is True
    assert result["metrics"]["height"] >= 1
    assert result["metrics"]["levels"] == result["metrics"]["height"] + 1
    assert result["metrics"]["leafCount"] > 0
    assert result["context"] == "Árbol B como índice académico de expedientes universitarios"
    assert result["splitOccurred"] is True
    assert len(result["splitEvents"]) > 0


def test_load_demo_is_idempotent_and_resets_previous_state():
    service = BTreeService()
    service.insert(999)

    first_result = service.load_demo()
    second_result = service.load_demo()

    assert first_result["size"] == 11
    assert second_result["size"] == 11
    assert service.search(999)["found"] is False


def test_metrics_method_marks_metrics_only_result():
    service = BTreeService()
    service.load_demo()

    result = service.metrics()

    assert result["metricsOnly"] is True
    assert result["metrics"]["count"] == 11
    assert result["metrics"]["nodeCount"] == len(result["nodes"])
    assert result["metrics"]["isValid"] is True


def test_reset_clears_tree_state_but_keeps_order():
    service = BTreeService(order=5)
    service.load_demo()

    result = service.reset()

    assert result["reset"] is True
    assert result["operation"] == "reset"
    assert result["isEmpty"] is True
    assert result["order"] == 5
    assert result["size"] == 0
    assert result["nodes"] == []
    assert result["edges"] == []
