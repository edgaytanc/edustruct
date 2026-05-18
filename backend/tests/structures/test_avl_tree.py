import pytest

from app.structures.avl_tree import AVLNode, AVLTree


def assert_all_nodes_balanced(tree):
    for node in tree.preorder_nodes():
        assert abs(node.balance_factor()) <= 1


def build_sample_tree():
    tree = AVLTree()
    for value in [50, 25, 75, 10, 40, 60, 90]:
        tree.insert(value)
    return tree


def test_initial_tree_is_empty():
    tree = AVLTree()

    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root is None
    assert tree.height() == 0
    assert tree.levels_count() == 0
    assert tree.leaf_count() == 0
    assert tree.edges_count() == 0
    assert tree.balance_factor() == 0
    assert tree.is_balanced() is True
    assert tree.rotation_events == []


def test_insert_first_value_as_root():
    tree = AVLTree()

    inserted = tree.insert(50)

    assert isinstance(inserted, AVLNode)
    assert tree.root is inserted
    assert tree.root.value == 50
    assert tree.root.height == 1
    assert tree.size() == 1
    assert tree.height() == 0
    assert tree.levels_count() == 1


def test_insert_preserves_bst_ordering():
    tree = build_sample_tree()

    assert [item["value"] for item in tree.inorder()] == [10, 25, 40, 50, 60, 75, 90]
    assert tree.root.value == 50
    assert_all_nodes_balanced(tree)


def test_insert_rejects_duplicate_values():
    tree = AVLTree()
    tree.insert(50)

    with pytest.raises(ValueError, match="DUPLICATE_VALUE"):
        tree.insert(50)


def test_insert_rejects_empty_string_values():
    tree = AVLTree()

    with pytest.raises(ValueError, match="VALUE_REQUIRED"):
        tree.insert("   ")


def test_insert_rejects_incomparable_values():
    tree = AVLTree()
    tree.insert(10)

    with pytest.raises(ValueError, match="INCOMPARABLE_VALUE"):
        tree.insert({"value": 20})


def test_ll_rotation_is_registered_and_balances_tree():
    tree = AVLTree()

    for value in [30, 20, 10]:
        tree.insert(value)

    assert tree.root.value == 20
    assert [item["value"] for item in tree.levelorder()] == [20, 10, 30]
    assert tree.rotation_events[-1]["type"] == "LL"
    assert tree.rotation_events[-1]["pivot"] == 30
    assert tree.rotation_events[-1]["before"]["value"] == 30
    assert tree.rotation_events[-1]["after"]["value"] == 20
    assert_all_nodes_balanced(tree)


def test_rr_rotation_is_registered_and_balances_tree():
    tree = AVLTree()

    for value in [10, 20, 30]:
        tree.insert(value)

    assert tree.root.value == 20
    assert [item["value"] for item in tree.levelorder()] == [20, 10, 30]
    assert tree.rotation_events[-1]["type"] == "RR"
    assert tree.rotation_events[-1]["pivot"] == 10
    assert tree.rotation_events[-1]["before"]["value"] == 10
    assert tree.rotation_events[-1]["after"]["value"] == 20
    assert_all_nodes_balanced(tree)


def test_lr_rotation_is_registered_and_balances_tree():
    tree = AVLTree()

    for value in [30, 10, 20]:
        tree.insert(value)

    assert tree.root.value == 20
    assert [item["value"] for item in tree.levelorder()] == [20, 10, 30]
    assert tree.rotation_events[-1]["type"] == "LR"
    assert tree.rotation_events[-1]["pivot"] == 30
    assert tree.rotation_events[-1]["before"]["value"] == 30
    assert tree.rotation_events[-1]["after"]["value"] == 20
    assert_all_nodes_balanced(tree)


def test_rl_rotation_is_registered_and_balances_tree():
    tree = AVLTree()

    for value in [10, 30, 20]:
        tree.insert(value)

    assert tree.root.value == 20
    assert [item["value"] for item in tree.levelorder()] == [20, 10, 30]
    assert tree.rotation_events[-1]["type"] == "RL"
    assert tree.rotation_events[-1]["pivot"] == 10
    assert tree.rotation_events[-1]["before"]["value"] == 10
    assert tree.rotation_events[-1]["after"]["value"] == 20
    assert_all_nodes_balanced(tree)


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


def test_levelorder_includes_avl_metadata():
    tree = build_sample_tree()

    levelorder = tree.levelorder()
    node_40 = next(item for item in levelorder if item["value"] == 40)

    assert node_40["level"] == 2
    assert node_40["parentValue"] == 25
    assert node_40["parentId"] == "25"
    assert node_40["direction"] == "right"
    assert node_40["height"] == 1
    assert node_40["visualHeight"] == 0
    assert node_40["balanceFactor"] == 0
    assert node_40["isUnbalanced"] is False


def test_metrics_for_balanced_sample_tree():
    tree = build_sample_tree()

    assert tree.size() == 7
    assert tree.height() == 2
    assert tree.levels_count() == 3
    assert tree.leaf_count() == 4
    assert tree.edges_count() == 6
    assert tree.balance_factor() == 0
    assert tree.is_balanced() is True


def test_delete_leaf_node_keeps_tree_balanced():
    tree = build_sample_tree()

    deleted = tree.delete(10)

    assert deleted.value == 10
    assert tree.size() == 6
    assert tree.search(10) is None
    assert [item["value"] for item in tree.inorder()] == [25, 40, 50, 60, 75, 90]
    assert_all_nodes_balanced(tree)


def test_delete_node_with_one_child_keeps_tree_balanced():
    tree = AVLTree()
    for value in [50, 25, 10]:
        tree.insert(value)

    deleted = tree.delete(25)

    assert deleted.value == 25
    assert tree.size() == 2
    assert [item["value"] for item in tree.inorder()] == [10, 50]
    assert_all_nodes_balanced(tree)


def test_delete_node_with_two_children_uses_inorder_successor():
    tree = build_sample_tree()

    deleted = tree.delete(25)

    assert deleted.value == 25
    assert tree.root.left.value == 40
    assert tree.size() == 6
    assert [item["value"] for item in tree.inorder()] == [10, 40, 50, 60, 75, 90]
    assert_all_nodes_balanced(tree)


def test_delete_can_trigger_rebalancing_rotation():
    tree = AVLTree()
    for value in [50, 30, 70, 20, 40, 60, 80, 10]:
        tree.insert(value)

    deleted = tree.delete(80)

    assert deleted.value == 80
    assert tree.is_balanced() is True
    assert [item["value"] for item in tree.inorder()] == [10, 20, 30, 40, 50, 60, 70]
    assert_all_nodes_balanced(tree)


def test_delete_missing_value_returns_none_and_preserves_size():
    tree = build_sample_tree()

    deleted = tree.delete(999)

    assert deleted is None
    assert tree.size() == 7
    assert tree.rotation_events == []


def test_to_dict_serializes_tree_state_and_avl_metadata():
    tree = build_sample_tree()

    data = tree.to_dict()

    assert data["type"] == "avl-tree"
    assert data["root"]["value"] == 50
    assert data["root"]["height"] == 3
    assert data["root"]["balanceFactor"] == 0
    assert data["root"]["isUnbalanced"] is False
    assert data["size"] == 7
    assert data["height"] == 2
    assert data["levels"] == 3
    assert data["isBalanced"] is True
    assert data["rotationEvents"] == []


def test_clear_removes_all_nodes_and_events():
    tree = AVLTree()
    for value in [30, 20, 10]:
        tree.insert(value)

    assert tree.rotation_events != []

    tree.clear()

    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root is None
    assert tree.levelorder() == []
    assert tree.rotation_events == []
