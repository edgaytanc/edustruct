import sys
from pathlib import Path

import pytest

STRUCTURES_PATH = Path(__file__).resolve().parents[2] / "app" / "structures"
sys.path.insert(0, str(STRUCTURES_PATH))

from stack import Stack


def test_new_stack_starts_empty():
    stack = Stack()

    assert stack.is_empty() is True
    assert stack.size() == 0
    assert stack.to_list() == []


def test_push_adds_values_to_top():
    stack = Stack()

    stack.push("page-1")
    stack.push("page-2")
    stack.push("page-3")

    assert stack.size() == 3
    assert stack.peek() == "page-3"
    assert stack.to_list() == ["page-3", "page-2", "page-1"]


def test_pop_removes_values_in_lifo_order():
    stack = Stack()

    stack.push("step-1")
    stack.push("step-2")
    stack.push("step-3")

    assert stack.pop() == "step-3"
    assert stack.pop() == "step-2"
    assert stack.pop() == "step-1"
    assert stack.is_empty() is True


def test_peek_does_not_remove_value():
    stack = Stack()

    stack.push("current-action")

    assert stack.peek() == "current-action"
    assert stack.peek() == "current-action"
    assert stack.size() == 1


def test_pop_empty_stack_raises_error():
    stack = Stack()

    with pytest.raises(IndexError):
        stack.pop()


def test_peek_empty_stack_raises_error():
    stack = Stack()

    with pytest.raises(IndexError):
        stack.peek()


def test_clear_resets_stack():
    stack = Stack()

    stack.push("A")
    stack.push("B")
    stack.clear()

    assert stack.is_empty() is True
    assert stack.size() == 0
    assert stack.to_list() == []
