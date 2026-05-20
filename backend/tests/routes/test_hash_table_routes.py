from app import create_app
from app.routes.hash_table import hash_table_service


def setup_function():
    hash_table_service.configure(7)


def create_test_client():
    app = create_app()
    return app.test_client()


def test_hash_state_route_returns_empty_table():
    client = create_test_client()

    response = client.get("/api/hash/state")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["structure"] == "hash"
    assert payload["data"]["operation"] == "state"
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["metrics"]["capacity"] == 7
    assert payload["data"]["metrics"]["collisions"] == 0
    assert len(payload["data"]["nodes"]) == 7
    assert payload["data"]["edges"] == []


def test_hash_configure_route_sets_capacity_and_resets_table():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})

    response = client.post("/api/hash/configure", json={"capacity": 5})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "configure"
    assert payload["data"]["metrics"]["capacity"] == 5
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["result"]["configured"] is True


def test_hash_configure_route_accepts_capacity_query_param():
    client = create_test_client()

    response = client.post("/api/hash/configure?capacity=11")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["metrics"]["capacity"] == 11


def test_hash_configure_route_rejects_invalid_capacity():
    client = create_test_client()

    response = client.post("/api/hash/configure", json={"capacity": 2})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_hash_insert_route_adds_student_entry():
    client = create_test_client()

    response = client.post(
        "/api/hash/insert",
        json={"key": "2024001", "value": {"student_id": "STU-001", "full_name": "Andrea Morales"}},
    )
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "insert"
    assert payload["data"]["metrics"]["count"] == 1
    assert payload["data"]["metrics"]["loadFactor"] == round(1 / 7, 4)
    assert payload["data"]["result"]["inserted"]["key"] == "2024001"
    assert len(payload["data"]["nodes"]) == 8


def test_hash_insert_route_reports_collision():
    client = create_test_client()
    client.post("/api/hash/configure", json={"capacity": 3})
    client.post("/api/hash/insert", json={"key": "a", "value": {"student_id": "STU-A"}})

    response = client.post("/api/hash/insert", json={"key": "d", "value": {"student_id": "STU-D"}})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["result"]["collisionOccurred"] is True
    assert payload["data"]["metrics"]["collisions"] == 1
    assert payload["data"]["metrics"]["collisionBucketCount"] == 1
    assert len(payload["data"]["edges"]) == 2


def test_hash_insert_route_validates_required_key():
    client = create_test_client()

    response = client.post("/api/hash/insert", json={"value": {"student_id": "STU-001"}})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_hash_insert_route_validates_required_value():
    client = create_test_client()

    response = client.post("/api/hash/insert", json={"key": "2024001"})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_hash_insert_route_rejects_duplicate_key():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})

    response = client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})
    payload = response.get_json()

    assert response.status_code == 409
    assert payload["success"] is False
    assert payload["error"]["code"] == "DUPLICATE_KEY"


def test_hash_bulk_insert_route_adds_multiple_entries():
    client = create_test_client()
    client.post("/api/hash/configure", json={"capacity": 3})

    response = client.post(
        "/api/hash/bulk-insert",
        json={
            "entries": [
                {"key": "a", "value": {"student_id": "STU-A"}},
                {"key": "d", "value": {"student_id": "STU-D"}},
            ]
        },
    )
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "bulk-insert"
    assert payload["data"]["metrics"]["count"] == 2
    assert payload["data"]["result"]["collisionOccurred"] is True
    assert len(payload["data"]["result"]["inserted"]) == 2


def test_hash_insert_route_accepts_entries_alias_for_bulk_insert():
    client = create_test_client()

    response = client.post(
        "/api/hash/insert",
        json={
            "entries": [
                {"key": "2024001", "value": {"student_id": "STU-001"}},
                {"key": "2024002", "value": {"student_id": "STU-002"}},
            ]
        },
    )
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["data"]["operation"] == "bulk-insert"
    assert payload["data"]["metrics"]["count"] == 2


def test_hash_bulk_insert_route_rejects_non_list_entries():
    client = create_test_client()

    response = client.post("/api/hash/bulk-insert", json={"entries": {"key": "2024001"}})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_hash_search_route_returns_found_entry():
    client = create_test_client()
    client.post(
        "/api/hash/insert",
        json={"key": "2024001", "value": {"student_id": "STU-001", "full_name": "Andrea Morales"}},
    )

    response = client.get("/api/hash/search?key=2024001")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "search"
    assert payload["data"]["result"]["found"] is True
    assert payload["data"]["result"]["value"]["student_id"] == "STU-001"
    assert isinstance(payload["data"]["result"]["bucketIndex"], int)


def test_hash_search_route_returns_not_found_result():
    client = create_test_client()

    response = client.get("/api/hash/search?key=2024999")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["found"] is False
    assert payload["data"]["result"]["value"] is None


def test_hash_search_route_validates_missing_key():
    client = create_test_client()

    response = client.get("/api/hash/search")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_hash_delete_route_removes_entry_by_json_body():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})

    response = client.delete("/api/hash/delete", json={"key": "2024001"})
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "delete"
    assert payload["data"]["result"]["deleted"]["key"] == "2024001"
    assert payload["data"]["metrics"]["count"] == 0

    search_response = client.get("/api/hash/search?key=2024001")
    assert search_response.get_json()["data"]["result"]["found"] is False


def test_hash_delete_route_accepts_query_param():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024002", "value": {"student_id": "STU-002"}})

    response = client.delete("/api/hash/delete?key=2024002")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["result"]["deleted"]["key"] == "2024002"


def test_hash_delete_route_rejects_empty_table():
    client = create_test_client()

    response = client.delete("/api/hash/delete", json={"key": "2024001"})
    payload = response.get_json()

    assert response.status_code == 422
    assert payload["success"] is False
    assert payload["error"]["code"] == "STRUCTURE_EMPTY"


def test_hash_delete_route_returns_not_found_for_missing_key():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})

    response = client.delete("/api/hash/delete", json={"key": "2024999"})
    payload = response.get_json()

    assert response.status_code == 404
    assert payload["success"] is False
    assert payload["error"]["code"] == "NOT_FOUND"


def test_hash_demo_load_route_returns_visible_collisions():
    client = create_test_client()

    response = client.post("/api/hash/demo/load")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["operation"] == "demo-load"
    assert payload["data"]["metrics"]["count"] == 5
    assert payload["data"]["metrics"]["collisions"] > 0
    assert payload["data"]["metrics"]["collisionBucketCount"] > 0
    assert payload["data"]["result"]["context"] == "Tabla hash para búsqueda de estudiantes por carnet universitario"


def test_hash_metrics_route_returns_current_metrics():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})

    response = client.get("/api/hash/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "metrics"
    assert payload["data"]["metrics"]["count"] == 1
    assert payload["data"]["result"]["metricsOnly"] is True


def test_hash_traverse_route_returns_bucket_chain_steps():
    client = create_test_client()
    client.post("/api/hash/configure", json={"capacity": 3})
    client.post("/api/hash/bulk-insert", json={"entries": [
        {"key": "a", "value": {"student_id": "STU-A"}},
        {"key": "d", "value": {"student_id": "STU-D"}},
    ]})

    response = client.get("/api/hash/traverse")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "traverse"
    assert payload["data"]["traversal"]["type"] == "buckets"
    assert payload["data"]["traversal"]["order"] == ["a", "d"]
    assert payload["data"]["traversal"]["steps"][1]["collision"] is True


def test_hash_reset_route_clears_table():
    client = create_test_client()
    client.post("/api/hash/insert", json={"key": "2024001", "value": {"student_id": "STU-001"}})

    response = client.post("/api/hash/reset")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["operation"] == "reset"
    assert payload["data"]["metrics"]["count"] == 0
    assert payload["data"]["metrics"]["collisions"] == 0
    assert payload["data"]["result"]["reset"] is True
