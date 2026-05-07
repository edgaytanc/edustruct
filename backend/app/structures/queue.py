"""
Queue implementation for EduStruct.

The queue uses FIFO behavior and delegates storage to the manual linked list.
This module must remain independent from Flask.
"""

from __future__ import annotations

from typing import Any

try:
    from .list_model import LinkedList
except ImportError:  # Allows direct execution in isolated unit tests.
    from list_model import LinkedList


class Queue:
    """Manual queue implemented on top of LinkedList."""

    def __init__(self) -> None:
        self._items = LinkedList()

    def __len__(self) -> int:
        return self.size()

    def enqueue(self, value: Any) -> None:
        """Insert a value at the rear of the queue in O(1)."""
        self._items.append(value)

    def dequeue(self) -> Any:
        """Remove and return the value from the front of the queue in O(1)."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")

        return self._items.pop_front()

    def front(self) -> Any:
        """Return the front value without removing it."""
        if self.is_empty():
            raise IndexError("Cannot inspect the front of an empty queue.")

        return self._items.get_at(0)

    def is_empty(self) -> bool:
        """Return True when the queue has no values."""
        return self._items.is_empty()

    def size(self) -> int:
        """Return the number of values stored in the queue."""
        return self._items.size()

    def clear(self) -> None:
        """Remove all values from the queue."""
        self._items.clear()

    def to_list(self) -> list[Any]:
        """
        Return the queue as a plain list from front to rear.

        This representation is useful for JSON serialization and future UI views.
        """
        return self._items.to_list()
