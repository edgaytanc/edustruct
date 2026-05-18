import pytest

from app.structures.general_tree import GeneralTree, GeneralTreeNode


def build_sample_tree():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad", category="faculty")
    tree.insert("career", "Carrera", parent_id="faculty", category="career")
    tree.insert("cycle-1", "Ciclo 1", parent_id="career", category="cycle")
    tree.insert("math-1", "Matemática I", parent_id="cycle-1", category="course")
    tree.insert("programming-1", "Programación I", parent_id="cycle-1", category="course")
    tree.insert("cycle-2", "Ciclo 2", parent_id="career", category="cycle")
    return tree


def test_insert_root_and_children_by_parent_id():
    tree = GeneralTree()

    tree.insert("faculty", "Facultad")
    tree.insert("career", "Carrera", parent_id="faculty")
    tree.insert("cycle-1", "Ciclo 1", parent_id="career")

    assert tree.size() == 3
    assert tree.root.node_id == "faculty"
    assert tree.search("career").label == "Carrera"
    assert tree.search("cycle-1").label == "Ciclo 1"


def test_insert_root_preserves_category_and_metadata():
    tree = GeneralTree()

    inserted = tree.insert(
        "faculty",
        "Facultad de Ingeniería",
        category="faculty",
        metadata={"entity": "faculty", "campus": "central"},
    )

    assert inserted.category == "faculty"
    assert inserted.metadata["entity"] == "faculty"
    assert inserted.metadata["campus"] == "central"
    assert tree.to_dict()["root"]["metadata"]["campus"] == "central"


def test_insert_duplicate_id_raises_value_error():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")

    with pytest.raises(ValueError, match="DUPLICATE_NODE_ID"):
        tree.insert("faculty", "Facultad repetida", parent_id="faculty")


def test_insert_without_parent_when_tree_has_root_raises_value_error():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")

    with pytest.raises(ValueError, match="PARENT_REQUIRED"):
        tree.insert("career", "Carrera")


def test_insert_with_missing_parent_raises_value_error():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")

    with pytest.raises(ValueError, match="PARENT_NOT_FOUND"):
        tree.insert("career", "Carrera", parent_id="missing")


def test_insert_root_with_parent_id_on_empty_tree_raises_value_error():
    tree = GeneralTree()

    with pytest.raises(ValueError, match="PARENT_NOT_FOUND"):
        tree.insert("career", "Carrera", parent_id="faculty")


def test_delete_node_removes_full_subtree():
    tree = build_sample_tree()

    removed = tree.delete("cycle-1")

    assert removed.node_id == "cycle-1"
    assert tree.size() == 3
    assert tree.search("cycle-1") is None
    assert tree.search("math-1") is None
    assert tree.search("programming-1") is None
    assert tree.search("cycle-2") is not None


def test_delete_root_clears_tree_and_returns_removed_root():
    tree = build_sample_tree()

    removed = tree.delete("faculty")

    assert removed.node_id == "faculty"
    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.root is None
    assert tree.levelorder() == []


def test_delete_missing_node_returns_none_without_changing_tree():
    tree = build_sample_tree()

    removed = tree.delete("missing")

    assert removed is None
    assert tree.size() == 6
    assert tree.root.node_id == "faculty"


def test_search_and_contains_behaviour():
    tree = build_sample_tree()

    assert tree.contains("math-1") is True
    assert tree.search("math-1").label == "Matemática I"
    assert tree.contains("missing") is False
    assert tree.search("missing") is None


def test_preorder_postorder_and_levelorder():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")
    tree.insert("career", "Carrera", parent_id="faculty")
    tree.insert("cycle-1", "Ciclo 1", parent_id="career")
    tree.insert("cycle-2", "Ciclo 2", parent_id="career")

    assert [item["id"] for item in tree.preorder()] == [
        "faculty",
        "career",
        "cycle-1",
        "cycle-2",
    ]
    assert [item["id"] for item in tree.postorder()] == [
        "cycle-1",
        "cycle-2",
        "career",
        "faculty",
    ]
    assert [item["id"] for item in tree.levelorder()] == [
        "faculty",
        "career",
        "cycle-1",
        "cycle-2",
    ]


def test_levelorder_includes_parent_id_and_level_metadata():
    tree = build_sample_tree()

    levelorder = tree.levelorder()
    math_node = next(item for item in levelorder if item["id"] == "math-1")

    assert levelorder[0]["id"] == "faculty"
    assert "parentId" not in levelorder[0]
    assert math_node["level"] == 3
    assert math_node["parentId"] == "cycle-1"


def test_height_levels_leaf_count_and_max_children():
    tree = build_sample_tree()

    assert tree.height() == 3
    assert tree.levels_count() == 4
    assert tree.leaf_count() == 3
    assert tree.max_children() == 2
    assert tree.get_level("math-1") == 3


def test_empty_tree_metrics_are_zero_based():
    tree = GeneralTree()

    assert tree.is_empty() is True
    assert tree.size() == 0
    assert tree.height() == 0
    assert tree.levels_count() == 0
    assert tree.leaf_count() == 0
    assert tree.max_children() == 0
    assert tree.get_level("missing") is None


def test_node_to_dict_serializes_full_subtree():
    root = GeneralTreeNode("faculty", "Facultad", category="faculty")
    child = GeneralTreeNode("career", "Carrera", category="career")
    root.add_child(child)

    assert root.to_dict() == {
        "id": "faculty",
        "label": "Facultad",
        "category": "faculty",
        "metadata": {},
        "children": [
            {
                "id": "career",
                "label": "Carrera",
                "category": "career",
                "metadata": {},
                "children": [],
            }
        ],
    }
