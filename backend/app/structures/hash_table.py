"""
Manual hash table implementation for EduStruct.

This module implements a real hash table using separate chaining for
collisions. It intentionally does not use ``dict`` as the internal storage
mechanism. Buckets are represented with a native Python list and every
collision chain is built manually with linked ``HashEntry`` nodes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class HashEntry:
    """Linked entry stored inside a hash table bucket."""

    key: str
    value: Any
    next: Optional["HashEntry"] = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of this entry only."""
        return {
            "key": self.key,
            "value": self.value,
            "hasNext": self.next is not None,
        }


@dataclass
class HashSearchResult:
    """Detailed result returned by hash table searches."""

    found: bool
    key: str
    bucket_index: int
    value: Any = None
    comparisons: int = 0
    chain_position: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly search result."""
        return {
            "found": self.found,
            "key": self.key,
            "bucketIndex": self.bucket_index,
            "value": self.value,
            "comparisons": self.comparisons,
            "chainPosition": self.chain_position,
        }


class HashTable:
    """
    Manual hash table using separate chaining.

    The table is designed for educational visualization. Capacity is fixed by
    default so collisions remain visible and explainable during demonstrations.
    """

    def __init__(self, capacity: int = 7) -> None:
        self._validate_capacity(capacity)
        self._capacity = capacity
        self._buckets: list[Optional[HashEntry]] = [None for _ in range(capacity)]
        self._size = 0
        self._collisions = 0
        self._last_operation: Optional[dict[str, Any]] = None

    @property
    def capacity(self) -> int:
        """Return the number of buckets in the table."""
        return self._capacity

    @property
    def buckets(self) -> list[Optional[HashEntry]]:
        """Return the internal bucket list for serializers and tests."""
        return self._buckets

    @property
    def collisions(self) -> int:
        """Return the number of insertions that collided with an occupied bucket."""
        return self._collisions

    @property
    def last_operation(self) -> Optional[dict[str, Any]]:
        """Return metadata for the last mutating/search operation."""
        if self._last_operation is None:
            return None
        return dict(self._last_operation)

    def size(self) -> int:
        """Return the number of stored entries."""
        return self._size

    def is_empty(self) -> bool:
        """Return True when no entries are stored."""
        return self._size == 0

    def load_factor(self) -> float:
        """Return the current load factor rounded to four decimals."""
        return round(self._size / self._capacity, 4)

    def hash_function(self, key: Any) -> int:
        """
        Compute a deterministic bucket index for a key.

        The function uses a weighted character sum. It is intentionally simple
        enough to defend in class and deterministic across Python executions,
        unlike Python's built-in ``hash`` for strings.
        """
        normalized_key = self._normalize_key(key)
        total = 0
        for index, character in enumerate(normalized_key, start=1):
            total += index * ord(character)
        return total % self._capacity

    def insert(self, key: Any, value: Any) -> HashEntry:
        """
        Insert a new key/value pair.

        Duplicate keys are rejected because carnets must be unique in the
        educational domain and stable in the visualization.
        """
        normalized_key = self._normalize_key(key)
        bucket_index = self.hash_function(normalized_key)
        current = self._buckets[bucket_index]

        if current is None:
            entry = HashEntry(normalized_key, value)
            self._buckets[bucket_index] = entry
            self._size += 1
            self._last_operation = self._operation_payload(
                operation="INSERT",
                key=normalized_key,
                bucket_index=bucket_index,
                collision=False,
                chain_position=0,
            )
            return entry

        position = 0
        tail = current
        while tail is not None:
            if tail.key == normalized_key:
                raise ValueError("DUPLICATE_KEY")
            if tail.next is None:
                break
            tail = tail.next
            position += 1

        entry = HashEntry(normalized_key, value)
        tail.next = entry
        self._size += 1
        self._collisions += 1
        self._last_operation = self._operation_payload(
            operation="INSERT",
            key=normalized_key,
            bucket_index=bucket_index,
            collision=True,
            chain_position=position + 1,
        )
        return entry

    def search(self, key: Any) -> HashSearchResult:
        """Search a key and return bucket/chain metadata."""
        normalized_key = self._normalize_key(key)
        bucket_index = self.hash_function(normalized_key)
        current = self._buckets[bucket_index]
        comparisons = 0
        position = 0

        while current is not None:
            comparisons += 1
            if current.key == normalized_key:
                result = HashSearchResult(
                    found=True,
                    key=normalized_key,
                    bucket_index=bucket_index,
                    value=current.value,
                    comparisons=comparisons,
                    chain_position=position,
                )
                self._last_operation = self._operation_payload(
                    operation="SEARCH",
                    key=normalized_key,
                    bucket_index=bucket_index,
                    collision=position > 0,
                    chain_position=position,
                    found=True,
                )
                return result
            current = current.next
            position += 1

        result = HashSearchResult(
            found=False,
            key=normalized_key,
            bucket_index=bucket_index,
            comparisons=comparisons,
            chain_position=None,
        )
        self._last_operation = self._operation_payload(
            operation="SEARCH",
            key=normalized_key,
            bucket_index=bucket_index,
            collision=False,
            chain_position=None,
            found=False,
        )
        return result

    def contains(self, key: Any) -> bool:
        """Return True when a key exists."""
        return self.search(key).found

    def delete(self, key: Any) -> bool:
        """Delete a key from its collision chain if it exists."""
        normalized_key = self._normalize_key(key)
        bucket_index = self.hash_function(normalized_key)
        current = self._buckets[bucket_index]
        previous: Optional[HashEntry] = None
        position = 0

        while current is not None:
            if current.key == normalized_key:
                if previous is None:
                    self._buckets[bucket_index] = current.next
                else:
                    previous.next = current.next
                self._size -= 1
                self._last_operation = self._operation_payload(
                    operation="DELETE",
                    key=normalized_key,
                    bucket_index=bucket_index,
                    collision=position > 0,
                    chain_position=position,
                    found=True,
                )
                return True
            previous = current
            current = current.next
            position += 1

        self._last_operation = self._operation_payload(
            operation="DELETE",
            key=normalized_key,
            bucket_index=bucket_index,
            collision=False,
            chain_position=None,
            found=False,
        )
        return False

    def clear(self) -> None:
        """Remove all entries and reset collision counters."""
        self._buckets = [None for _ in range(self._capacity)]
        self._size = 0
        self._collisions = 0
        self._last_operation = self._operation_payload(
            operation="CLEAR",
            key=None,
            bucket_index=None,
            collision=False,
            chain_position=None,
        )

    def bucket_entries(self, bucket_index: int) -> list[HashEntry]:
        """Return entries stored in one bucket preserving chain order."""
        if not isinstance(bucket_index, int):
            raise ValueError("BUCKET_INDEX_MUST_BE_INTEGER")
        if bucket_index < 0 or bucket_index >= self._capacity:
            raise ValueError("BUCKET_INDEX_OUT_OF_RANGE")

        entries: list[HashEntry] = []
        current = self._buckets[bucket_index]
        while current is not None:
            entries.append(current)
            current = current.next
        return entries

    def buckets_snapshot(self) -> list[dict[str, Any]]:
        """Return a serializable bucket snapshot for services/serializers."""
        snapshot: list[dict[str, Any]] = []
        for index in range(self._capacity):
            entries = self.bucket_entries(index)
            snapshot.append({
                "bucketIndex": index,
                "size": len(entries),
                "hasCollision": len(entries) > 1,
                "items": [
                    {
                        "key": entry.key,
                        "value": entry.value,
                        "chainPosition": position,
                        "collision": position > 0,
                    }
                    for position, entry in enumerate(entries)
                ],
            })
        return snapshot

    def max_chain_length(self) -> int:
        """Return the largest number of entries stored in one bucket."""
        if self._capacity == 0:
            return 0
        return max(len(self.bucket_entries(index)) for index in range(self._capacity))

    def collision_bucket_count(self) -> int:
        """Return how many buckets currently contain collision chains."""
        return sum(1 for index in range(self._capacity) if len(self.bucket_entries(index)) > 1)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full table state to plain Python structures."""
        return {
            "capacity": self._capacity,
            "size": self._size,
            "collisions": self._collisions,
            "loadFactor": self.load_factor(),
            "maxChainLength": self.max_chain_length(),
            "collisionBucketCount": self.collision_bucket_count(),
            "buckets": self.buckets_snapshot(),
            "lastOperation": self.last_operation,
        }

    @staticmethod
    def _validate_capacity(capacity: int) -> None:
        if not isinstance(capacity, int):
            raise ValueError("CAPACITY_MUST_BE_INTEGER")
        if capacity < 3:
            raise ValueError("CAPACITY_MUST_BE_AT_LEAST_3")

    @staticmethod
    def _normalize_key(key: Any) -> str:
        if key is None:
            raise ValueError("KEY_REQUIRED")
        normalized_key = str(key).strip()
        if not normalized_key:
            raise ValueError("KEY_REQUIRED")
        return normalized_key

    @staticmethod
    def _operation_payload(
        operation: str,
        key: Optional[str],
        bucket_index: Optional[int],
        collision: bool,
        chain_position: Optional[int],
        found: Optional[bool] = None,
    ) -> dict[str, Any]:
        payload = {
            "operation": operation,
            "key": key,
            "bucketIndex": bucket_index,
            "collision": collision,
            "chainPosition": chain_position,
        }
        if found is not None:
            payload["found"] = found
        return payload
