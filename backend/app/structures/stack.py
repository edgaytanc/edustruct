"""
Stack implementation for EduStruct.

The stack uses LIFO behavior and delegates storage to the manual linked list.
This module must remain independent from Flask.
"""

from __future__ import annotations

from typing import Any

try:
    from .list_model import LinkedList
except ImportError:  # Allows direct execution in isolated unit tests.
    from list_model import LinkedList


class Stack:
    """Manual stack implemented on top of LinkedList."""

    def __init__(self) -> None:
        self._items = LinkedList()

    def __len__(self) -> int:
        return self.size()

    def push(self, value: Any) -> None:
        """Insert a value on top of the stack in O(1)."""
        self._items.prepend(value)

    def pop(self) -> Any:
        """Remove and return the value from the top of the stack in O(1)."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")

        return self._items.pop_front()

    def peek(self) -> Any:
        """Return the top value without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek an empty stack.")

        return self._items.get_at(0)

    def is_empty(self) -> bool:
        """Return True when the stack has no values."""
        return self._items.is_empty()

    def size(self) -> int:
        """Return the number of values stored in the stack."""
        return self._items.size()

    def clear(self) -> None:
        """Remove all values from the stack."""
        self._items.clear()

    def to_list(self) -> list[Any]:
        """
        Return the stack as a plain list from top to bottom.

        This representation is useful for JSON serialization and future UI views.
        """
        return self._items.to_list()
