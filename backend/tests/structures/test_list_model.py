import sys
from pathlib import Path

import pytest

STRUCTURES_PATH = Path(__file__).resolve().parents[2] / "app" / "structures"
sys.path.insert(0, str(STRUCTURES_PATH))

from list_model import LinkedList


def test_new_list_starts_empty():
    linked_list = LinkedList()

    assert linked_list.is_empty() is True
    assert linked_list.size() == 0
    assert linked_list.to_list() == []
    assert linked_list.head is None
    assert linked_list.tail is None


def test_append_adds_values_in_insertion_order():
    linked_list = LinkedList()

    linked_list.append("student-1")
    linked_list.append("student-2")
    linked_list.append("student-3")

    assert linked_list.size() == 3
    assert linked_list.to_list() == ["student-1", "student-2", "student-3"]
    assert linked_list.head.value == "student-1"
    assert linked_list.tail.value == "student-3"


def test_prepend_adds_values_at_the_beginning():
    linked_list = LinkedList()

    linked_list.prepend("course-3")
    linked_list.prepend("course-2")
    linked_list.prepend("course-1")

    assert linked_list.to_list() == ["course-1", "course-2", "course-3"]
    assert linked_list.head.value == "course-1"
    assert linked_list.tail.value == "course-3"


def test_insert_at_valid_positions():
    linked_list = LinkedList()

    linked_list.append("A")
    linked_list.append("C")
    linked_list.insert_at(1, "B")
    linked_list.insert_at(0, "START")
    linked_list.insert_at(4, "END")

    assert linked_list.to_list() == ["START", "A", "B", "C", "END"]


def test_insert_at_invalid_position_raises_error():
    linked_list = LinkedList()

    with pytest.raises(IndexError):
        linked_list.insert_at(1, "invalid")

    with pytest.raises(IndexError):
        linked_list.insert_at(-1, "invalid")


def test_remove_existing_value():
    linked_list = LinkedList()

    linked_list.append("A")
    linked_list.append("B")
    linked_list.append("C")

    removed = linked_list.remove("B")

    assert removed is True
    assert linked_list.to_list() == ["A", "C"]
    assert linked_list.size() == 2


def test_remove_head_and_tail_updates_references():
    linked_list = LinkedList()

    linked_list.append("A")
    linked_list.append("B")
    linked_list.append("C")

    assert linked_list.remove("A") is True
    assert linked_list.head.value == "B"

    assert linked_list.remove("C") is True
    assert linked_list.tail.value == "B"
    assert linked_list.to_list() == ["B"]


def test_remove_missing_value_returns_false():
    linked_list = LinkedList()

    linked_list.append("A")

    assert linked_list.remove("missing") is False
    assert linked_list.to_list() == ["A"]


def test_pop_front_removes_first_value():
    linked_list = LinkedList()

    linked_list.append("first")
    linked_list.append("second")

    assert linked_list.pop_front() == "first"
    assert linked_list.to_list() == ["second"]
    assert linked_list.size() == 1


def test_pop_front_empty_list_raises_error():
    linked_list = LinkedList()

    with pytest.raises(IndexError):
        linked_list.pop_front()


def test_find_and_contains():
    linked_list = LinkedList()

    linked_list.append("record-1")
    linked_list.append("record-2")

    assert linked_list.find("record-2") == "record-2"
    assert linked_list.find("record-3") is None
    assert linked_list.contains("record-1") is True
    assert linked_list.contains("record-3") is False


def test_get_at_returns_value_by_index():
    linked_list = LinkedList()

    linked_list.append("zero")
    linked_list.append("one")

    assert linked_list.get_at(0) == "zero"
    assert linked_list.get_at(1) == "one"

    with pytest.raises(IndexError):
        linked_list.get_at(2)


def test_clear_resets_list():
    linked_list = LinkedList()

    linked_list.append("A")
    linked_list.append("B")
    linked_list.clear()

    assert linked_list.is_empty() is True
    assert linked_list.size() == 0
    assert linked_list.to_list() == []
    assert linked_list.head is None
    assert linked_list.tail is None
