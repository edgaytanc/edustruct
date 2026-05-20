import pytest

from app.structures.hash_table import HashEntry, HashSearchResult, HashTable


def sample_student(name="Ana López"):
    return {
        "student_id": "STU-001",
        "carnet": "2024001",
        "full_name": name,
        "career_id": "CAR-001",
        "status": "active",
    }


def find_collision_keys(table):
    buckets = {}
    number = 2024000
    while True:
        key = str(number)
        bucket_index = table.hash_function(key)
        if bucket_index in buckets:
            return buckets[bucket_index], key, bucket_index
        buckets[bucket_index] = key
        number += 1


def test_initial_table_uses_manual_buckets_and_default_capacity():
    table = HashTable()

    assert table.capacity == 7
    assert table.size() == 0
    assert table.is_empty() is True
    assert table.collisions == 0
    assert table.load_factor() == 0
    assert isinstance(table.buckets, list)
    assert all(bucket is None for bucket in table.buckets)
    assert table.last_operation is None


def test_capacity_must_be_integer_and_at_least_three():
    with pytest.raises(ValueError, match="CAPACITY_MUST_BE_INTEGER"):
        HashTable(capacity="7")

    with pytest.raises(ValueError, match="CAPACITY_MUST_BE_AT_LEAST_3"):
        HashTable(capacity=2)


def test_hash_function_is_deterministic_and_within_capacity():
    table = HashTable(capacity=5)

    first = table.hash_function("2024001")
    second = table.hash_function("2024001")

    assert first == second
    assert 0 <= first < table.capacity


def test_hash_function_rejects_empty_keys():
    table = HashTable()

    with pytest.raises(ValueError, match="KEY_REQUIRED"):
        table.hash_function(None)

    with pytest.raises(ValueError, match="KEY_REQUIRED"):
        table.hash_function("   ")


def test_insert_first_entry_without_collision():
    table = HashTable(capacity=5)
    student = sample_student()

    entry = table.insert("2024001", student)
    bucket_index = table.hash_function("2024001")

    assert isinstance(entry, HashEntry)
    assert entry.key == "2024001"
    assert entry.value == student
    assert table.buckets[bucket_index] is entry
    assert table.size() == 1
    assert table.collisions == 0
    assert table.load_factor() == 0.2
    assert table.last_operation["operation"] == "INSERT"
    assert table.last_operation["collision"] is False


def test_insert_rejects_duplicate_keys():
    table = HashTable()
    table.insert("2024001", sample_student())

    with pytest.raises(ValueError, match="DUPLICATE_KEY"):
        table.insert("2024001", sample_student("Duplicado"))


def test_insert_collision_uses_separate_chaining_and_counts_collision():
    table = HashTable(capacity=3)
    first_key, second_key, bucket_index = find_collision_keys(table)

    first = table.insert(first_key, sample_student("Primero"))
    second = table.insert(second_key, sample_student("Segundo"))

    assert table.buckets[bucket_index] is first
    assert first.next is second
    assert second.next is None
    assert table.size() == 2
    assert table.collisions == 1
    assert table.collision_bucket_count() == 1
    assert table.max_chain_length() == 2
    assert table.last_operation["collision"] is True
    assert table.last_operation["chainPosition"] == 1


def test_search_returns_value_and_chain_metadata():
    table = HashTable(capacity=3)
    first_key, second_key, bucket_index = find_collision_keys(table)
    table.insert(first_key, sample_student("Primero"))
    table.insert(second_key, sample_student("Segundo"))

    result = table.search(second_key)

    assert isinstance(result, HashSearchResult)
    assert result.found is True
    assert result.key == second_key
    assert result.bucket_index == bucket_index
    assert result.value["full_name"] == "Segundo"
    assert result.comparisons == 2
    assert result.chain_position == 1
    assert table.contains(second_key) is True


def test_search_missing_key_returns_bucket_metadata():
    table = HashTable(capacity=5)
    table.insert("2024001", sample_student())

    result = table.search("9999999")

    assert result.found is False
    assert result.key == "9999999"
    assert 0 <= result.bucket_index < table.capacity
    assert result.value is None
    assert result.chain_position is None
    assert table.contains("9999999") is False


def test_delete_head_entry_preserves_remaining_chain():
    table = HashTable(capacity=3)
    first_key, second_key, bucket_index = find_collision_keys(table)
    table.insert(first_key, sample_student("Primero"))
    table.insert(second_key, sample_student("Segundo"))

    deleted = table.delete(first_key)

    assert deleted is True
    assert table.size() == 1
    assert table.buckets[bucket_index].key == second_key
    assert table.search(second_key).found is True
    assert table.search(first_key).found is False


def test_delete_middle_or_tail_entry_from_collision_chain():
    table = HashTable(capacity=3)
    first_key, second_key, bucket_index = find_collision_keys(table)
    third_key = None
    number = 2025000
    while third_key is None:
        candidate = str(number)
        if candidate not in {first_key, second_key} and table.hash_function(candidate) == bucket_index:
            third_key = candidate
        number += 1

    table.insert(first_key, sample_student("Primero"))
    table.insert(second_key, sample_student("Segundo"))
    table.insert(third_key, sample_student("Tercero"))

    assert table.delete(second_key) is True

    entries = table.bucket_entries(bucket_index)
    assert [entry.key for entry in entries] == [first_key, third_key]
    assert table.size() == 2
    assert table.search(second_key).found is False
    assert table.search(third_key).found is True


def test_delete_missing_key_returns_false():
    table = HashTable()
    table.insert("2024001", sample_student())

    assert table.delete("0000000") is False
    assert table.size() == 1
    assert table.last_operation["operation"] == "DELETE"
    assert table.last_operation["found"] is False


def test_bucket_entries_validates_bucket_index():
    table = HashTable()

    with pytest.raises(ValueError, match="BUCKET_INDEX_MUST_BE_INTEGER"):
        table.bucket_entries("0")

    with pytest.raises(ValueError, match="BUCKET_INDEX_OUT_OF_RANGE"):
        table.bucket_entries(-1)

    with pytest.raises(ValueError, match="BUCKET_INDEX_OUT_OF_RANGE"):
        table.bucket_entries(table.capacity)


def test_buckets_snapshot_marks_collisions_by_chain_position():
    table = HashTable(capacity=3)
    first_key, second_key, bucket_index = find_collision_keys(table)
    table.insert(first_key, sample_student("Primero"))
    table.insert(second_key, sample_student("Segundo"))

    snapshot = table.buckets_snapshot()
    bucket = snapshot[bucket_index]

    assert bucket["bucketIndex"] == bucket_index
    assert bucket["size"] == 2
    assert bucket["hasCollision"] is True
    assert bucket["items"][0]["collision"] is False
    assert bucket["items"][1]["collision"] is True
    assert bucket["items"][1]["chainPosition"] == 1


def test_to_dict_serializes_complete_state():
    table = HashTable(capacity=3)
    first_key, second_key, _ = find_collision_keys(table)
    table.insert(first_key, sample_student("Primero"))
    table.insert(second_key, sample_student("Segundo"))

    payload = table.to_dict()

    assert payload["capacity"] == 3
    assert payload["size"] == 2
    assert payload["collisions"] == 1
    assert payload["loadFactor"] == round(2 / 3, 4)
    assert payload["maxChainLength"] == 2
    assert payload["collisionBucketCount"] == 1
    assert isinstance(payload["buckets"], list)
    assert payload["lastOperation"]["operation"] == "INSERT"


def test_search_result_to_dict_is_json_friendly():
    table = HashTable()
    table.insert("2024001", sample_student())

    payload = table.search("2024001").to_dict()

    assert payload["found"] is True
    assert payload["key"] == "2024001"
    assert isinstance(payload["bucketIndex"], int)
    assert payload["value"]["student_id"] == "STU-001"


def test_clear_resets_entries_metrics_and_collision_counter():
    table = HashTable(capacity=3)
    first_key, second_key, _ = find_collision_keys(table)
    table.insert(first_key, sample_student("Primero"))
    table.insert(second_key, sample_student("Segundo"))

    table.clear()

    assert table.is_empty() is True
    assert table.size() == 0
    assert table.collisions == 0
    assert table.load_factor() == 0
    assert all(bucket is None for bucket in table.buckets)
    assert table.last_operation["operation"] == "CLEAR"
