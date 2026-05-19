"""
B-Tree implementation for EduStruct.

This module contains a manual B-Tree built in pure Python for educational
visualization. It intentionally avoids Flask, serializers, services, routes,
and third-party data-structure libraries.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BTreeNode:
    """Node for a B-Tree that stores multiple ordered keys."""

    keys: list[Any] = field(default_factory=list)
    children: list["BTreeNode"] = field(default_factory=list)
    leaf: bool = True

    def is_full(self, order: int) -> bool:
        """Return True when the node has reached the maximum key capacity."""
        return len(self.keys) >= order - 1

    def to_dict(self) -> dict[str, Any]:
        """Serialize this node and descendants to plain dictionaries."""
        return {
            "keys": list(self.keys),
            "leaf": self.leaf,
            "children": [child.to_dict() for child in self.children],
        }


class BTree:
    """
    Manual B-Tree using max-children order semantics.

    ``order`` is the maximum number of children per node. Therefore each node
    can store at most ``order - 1`` keys. The default order is 4, which is easy
    to explain visually because each node can contain up to three keys before a
    split promotes the median key.
    """

    def __init__(self, order: int = 4) -> None:
        if not isinstance(order, int) or order < 3:
            raise ValueError("INVALID_ORDER")

        self.order = order
        self._root = BTreeNode()
        self._size = 0
        self._split_events: list[dict[str, Any]] = []

    @property
    def root(self) -> BTreeNode:
        """Return the current root node."""
        return self._root

    @property
    def split_events(self) -> list[dict[str, Any]]:
        """Return defensive copies of split events registered by the last operation."""
        return deepcopy(self._split_events)

    def clear_split_events(self) -> None:
        """Clear split events without modifying the tree."""
        self._split_events = []

    def is_empty(self) -> bool:
        """Return True when the tree contains no keys."""
        return self._size == 0

    def size(self) -> int:
        """Return the number of keys stored in the tree."""
        return self._size

    def insert(self, key: Any) -> Any:
        """Insert a unique comparable key and split full nodes on the descent."""
        normalized_key = self._normalize_key(key)
        self.clear_split_events()

        if self.contains(normalized_key):
            raise ValueError("DUPLICATE_KEY")

        if self._root.is_full(self.order):
            old_root = self._root
            new_root = BTreeNode(keys=[], children=[old_root], leaf=False)
            self._root = new_root
            self._split_child(new_root, 0)

        self._insert_non_full(self._root, normalized_key)
        self._size += 1
        return normalized_key

    def search(self, key: Any) -> Optional[dict[str, Any]]:
        """Return match metadata for a key, or None when it does not exist."""
        normalized_key = self._normalize_key(key)
        return self._search_node(self._root, normalized_key, level=0, path=[])

    def contains(self, key: Any) -> bool:
        """Return True when the key exists in the tree."""
        return self.search(key) is not None

    def levelorder(self) -> list[dict[str, Any]]:
        """Return node metadata in breadth-first order for visualization."""
        if self.is_empty():
            return []

        result: list[dict[str, Any]] = []
        queue: list[tuple[BTreeNode, int, Optional[str], Optional[int]]] = [(self._root, 0, None, None)]
        index = 0

        while index < len(queue):
            node, level, parent_id, child_index = queue[index]
            index += 1
            node_id = self._node_id(node, level, parent_id, child_index)
            result.append(
                {
                    "id": node_id,
                    "keys": list(node.keys),
                    "label": self._label_for_keys(node.keys),
                    "leaf": node.leaf,
                    "level": level,
                    "parentId": parent_id,
                    "childIndex": child_index,
                    "keyCount": len(node.keys),
                    "childrenCount": len(node.children),
                    "isRoot": parent_id is None,
                }
            )

            for position, child in enumerate(node.children):
                queue.append((child, level + 1, node_id, position))

        return result

    def height(self) -> int:
        """Return the maximum zero-based level. Empty tree height is 0."""
        if self.is_empty():
            return 0

        height = 0
        current = self._root
        while not current.leaf and current.children:
            height += 1
            current = current.children[0]
        return height

    def levels_count(self) -> int:
        """Return total visual levels in the B-Tree."""
        if self.is_empty():
            return 0
        return self.height() + 1

    def node_count(self) -> int:
        """Return the total number of B-Tree nodes."""
        return len(self.levelorder())

    def leaf_count(self) -> int:
        """Return the number of leaf nodes."""
        return sum(1 for item in self.levelorder() if item["leaf"])

    def edges_count(self) -> int:
        """Return parent-child edge count."""
        if self.is_empty():
            return 0
        return max(0, self.node_count() - 1)

    def clear(self) -> None:
        """Remove every key and reset split metadata."""
        self._root = BTreeNode()
        self._size = 0
        self.clear_split_events()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the complete tree state."""
        return {
            "order": self.order,
            "size": self._size,
            "root": None if self.is_empty() else self._root.to_dict(),
        }

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        index = len(node.keys) - 1

        if node.leaf:
            node.keys.append(key)
            while index >= 0 and self._compare(key, node.keys[index]) < 0:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = key
            return

        while index >= 0 and self._compare(key, node.keys[index]) < 0:
            index -= 1
        child_index = index + 1

        if node.children[child_index].is_full(self.order):
            promoted_key = self._split_child(node, child_index)
            if self._compare(key, promoted_key) > 0:
                child_index += 1

        self._insert_non_full(node.children[child_index], key)

    def _split_child(self, parent: BTreeNode, child_index: int) -> Any:
        child = parent.children[child_index]
        before = child.to_dict()
        median_index = len(child.keys) // 2
        promoted_key = child.keys[median_index]

        left_keys = child.keys[:median_index]
        right_keys = child.keys[median_index + 1:]

        right_node = BTreeNode(keys=right_keys, leaf=child.leaf)
        if not child.leaf:
            right_node.children = child.children[median_index + 1:]
            child.children = child.children[: median_index + 1]

        child.keys = left_keys
        parent.keys.insert(child_index, promoted_key)
        parent.children.insert(child_index + 1, right_node)
        parent.leaf = False

        after = {
            "parent": parent.to_dict(),
            "left": child.to_dict(),
            "right": right_node.to_dict(),
        }
        self._split_events.append(
            {
                "type": "split",
                "promotedKey": promoted_key,
                "parentKeys": list(parent.keys),
                "childIndex": child_index,
                "before": before,
                "after": after,
            }
        )
        return promoted_key

    def _search_node(
        self,
        node: BTreeNode,
        key: Any,
        level: int,
        path: list[dict[str, Any]],
    ) -> Optional[dict[str, Any]]:
        index = 0
        while index < len(node.keys) and self._compare(key, node.keys[index]) > 0:
            index += 1

        current_path = [
            *path,
            {
                "level": level,
                "keys": list(node.keys),
                "childIndex": None,
            },
        ]

        if index < len(node.keys) and self._compare(key, node.keys[index]) == 0:
            return {
                "key": node.keys[index],
                "level": level,
                "keyIndex": index,
                "nodeKeys": list(node.keys),
                "path": current_path,
            }

        if node.leaf:
            return None

        current_path[-1]["childIndex"] = index
        return self._search_node(node.children[index], key, level + 1, current_path)

    def _node_id(
        self,
        node: BTreeNode,
        level: int,
        parent_id: Optional[str],
        child_index: Optional[int],
    ) -> str:
        keys_label = "-".join(str(key) for key in node.keys) if node.keys else "empty"
        if parent_id is None:
            return f"btree-root-{keys_label}"
        return f"btree-{level}-{parent_id}-{child_index}-{keys_label}"

    @staticmethod
    def _label_for_keys(keys: list[Any]) -> str:
        return " | ".join(str(key) for key in keys)

    @staticmethod
    def _normalize_key(key: Any) -> Any:
        if isinstance(key, str):
            normalized = key.strip()
            if normalized == "":
                raise ValueError("KEY_REQUIRED")
            return normalized

        if key is None:
            raise ValueError("KEY_REQUIRED")

        return key

    @staticmethod
    def _compare(left: Any, right: Any) -> int:
        try:
            if left < right:
                return -1
            if left > right:
                return 1
            return 0
        except TypeError as error:
            raise ValueError("INCOMPARABLE_KEY") from error
