from app.serializers.react_flow_serializer import serialize_binary_tree


def test_serialize_empty_binary_tree_returns_empty_nodes_and_edges():
    visualization = serialize_binary_tree([])

    assert visualization == {"nodes": [], "edges": []}


def test_serialize_binary_tree_creates_root_left_and_right_nodes():
    items = [
        {"id": "50", "value": 50, "label": "50", "level": 0, "hasLeft": True, "hasRight": True, "childrenCount": 2},
        {"id": "25", "value": 25, "label": "25", "level": 1, "parentId": "50", "parentValue": 50, "direction": "left", "hasLeft": False, "hasRight": False, "childrenCount": 0},
        {"id": "75", "value": 75, "label": "75", "level": 1, "parentId": "50", "parentValue": 50, "direction": "right", "hasLeft": False, "hasRight": False, "childrenCount": 0},
    ]

    visualization = serialize_binary_tree(items)

    assert len(visualization["nodes"]) == 3
    assert len(visualization["edges"]) == 2
    assert visualization["nodes"][0]["id"] == "50"
    assert visualization["nodes"][0]["data"]["category"] == "root"
    assert visualization["nodes"][1]["data"]["category"] == "left"
    assert visualization["nodes"][2]["data"]["category"] == "right"


def test_serialize_binary_tree_edges_keep_direction_relationship():
    items = [
        {"id": "50", "value": 50, "label": "50", "level": 0},
        {"id": "25", "value": 25, "label": "25", "level": 1, "parentId": "50", "direction": "left"},
    ]

    visualization = serialize_binary_tree(items)
    edge = visualization["edges"][0]

    assert edge["id"] == "binary-tree-edge-50-25"
    assert edge["source"] == "50"
    assert edge["target"] == "25"
    assert edge["label"] == "left"
    assert edge["data"]["relationship"] == "left"


def test_serialize_binary_tree_positions_left_before_root_and_right_after_root():
    items = [
        {"id": "50", "value": 50, "label": "50", "level": 0},
        {"id": "25", "value": 25, "label": "25", "level": 1, "parentId": "50", "direction": "left"},
        {"id": "75", "value": 75, "label": "75", "level": 1, "parentId": "50", "direction": "right"},
    ]

    visualization = serialize_binary_tree(items)
    positions = {node["id"]: node["position"]["x"] for node in visualization["nodes"]}

    assert positions["25"] < positions["50"]
    assert positions["75"] > positions["50"]


def test_serialize_binary_tree_preserves_metadata_for_animation_and_ui():
    items = [
        {
            "id": "25",
            "value": 25,
            "label": "25",
            "level": 1,
            "parentId": "50",
            "parentValue": 50,
            "direction": "left",
            "hasLeft": True,
            "hasRight": False,
            "childrenCount": 1,
        }
    ]

    visualization = serialize_binary_tree(items)
    metadata = visualization["nodes"][0]["data"]["metadata"]

    assert metadata["value"] == 25
    assert metadata["level"] == 1
    assert metadata["parentId"] == "50"
    assert metadata["parentValue"] == 50
    assert metadata["direction"] == "left"
    assert metadata["hasLeft"] is True
    assert metadata["hasRight"] is False
    assert metadata["childrenCount"] == 1
