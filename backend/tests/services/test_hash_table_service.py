import pytest

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.services.hash_table_service import HashTableService


def test_state_returns_empty_hash_table_visual_contract():
    service = HashTableService(capacity=5)

    result = service.state()

    assert result["capacity"] == 5
    assert result["size"] == 0
    assert result["isEmpty"] is True
    assert result["metrics"]["collisions"] == 0
    assert result["metrics"]["loadFactor"] == 0
    assert len(result["buckets"]) == 5
    assert len(result["nodes"]) == 5
    assert result["edges"] == []


def test_configure_resets_table_with_new_capacity():
    service = HashTableService(capacity=5)
    service.insert("2024001", {"student_id": "STU-001"})

    result = service.configure(7)

    assert result["configured"] is True
    assert result["operation"] == "configure"
    assert result["capacity"] == 7
    assert result["size"] == 0
    assert result["metrics"]["emptyBucketCount"] == 7


@pytest.mark.parametrize("capacity", [None, "7", True, 2])
def test_configure_rejects_invalid_capacity(capacity):
    service = HashTableService()

    with pytest.raises(ValidationError):
        service.configure(capacity)


def test_insert_adds_student_and_returns_metrics():
    service = HashTableService(capacity=5)

    result = service.insert("2024001", {"student_id": "STU-001", "full_name": "Andrea Morales"})

    assert result["operation"] == "insert"
    assert result["operationKey"] == "2024001"
    assert result["inserted"]["key"] == "2024001"
    assert result["size"] == 1
    assert result["metrics"]["count"] == 1
    assert result["metrics"]["capacity"] == 5
    assert result["metrics"]["loadFactor"] == 0.2
    assert result["before"] is not None
    assert result["after"] is not None


def test_insert_detects_collision_and_updates_visual_nodes():
    service = HashTableService(capacity=3)

    service.insert("a", {"student_id": "STU-A", "full_name": "Ana"})
    result = service.insert("d", {"student_id": "STU-D", "full_name": "Diego"})

    assert result["collisionOccurred"] is True
    assert result["metrics"]["collisions"] == 1
    assert result["metrics"]["collisionBucketCount"] == 1
    assert result["metrics"]["maxChainLength"] == 2
    collision_nodes = [node for node in result["nodes"] if node["data"]["category"] in {"collision", "highlighted-collision"}]
    assert len(collision_nodes) == 1
    assert collision_nodes[0]["data"]["metadata"]["collision"] is True


def test_insert_rejects_duplicate_key():
    service = HashTableService(capacity=5)
    service.insert("2024001", {"student_id": "STU-001"})

    with pytest.raises(DuplicateKeyError):
        service.insert("2024001", {"student_id": "STU-001"})


@pytest.mark.parametrize("key", [None, "", "   "])
def test_insert_rejects_invalid_key(key):
    service = HashTableService()

    with pytest.raises(ValidationError):
        service.insert(key, {"student_id": "STU-001"})


def test_insert_rejects_missing_value():
    service = HashTableService()

    with pytest.raises(ValidationError):
        service.insert("2024001", None)


def test_bulk_insert_loads_entries_and_reports_collision():
    service = HashTableService(capacity=3)
    entries = [
        {"key": "a", "value": {"student_id": "STU-A"}},
        {"key": "d", "value": {"student_id": "STU-D"}},
    ]

    result = service.bulk_insert(entries)

    assert result["operation"] == "bulk-insert"
    assert result["collisionOccurred"] is True
    assert len(result["inserted"]) == 2
    assert result["metrics"]["collisions"] == 1


def test_bulk_insert_rejects_invalid_entries_payload():
    service = HashTableService()

    with pytest.raises(ValidationError):
        service.bulk_insert({"key": "2024001"})

    with pytest.raises(ValidationError):
        service.bulk_insert(["2024001"])


def test_search_returns_found_result_with_bucket_metadata():
    service = HashTableService(capacity=5)
    value = {"student_id": "STU-001", "full_name": "Andrea Morales"}
    service.insert("2024001", value)

    result = service.search("2024001")

    assert result["found"] is True
    assert result["value"] == value
    assert result["search"]["key"] == "2024001"
    assert isinstance(result["bucketIndex"], int)
    assert result["chainPosition"] == 0


def test_search_returns_not_found_without_raising():
    service = HashTableService(capacity=5)

    result = service.search("2024999")

    assert result["found"] is False
    assert result["value"] is None
    assert result["search"]["found"] is False


def test_delete_removes_key_and_returns_deleted_payload():
    service = HashTableService(capacity=5)
    value = {"student_id": "STU-001", "full_name": "Andrea Morales"}
    service.insert("2024001", value)

    result = service.delete("2024001")

    assert result["operation"] == "delete"
    assert result["deleted"]["key"] == "2024001"
    assert result["deleted"]["value"] == value
    assert result["size"] == 0
    assert result["isEmpty"] is True


def test_delete_raises_when_table_empty():
    service = HashTableService()

    with pytest.raises(StructureEmptyError):
        service.delete("2024001")


def test_delete_raises_when_key_not_found():
    service = HashTableService()
    service.insert("2024001", {"student_id": "STU-001"})

    with pytest.raises(NotFoundError):
        service.delete("2024999")


def test_load_demo_creates_visible_collisions():
    service = HashTableService(capacity=7)

    result = service.load_demo()

    assert result["operation"] == "load-demo"
    assert result["size"] == len(result["loaded"])
    assert result["metrics"]["collisions"] > 0
    assert result["metrics"]["collisionBucketCount"] > 0


def test_reset_clears_table_and_collision_counter():
    service = HashTableService(capacity=3)
    service.insert("a", {"student_id": "STU-A"})
    service.insert("d", {"student_id": "STU-D"})

    result = service.reset()

    assert result["reset"] is True
    assert result["operation"] == "reset"
    assert result["size"] == 0
    assert result["metrics"]["collisions"] == 0
