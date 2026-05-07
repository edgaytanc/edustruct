import importlib.util
import sys
from pathlib import Path

import pytest

STRUCTURES_PATH = Path(__file__).resolve().parents[2] / "app" / "structures"
sys.path.insert(0, str(STRUCTURES_PATH))

QUEUE_MODULE_PATH = STRUCTURES_PATH / "queue.py"
spec = importlib.util.spec_from_file_location("edustruct_queue", QUEUE_MODULE_PATH)
queue_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue_module)
Queue = queue_module.Queue


def test_new_queue_starts_empty():
    queue = Queue()

    assert queue.is_empty() is True
    assert queue.size() == 0
    assert queue.to_list() == []


def test_enqueue_adds_values_to_rear():
    queue = Queue()

    queue.enqueue("student-1")
    queue.enqueue("student-2")
    queue.enqueue("student-3")

    assert queue.size() == 3
    assert queue.front() == "student-1"
    assert queue.to_list() == ["student-1", "student-2", "student-3"]


def test_dequeue_removes_values_in_fifo_order():
    queue = Queue()

    queue.enqueue("turn-1")
    queue.enqueue("turn-2")
    queue.enqueue("turn-3")

    assert queue.dequeue() == "turn-1"
    assert queue.dequeue() == "turn-2"
    assert queue.dequeue() == "turn-3"
    assert queue.is_empty() is True


def test_front_does_not_remove_value():
    queue = Queue()

    queue.enqueue("next-student")

    assert queue.front() == "next-student"
    assert queue.front() == "next-student"
    assert queue.size() == 1


def test_dequeue_empty_queue_raises_error():
    queue = Queue()

    with pytest.raises(IndexError):
        queue.dequeue()


def test_front_empty_queue_raises_error():
    queue = Queue()

    with pytest.raises(IndexError):
        queue.front()


def test_clear_resets_queue():
    queue = Queue()

    queue.enqueue("A")
    queue.enqueue("B")
    queue.clear()

    assert queue.is_empty() is True
    assert queue.size() == 0
    assert queue.to_list() == []
