import pytest

from app.structures.btree import BTree, BTreeNode, BTreeSearchResult


def build_sample_tree(order=4):
    tree = BTree(order=order)
    for key in [40, 20, 60, 10, 30, 50, 70, 5, 15, 25, 35]:
        tree.insert(key)
    return tree


def test_initial_tree_is_empty_with_default_order():
    tree = BTree()

    assert tree.is_empty() is True
    assert tree.root is None
    assert tree.order == 4
    assert tree.max_keys == 3
    assert tree.min_keys == 1
    assert tree.size() == 0
    assert tree.height() == 0
    assert tree.levels_count() == 0
    assert tree.node_count() == 0
    assert tree.leaf_count() == 0
    assert tree.edges_count() == 0
    assert tree.split_events == []
    assert tree.validate_invariants() is True


def test_order_must_be_integer_and_at_least_three():
    with pytest.raises(ValueError, match="ORDER_MUST_BE_INTEGER"):
        BTree(order="4")

    with pytest.raises(ValueError, match="ORDER_MUST_BE_AT_LEAST_3"):
        BTree(order=2)


def test_insert_first_key_as_root_leaf():
    tree = BTree(order=4)

    inserted = tree.insert(100)

    assert inserted == 100
    assert isinstance(tree.root, BTreeNode)
    assert tree.root.keys == [100]
    assert tree.root.leaf is True
    assert tree.size() == 1
    assert tree.height() == 0
    assert tree.levels_count() == 1
    assert tree.validate_invariants() is True


def test_insert_rejects_duplicate_keys():
    tree = BTree()
    tree.insert(10)

    with pytest.raises(ValueError, match="DUPLICATE_KEY"):
        tree.insert(10)


def test_insert_rejects_empty_keys():
    tree = BTree()

    with pytest.raises(ValueError, match="KEY_REQUIRED"):
        tree.insert("   ")

    with pytest.raises(ValueError, match="KEY_REQUIRED"):
        tree.insert(None)


def test_insert_rejects_incomparable_keys():
    tree = BTree()
    tree.insert(10)

    with pytest.raises(ValueError, match="INCOMPARABLE_KEY"):
        tree.insert({"record": 20})


def test_insert_splits_root_when_node_overflows():
    tree = BTree(order=4)

    for key in [10, 20, 30, 40]:
        tree.insert(key)

    assert tree.root.keys == [30]
    assert tree.root.leaf is False
    assert [child.keys for child in tree.root.children] == [[10, 20], [40]]
    assert tree.height() == 1
    assert tree.levels_count() == 2
    assert tree.split_events[-1]["type"] == "SPLIT"
    assert tree.split_events[-1]["beforeKeys"] == [10, 20, 30, 40]
    assert tree.split_events[-1]["promotedKey"] == 30
    assert tree.split_events[-1]["createdNewRoot"] is True
    assert tree.validate_invariants() is True


def test_insert_multiple_keys_keeps_sorted_inorder_and_invariants():
    tree = build_sample_tree()

    assert tree.inorder() == [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70]
    assert tree.size() == 11
    assert tree.validate_invariants() is True


def test_search_returns_result_metadata_when_key_exists():
    tree = build_sample_tree()

    result = tree.search(25)

    assert isinstance(result, BTreeSearchResult)
    assert result.found is True
    assert result.key == 25
    assert result.node is not None
    assert 25 in result.node.keys
    assert result.index == result.node.keys.index(25)
    assert result.level is not None
    assert result.path[0] == tree.root.keys
    assert tree.contains(25) is True


def test_search_returns_path_when_key_does_not_exist():
    tree = build_sample_tree()

    result = tree.search(999)

    assert result.found is False
    assert result.node is None
    assert result.index is None
    assert result.level is None
    assert len(result.path) >= 1
    assert tree.contains(999) is False


def test_levelorder_includes_visual_metadata():
    tree = build_sample_tree()

    levelorder = tree.levelorder()
    root_entry = levelorder[0]
    child_entry = next(item for item in levelorder if item["parentId"] == root_entry["id"])

    assert root_entry["keys"] == tree.root.keys
    assert root_entry["level"] == 0
    assert root_entry["parentId"] is None
    assert root_entry["parentKeys"] is None
    assert root_entry["childIndex"] is None
    assert root_entry["keyCount"] == len(root_entry["keys"])
    assert child_entry["level"] == 1
    assert child_entry["parentKeys"] == tree.root.keys


def test_metrics_for_sample_tree():
    tree = build_sample_tree()

    assert tree.size() == 11
    assert tree.height() >= 1
    assert tree.levels_count() == tree.height() + 1
    assert tree.node_count() == len(tree.levelorder())
    assert tree.leaf_count() > 0
    assert tree.edges_count() == tree.node_count() - 1


def test_clear_removes_keys_and_split_history():
    tree = build_sample_tree()
    assert tree.size() > 0
    assert len(tree.split_events) > 0

    tree.clear()

    assert tree.is_empty() is True
    assert tree.root is None
    assert tree.size() == 0
    assert tree.levelorder() == []
    assert tree.split_events == []
    assert tree.validate_invariants() is True


def test_to_dict_serializes_complete_state():
    tree = build_sample_tree()

    payload = tree.to_dict()

    assert payload["order"] == 4
    assert payload["maxKeys"] == 3
    assert payload["minKeys"] == 1
    assert payload["size"] == tree.size()
    assert payload["height"] == tree.height()
    assert payload["levels"] == tree.levels_count()
    assert payload["root"] == tree.root.to_dict()
    assert payload["levelorder"] == tree.levelorder()
    assert payload["splitEvents"] == tree.split_events


def test_search_result_to_dict_is_json_friendly():
    tree = build_sample_tree()
    result = tree.search(30).to_dict()

    assert result["found"] is True
    assert result["key"] == 30
    assert isinstance(result["nodeKeys"], list)
    assert isinstance(result["path"], list)


def test_order_five_supports_larger_nodes():
    tree = BTree(order=5)
    for key in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        tree.insert(key)

    assert tree.order == 5
    assert tree.max_keys == 4
    assert tree.min_keys == 2
    assert tree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert all(len(node.keys) <= 4 for node in tree.levelorder_nodes())
    assert tree.validate_invariants() is True
