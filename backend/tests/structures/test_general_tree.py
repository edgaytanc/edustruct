import pytest

from app.structures.general_tree import GeneralTree


def test_insert_root_and_children_by_parent_id():
    tree = GeneralTree()

    tree.insert("faculty", "Facultad")
    tree.insert("career", "Carrera", parent_id="faculty")
    tree.insert("cycle-1", "Ciclo 1", parent_id="career")

    assert tree.size() == 3
    assert tree.root.node_id == "faculty"
    assert tree.search("career").label == "Carrera"
    assert tree.search("cycle-1").label == "Ciclo 1"


def test_insert_duplicate_id_raises_value_error():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")

    with pytest.raises(ValueError):
        tree.insert("faculty", "Facultad repetida", parent_id="faculty")


def test_insert_without_parent_when_tree_has_root_raises_value_error():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")

    with pytest.raises(ValueError):
        tree.insert("career", "Carrera")


def test_delete_node_removes_full_subtree():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")
    tree.insert("career", "Carrera", parent_id="faculty")
    tree.insert("cycle-1", "Ciclo 1", parent_id="career")
    tree.insert("math-1", "Matemática I", parent_id="cycle-1")

    removed = tree.delete("career")

    assert removed.node_id == "career"
    assert tree.size() == 1
    assert tree.search("career") is None
    assert tree.search("math-1") is None


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


def test_height_levels_leaf_count_and_max_children():
    tree = GeneralTree()
    tree.insert("faculty", "Facultad")
    tree.insert("career", "Carrera", parent_id="faculty")
    tree.insert("cycle-1", "Ciclo 1", parent_id="career")
    tree.insert("cycle-2", "Ciclo 2", parent_id="career")
    tree.insert("math-1", "Matemática I", parent_id="cycle-1")

    assert tree.height() == 3
    assert tree.levels_count() == 4
    assert tree.leaf_count() == 2
    assert tree.max_children() == 2
    assert tree.get_level("math-1") == 3
