import pytest

from app.structures.btree import BTree, BTreeNode


def build_split_tree():
    tree = BTree(order=4)
    for key in [40, 20, 60, 10, 30, 50, 70]:
        tree.insert(key)
    return tree


def test_initial_tree_is_empty_with_default_order():
    tree = BTree()

    assert tree.order == 4
    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root.keys == []
    assert tree.root.leaf is True
    assert tree.height() == 0
    assert tree.levels_count() == 0
    assert tree.node_count() == 0
    assert tree.leaf_count() == 0
    assert tree.edges_count() == 0
    assert tree.split_events == []
    assert tree.levelorder() == []


def test_invalid_order_is_rejected():
    with pytest.raises(ValueError, match="INVALID_ORDER"):
        BTree(order=2)


def test_insert_first_keys_stay_in_single_multi_key_root():
    tree = BTree(order=4)

    tree.insert(20)
    tree.insert(10)
    tree.insert(30)

    assert tree.root.keys == [10, 20, 30]
    assert tree.root.leaf is True
    assert tree.size() == 3
    assert tree.height() == 0
    assert tree.levels_count() == 1
    assert tree.node_count() == 1


def test_insert_splits_full_root_and_promotes_median_key():
    tree = BTree(order=4)

    for key in [10, 20, 30, 40]:
        tree.insert(key)

    assert tree.root.keys == [20]
    assert tree.root.leaf is False
    assert tree.root.children[0].keys == [10]
    assert tree.root.children[1].keys == [30, 40]
    assert tree.size() == 4
    assert tree.height() == 1
    assert tree.levels_count() == 2
    assert tree.split_events[-1]["promotedKey"] == 20
    assert tree.split_events[-1]["before"]["keys"] == [10, 20, 30]
    assert tree.split_events[-1]["after"]["left"]["keys"] == [10]
    assert tree.split_events[-1]["after"]["right"]["keys"] == [30]


def test_insert_splits_internal_child():
    tree = build_split_tree()

    assert tree.root.keys == [40]
    assert [child.keys for child in tree.root.children] == [[10, 20, 30], [50, 60, 70]]

    tree.insert(25)

    assert tree.root.keys == [20, 40]
    assert [child.keys for child in tree.root.children] == [[10], [25, 30], [50, 60, 70]]
    assert tree.split_events[-1]["promotedKey"] == 20


def test_search_returns_match_metadata_when_key_exists():
    tree = build_split_tree()

    found = tree.search(50)

    assert found is not None
    assert found["key"] == 50
    assert found["level"] == 1
    assert found["nodeKeys"] == [50, 60, 70]
    assert found["keyIndex"] == 0
    assert found["path"][0]["keys"] == [40]


def test_search_returns_none_when_key_does_not_exist():
    tree = build_split_tree()

    assert tree.search(999) is None
    assert tree.contains(999) is False


def test_duplicate_keys_are_rejected():
    tree = BTree(order=4)
    tree.insert(10)

    with pytest.raises(ValueError, match="DUPLICATE_KEY"):
        tree.insert(10)


def test_required_key_validation():
    tree = BTree(order=4)

    with pytest.raises(ValueError, match="KEY_REQUIRED"):
        tree.insert(None)

    with pytest.raises(ValueError, match="KEY_REQUIRED"):
        tree.insert("   ")


def test_incomparable_key_validation():
    tree = BTree(order=4)
    tree.insert(10)

    with pytest.raises(ValueError, match="INCOMPARABLE_KEY"):
        tree.insert({"key": 20})


def test_levelorder_includes_visual_metadata():
    tree = build_split_tree()

    nodes = tree.levelorder()

    assert [node["keys"] for node in nodes] == [[40], [10, 20, 30], [50, 60, 70]]
    assert nodes[0]["level"] == 0
    assert nodes[0]["isRoot"] is True
    assert nodes[0]["leaf"] is False
    assert nodes[1]["parentId"] == nodes[0]["id"]
    assert nodes[1]["childIndex"] == 0
    assert nodes[1]["label"] == "10 | 20 | 30"
    assert nodes[1]["keyCount"] == 3


def test_metrics_for_split_tree():
    tree = build_split_tree()

    assert tree.size() == 7
    assert tree.height() == 1
    assert tree.levels_count() == 2
    assert tree.node_count() == 3
    assert tree.leaf_count() == 2
    assert tree.edges_count() == 2


def test_to_dict_serializes_complete_tree():
    tree = build_split_tree()

    serialized = tree.to_dict()

    assert serialized["order"] == 4
    assert serialized["size"] == 7
    assert serialized["root"]["keys"] == [40]
    assert serialized["root"]["children"][0]["keys"] == [10, 20, 30]
    assert serialized["root"]["children"][1]["keys"] == [50, 60, 70]


def test_clear_resets_tree_and_split_events():
    tree = build_split_tree()

    tree.clear()

    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root.keys == []
    assert tree.root.leaf is True
    assert tree.split_events == []


def test_node_to_dict():
    node = BTreeNode(keys=[10, 20], leaf=True)

    assert node.to_dict() == {"keys": [10, 20], "leaf": True, "children": []}
