from app.serializers.react_flow_serializer import serialize_btree


def test_serialize_empty_btree_returns_empty_nodes_and_edges():
    visualization = serialize_btree([])

    assert visualization == {"nodes": [], "edges": []}


def test_serialize_btree_preserves_multi_key_metadata():
    items = [
        {
            "id": "btree-20-40",
            "keys": [20, 40],
            "label": "20 | 40",
            "leaf": False,
            "level": 0,
            "keyCount": 2,
            "maxKeys": 3,
        }
    ]

    visualization = serialize_btree(items)
    node = visualization["nodes"][0]
    metadata = node["data"]["metadata"]

    assert node["id"] == "btree-20-40"
    assert node["type"] == "btreeNode"
    assert node["data"]["label"] == "20 | 40"
    assert node["data"]["category"] == "root"
    assert metadata["structure"] == "btree"
    assert metadata["keys"] == [20, 40]
    assert metadata["leaf"] is False
    assert metadata["level"] == 0
    assert metadata["keyCount"] == 2
    assert metadata["maxKeys"] == 3


def test_serialize_btree_marks_leaf_and_internal_categories():
    items = [
        {"id": "btree-30", "keys": [30], "leaf": False, "level": 0},
        {"id": "btree-10-20", "keys": [10, 20], "leaf": True, "level": 1, "parentId": "btree-30", "childIndex": 0},
        {"id": "btree-40-50", "keys": [40, 50], "leaf": False, "level": 1, "parentId": "btree-30", "childIndex": 1},
    ]

    visualization = serialize_btree(items)
    categories = {node["id"]: node["data"]["category"] for node in visualization["nodes"]}

    assert categories["btree-30"] == "root"
    assert categories["btree-10-20"] == "leaf"
    assert categories["btree-40-50"] == "internal"


def test_serialize_btree_edges_use_parent_child_contract():
    items = [
        {"id": "btree-30", "keys": [30], "leaf": False, "level": 0},
        {"id": "btree-10-20", "keys": [10, 20], "leaf": True, "level": 1, "parentId": "btree-30", "childIndex": 0},
    ]

    visualization = serialize_btree(items)
    edge = visualization["edges"][0]

    assert edge["id"] == "btree-edge-btree-30-btree-10-20"
    assert edge["source"] == "btree-30"
    assert edge["target"] == "btree-10-20"
    assert edge["label"] == "0"
    assert edge["data"]["relationship"] == "parent-child"


def test_serialize_btree_positions_siblings_on_same_level_horizontally():
    items = [
        {"id": "btree-30", "keys": [30], "leaf": False, "level": 0},
        {"id": "btree-10-20", "keys": [10, 20], "leaf": True, "level": 1, "parentId": "btree-30", "childIndex": 0},
        {"id": "btree-40-50", "keys": [40, 50], "leaf": True, "level": 1, "parentId": "btree-30", "childIndex": 1},
    ]

    visualization = serialize_btree(items)
    positions = {node["id"]: node["position"] for node in visualization["nodes"]}

    assert positions["btree-10-20"]["y"] == positions["btree-40-50"]["y"]
    assert positions["btree-10-20"]["x"] < positions["btree-40-50"]["x"]
