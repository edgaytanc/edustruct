from app.serializers.react_flow_serializer import serialize_avl_tree


def test_serialize_empty_avl_tree_returns_empty_nodes_and_edges():
    visualization = serialize_avl_tree([])

    assert visualization == {"nodes": [], "edges": []}


def test_serialize_avl_tree_preserves_balance_metadata():
    items = [
        {
            "id": "20",
            "value": 20,
            "label": "20",
            "level": 0,
            "height": 2,
            "visualHeight": 1,
            "balanceFactor": 0,
            "isUnbalanced": False,
            "hasLeft": True,
            "hasRight": True,
            "childrenCount": 2,
        },
        {
            "id": "10",
            "value": 10,
            "label": "10",
            "level": 1,
            "parentId": "20",
            "parentValue": 20,
            "direction": "left",
            "height": 1,
            "visualHeight": 0,
            "balanceFactor": 0,
            "isUnbalanced": False,
        },
    ]

    visualization = serialize_avl_tree(items)
    metadata = visualization["nodes"][0]["data"]["metadata"]

    assert metadata["structure"] == "avl-tree"
    assert metadata["height"] == 2
    assert metadata["visualHeight"] == 1
    assert metadata["balanceFactor"] == 0
    assert metadata["isUnbalanced"] is False
    assert metadata["hasLeft"] is True
    assert metadata["hasRight"] is True
    assert metadata["childrenCount"] == 2


def test_serialize_avl_tree_marks_unbalanced_category_when_received():
    items = [
        {"id": "30", "value": 30, "label": "30", "level": 0, "height": 3, "balanceFactor": 2},
        {
            "id": "20",
            "value": 20,
            "label": "20",
            "level": 1,
            "parentId": "30",
            "direction": "left",
            "height": 2,
            "balanceFactor": 2,
            "isUnbalanced": True,
        },
    ]

    visualization = serialize_avl_tree(items)

    assert visualization["nodes"][0]["data"]["category"] == "root"
    assert visualization["nodes"][1]["data"]["category"] == "unbalanced"
    assert visualization["nodes"][1]["data"]["metadata"]["isUnbalanced"] is True


def test_serialize_avl_tree_edges_use_avl_prefix_and_direction():
    items = [
        {"id": "20", "value": 20, "label": "20", "level": 0},
        {"id": "30", "value": 30, "label": "30", "level": 1, "parentId": "20", "direction": "right"},
    ]

    visualization = serialize_avl_tree(items)
    edge = visualization["edges"][0]

    assert edge["id"] == "avl-tree-edge-20-30"
    assert edge["source"] == "20"
    assert edge["target"] == "30"
    assert edge["label"] == "right"
    assert edge["data"]["relationship"] == "right"


def test_serialize_avl_tree_positions_left_before_root_and_right_after_root():
    items = [
        {"id": "20", "value": 20, "label": "20", "level": 0},
        {"id": "10", "value": 10, "label": "10", "level": 1, "parentId": "20", "direction": "left"},
        {"id": "30", "value": 30, "label": "30", "level": 1, "parentId": "20", "direction": "right"},
    ]

    visualization = serialize_avl_tree(items)
    positions = {node["id"]: node["position"]["x"] for node in visualization["nodes"]}

    assert positions["10"] < positions["20"]
    assert positions["30"] > positions["20"]
