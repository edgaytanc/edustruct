from app.serializers.react_flow_serializer import serialize_hash_table


def test_serialize_hash_table_creates_bucket_nodes_for_empty_table():
    buckets = [
        {"bucketIndex": 0, "size": 0, "hasCollision": False, "items": []},
        {"bucketIndex": 1, "size": 0, "hasCollision": False, "items": []},
    ]

    result = serialize_hash_table(buckets=buckets)

    assert len(result["nodes"]) == 2
    assert result["edges"] == []
    assert result["nodes"][0]["id"] == "hash-bucket-0"
    assert result["nodes"][0]["type"] == "hashBucket"
    assert result["nodes"][0]["data"]["category"] == "bucket-empty"
    assert result["nodes"][0]["data"]["metadata"]["role"] == "bucket"


def test_serialize_hash_table_creates_chain_edges_and_collision_categories():
    buckets = [
        {
            "bucketIndex": 0,
            "size": 2,
            "hasCollision": True,
            "items": [
                {
                    "key": "a",
                    "value": {"student_id": "STU-A", "full_name": "Ana"},
                    "chainPosition": 0,
                    "collision": False,
                },
                {
                    "key": "d",
                    "value": {"student_id": "STU-D", "full_name": "Diego"},
                    "chainPosition": 1,
                    "collision": True,
                },
            ],
        }
    ]

    result = serialize_hash_table(
        buckets=buckets,
        metrics={"collisions": 1, "loadFactor": 0.67, "capacity": 3},
    )

    assert len(result["nodes"]) == 3
    assert len(result["edges"]) == 2
    assert result["nodes"][0]["data"]["category"] == "bucket-collision"
    assert result["nodes"][1]["data"]["category"] == "entry"
    assert result["nodes"][2]["data"]["category"] == "collision"
    assert result["nodes"][2]["data"]["metadata"]["collision"] is True
    assert result["edges"][0]["label"] == "head"
    assert result["edges"][1]["label"] == "next"
    assert result["edges"][1]["animated"] is True


def test_serialize_hash_table_highlights_last_operation_item_and_bucket():
    buckets = [
        {
            "bucketIndex": 2,
            "size": 1,
            "hasCollision": False,
            "items": [
                {
                    "key": "2024001",
                    "value": {"student_id": "STU-001", "full_name": "Andrea Morales"},
                    "chainPosition": 0,
                    "collision": False,
                }
            ],
        }
    ]

    result = serialize_hash_table(
        buckets=buckets,
        last_operation={"operation": "SEARCH", "key": "2024001", "bucketIndex": 2},
    )

    bucket = result["nodes"][0]
    entry = result["nodes"][1]
    assert bucket["data"]["metadata"]["isHighlighted"] is True
    assert entry["data"]["category"] == "highlighted-entry"
    assert entry["data"]["metadata"]["isHighlighted"] is True


def test_serialize_hash_table_uses_value_as_label_when_not_dict():
    buckets = [
        {
            "bucketIndex": 0,
            "size": 1,
            "hasCollision": False,
            "items": [
                {"key": "CUR-001", "value": "Programación III", "chainPosition": 0, "collision": False}
            ],
        }
    ]

    result = serialize_hash_table(buckets=buckets)

    assert "Programación III" in result["nodes"][1]["data"]["label"]
