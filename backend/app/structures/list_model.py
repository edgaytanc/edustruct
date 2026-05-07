"""
Singly linked list implementation for EduStruct.

This module belongs to the pure data-structures layer. It must not import
Flask, serializers, routes, services, or any HTTP-related dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Optional


@dataclass
class ListNode:
    """Node used by the singly linked list."""

    value: Any
    next: Optional["ListNode"] = None


class LinkedList:
    """
    Manual singly linked list.

    Responsibilities:
    - Store values using custom nodes.
    - Support insertion, deletion, search, traversal, and reset operations.
    - Provide a reusable base for stack and queue structures.
    """

    def __init__(self) -> None:
        self._head: Optional[ListNode] = None
        self._tail: Optional[ListNode] = None
        self._size: int = 0

    @property
    def head(self) -> Optional[ListNode]:
        """Return the first node of the list."""
        return self._head

    @property
    def tail(self) -> Optional[ListNode]:
        """Return the last node of the list."""
        return self._tail

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def is_empty(self) -> bool:
        """Return True when the list has no elements."""
        return self._size == 0

    def size(self) -> int:
        """Return the number of elements stored in the list."""
        return self._size

    def prepend(self, value: Any) -> None:
        """Insert a value at the beginning of the list in O(1)."""
        new_node = ListNode(value=value, next=self._head)
        self._head = new_node

        if self._tail is None:
            self._tail = new_node

        self._size += 1

    def append(self, value: Any) -> None:
        """Insert a value at the end of the list in O(1)."""
        new_node = ListNode(value=value)

        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def insert_at(self, index: int, value: Any) -> None:
        """Insert a value at the provided zero-based index."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range.")

        if index == 0:
            self.prepend(value)
            return

        if index == self._size:
            self.append(value)
            return

        previous = self._node_at(index - 1)
        new_node = ListNode(value=value, next=previous.next)
        previous.next = new_node
        self._size += 1

    def remove(self, value: Any) -> bool:
        """
        Remove the first node matching value.

        Returns True when a node was removed, otherwise False.
        """
        if self._head is None:
            return False

        if self._head.value == value:
            self.pop_front()
            return True

        previous = self._head
        current = self._head.next

        while current is not None:
            if current.value == value:
                previous.next = current.next

                if current is self._tail:
                    self._tail = previous

                self._size -= 1
                return True

            previous = current
            current = current.next

        return False

    def pop_front(self) -> Any:
        """Remove and return the first value of the list in O(1)."""
        if self._head is None:
            raise IndexError("Cannot remove from an empty list.")

        removed_node = self._head
        self._head = removed_node.next

        if self._head is None:
            self._tail = None

        self._size -= 1
        return removed_node.value

    def get_at(self, index: int) -> Any:
        """Return the value stored at the provided zero-based index."""
        return self._node_at(index).value

    def find(self, value: Any) -> Optional[Any]:
        """Return the first matching value or None when it does not exist."""
        current = self._head

        while current is not None:
            if current.value == value:
                return current.value
            current = current.next

        return None

    def contains(self, value: Any) -> bool:
        """Return True when value exists in the list."""
        return self.find(value) is not None

    def clear(self) -> None:
        """Remove all values from the list."""
        self._head = None
        self._tail = None
        self._size = 0

    def to_list(self) -> list[Any]:
        """Return a plain Python list representation for JSON serialization."""
        return [value for value in self]

    def _node_at(self, index: int) -> ListNode:
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range.")

        current = self._head
        current_index = 0

        while current is not None:
            if current_index == index:
                return current
            current = current.next
            current_index += 1

        raise IndexError("Index out of range.")
