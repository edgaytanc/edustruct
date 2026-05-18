import pytest

from app.structures.binary_tree import BinaryTree, BinaryTreeNode


def build_sample_tree():
    tree = BinaryTree()
    for value in [50, 25, 75, 10, 40, 60, 90]:
        tree.insert(value)
    return tree


def test_initial_tree_is_empty():
    tree = BinaryTree()

    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root is None
    assert tree.height() == 0
    assert tree.levels_count() == 0
    assert tree.leaf_count() == 0
    assert tree.edges_count() == 0


def test_insert_first_value_as_root():
    tree = BinaryTree()

    inserted = tree.insert(50)

    assert isinstance(inserted, BinaryTreeNode)
    assert tree.root is inserted
    assert tree.root.value == 50
    assert tree.size() == 1
    assert tree.height() == 0
    assert tree.levels_count() == 1


def test_insert_preserves_bst_ordering():
    tree = build_sample_tree()

    assert tree.root.value == 50
    assert tree.root.left.value == 25
    assert tree.root.right.value == 75
    assert tree.root.left.left.value == 10
    assert tree.root.left.right.value == 40
    assert tree.root.right.left.value == 60
    assert tree.root.right.right.value == 90


def test_insert_rejects_duplicate_values():
    tree = BinaryTree()
    tree.insert(50)

    with pytest.raises(ValueError, match="DUPLICATE_VALUE"):
        tree.insert(50)


def test_insert_rejects_empty_string_values():
    tree = BinaryTree()

    with pytest.raises(ValueError, match="VALUE_REQUIRED"):
        tree.insert("   ")


def test_insert_rejects_incomparable_values():
    tree = BinaryTree()
    tree.insert(10)

    with pytest.raises(ValueError, match="INCOMPARABLE_VALUE"):
        tree.insert({"value": 20})


def test_search_returns_node_when_value_exists():
    tree = build_sample_tree()

    found = tree.search(40)

    assert found is not None
    assert found.value == 40
    assert tree.contains(40) is True


def test_search_returns_none_when_value_does_not_exist():
    tree = build_sample_tree()

    assert tree.search(999) is None
    assert tree.contains(999) is False


def test_get_level_returns_zero_based_level():
    tree = build_sample_tree()

    assert tree.get_level(50) == 0
    assert tree.get_level(25) == 1
    assert tree.get_level(10) == 2
    assert tree.get_level(999) is None


def test_traversals_return_expected_order():
    tree = build_sample_tree()

    assert [item["value"] for item in tree.preorder()] == [50, 25, 10, 40, 75, 60, 90]
    assert [item["value"] for item in tree.inorder()] == [10, 25, 40, 50, 60, 75, 90]
    assert [item["value"] for item in tree.postorder()] == [10, 40, 25, 60, 90, 75, 50]
    assert [item["value"] for item in tree.levelorder()] == [50, 25, 75, 10, 40, 60, 90]


def test_levelorder_includes_level_parent_and_direction_metadata():
    tree = build_sample_tree()

    levelorder = tree.levelorder()
    node_40 = next(item for item in levelorder if item["value"] == 40)
    node_60 = next(item for item in levelorder if item["value"] == 60)

    assert node_40["level"] == 2
    assert node_40["parentValue"] == 25
    assert node_40["parentId"] == "25"
    assert node_40["direction"] == "right"
    assert node_60["direction"] == "left"


def test_metrics_for_balanced_sample_tree():
    tree = build_sample_tree()

    assert tree.size() == 7
    assert tree.height() == 2
    assert tree.levels_count() == 3
    assert tree.leaf_count() == 4
    assert tree.edges_count() == 6
    assert tree.balance_factor() == 0


def test_delete_leaf_node():
    tree = build_sample_tree()

    deleted = tree.delete(10)

    assert deleted.value == 10
    assert tree.size() == 6
    assert tree.search(10) is None
    assert [item["value"] for item in tree.inorder()] == [25, 40, 50, 60, 75, 90]


def test_delete_node_with_one_child():
    tree = BinaryTree()
    for value in [50, 25, 10]:
        tree.insert(value)

    deleted = tree.delete(25)

    assert deleted.value == 25
    assert tree.root.left.value == 10
    assert tree.size() == 2
    assert [item["value"] for item in tree.inorder()] == [10, 50]


def test_delete_node_with_two_children_uses_inorder_successor():
    tree = build_sample_tree()

    deleted = tree.delete(25)

    assert deleted.value == 25
    assert tree.root.left.value == 40
    assert tree.size() == 6
    assert [item["value"] for item in tree.inorder()] == [10, 40, 50, 60, 75, 90]


def test_delete_root_with_two_children():
    tree = build_sample_tree()

    deleted = tree.delete(50)

    assert deleted.value == 50
    assert tree.root.value == 60
    assert tree.size() == 6
    assert [item["value"] for item in tree.inorder()] == [10, 25, 40, 60, 75, 90]


def test_delete_missing_value_returns_none():
    tree = build_sample_tree()

    deleted = tree.delete(999)

    assert deleted is None
    assert tree.size() == 7


def test_to_dict_serializes_tree_state():
    tree = build_sample_tree()

    data = tree.to_dict()

    assert data["type"] == "binary-search-tree"
    assert data["root"]["value"] == 50
    assert data["size"] == 7
    assert data["height"] == 2
    assert data["levels"] == 3


def test_clear_removes_all_nodes():
    tree = build_sample_tree()

    tree.clear()

    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root is None
    assert tree.levelorder() == []
