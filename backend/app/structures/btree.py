"""
B-Tree implementation for EduStruct.

This module contains a pure Python B-Tree designed for educational
visualization of academic record indexes. It has no dependency on Flask,
serializers, routes, services, or external tree libraries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

try:
    from .queue import Queue
except ImportError:  # Allows direct execution in isolated unit tests.
    from queue import Queue


@dataclass
class BTreeNode:
    """Node for a manual B-Tree."""

    keys: list[Any] = field(default_factory=list)
    children: list["BTreeNode"] = field(default_factory=list)
    leaf: bool = True

    def is_leaf(self) -> bool:
        """Return True when this node has no children."""
        return self.leaf

    def to_dict(self) -> dict[str, Any]:
        """Serialize this node and descendants to plain dictionaries."""
        return {
            "keys": list(self.keys),
            "leaf": self.leaf,
            "children": [child.to_dict() for child in self.children],
        }


@dataclass
class BTreeSearchResult:
    """Search result metadata for a key stored in the B-Tree."""

    found: bool
    key: Any
    node: Optional[BTreeNode] = None
    index: Optional[int] = None
    level: Optional[int] = None
    path: list[list[Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the search result without exposing object references."""
        return {
            "found": self.found,
            "key": self.key,
            "index": self.index,
            "level": self.level,
            "nodeKeys": list(self.node.keys) if self.node else None,
            "path": [list(keys) for keys in self.path],
        }


class BTree:
    """
    Manual B-Tree using configurable order.

    The order represents the maximum number of children per node. Therefore,
    every node can store at most ``order - 1`` keys. Insertions split nodes when
    they overflow to ``order`` keys, promoting the median key to the parent.
    """

    def __init__(self, order: int = 4) -> None:
        self._validate_order(order)
        self._order = order
        self._root: Optional[BTreeNode] = None
        self._size = 0
        self._split_events: list[dict[str, Any]] = []

    @property
    def root(self) -> Optional[BTreeNode]:
        """Return the root node."""
        return self._root

    @property
    def order(self) -> int:
        """Return the configured B-Tree order."""
        return self._order

    @property
    def max_keys(self) -> int:
        """Return the maximum number of keys allowed per node."""
        return self._order - 1

    @property
    def min_keys(self) -> int:
        """Return the non-root minimum key count used by B-Tree invariants."""
        return (self._order + 1) // 2 - 1

    @property
    def split_events(self) -> list[dict[str, Any]]:
        """Return split events registered during insertions."""
        return list(self._split_events)

    def is_empty(self) -> bool:
        """Return True when the tree has no keys."""
        return self._root is None

    def size(self) -> int:
        """Return the number of keys stored in the tree."""
        return self._size

    def insert(self, key: Any) -> Any:
        """
        Insert a key into the B-Tree.

        Duplicate keys are rejected because keys are used as stable visual
        identifiers for academic records in the frontend.
        """
        normalized_key = self._normalize_key(key)

        if self.contains(normalized_key):
            raise ValueError("DUPLICATE_KEY")

        if self._root is None:
            self._root = BTreeNode(keys=[normalized_key], leaf=True)
            self._size = 1
            return normalized_key

        split_result = self._insert_recursive(self._root, normalized_key, level=0)
        if split_result is not None:
            promoted_key, left_node, right_node, event = split_result
            self._root = BTreeNode(
                keys=[promoted_key],
                children=[left_node, right_node],
                leaf=False,
            )
            event["parentKeysAfter"] = [promoted_key]
            event["createdNewRoot"] = True
            self._split_events.append(event)

        self._size += 1
        return normalized_key

    def search(self, key: Any) -> BTreeSearchResult:
        """Search a key and return detailed traversal metadata."""
        normalized_key = self._normalize_key(key)
        current = self._root
        level = 0
        path: list[list[Any]] = []

        while current is not None:
            path.append(list(current.keys))
            index = self._find_insert_position(current.keys, normalized_key)

            if index < len(current.keys) and self._compare(normalized_key, current.keys[index]) == 0:
                return BTreeSearchResult(
                    found=True,
                    key=normalized_key,
                    node=current,
                    index=index,
                    level=level,
                    path=path,
                )

            if current.leaf:
                return BTreeSearchResult(found=False, key=normalized_key, level=None, path=path)

            current = current.children[index]
            level += 1

        return BTreeSearchResult(found=False, key=normalized_key, level=None, path=path)

    def contains(self, key: Any) -> bool:
        """Return True when the key exists in the tree."""
        return self.search(key).found

    def height(self) -> int:
        """
        Return visual height as maximum zero-based level.

        Empty tree height remains 0 for compatibility with existing metrics.
        """
        if self._root is None:
            return 0

        height = 0
        current = self._root
        while not current.leaf:
            height += 1
            current = current.children[0]
        return height

    def levels_count(self) -> int:
        """Return the number of visual levels."""
        if self._root is None:
            return 0
        return self.height() + 1

    def node_count(self) -> int:
        """Return the number of B-Tree nodes, not the number of keys."""
        return len(self.levelorder_nodes())

    def leaf_count(self) -> int:
        """Return the number of leaf nodes."""
        return sum(1 for node in self.levelorder_nodes() if node.leaf)

    def edges_count(self) -> int:
        """Return the number of parent-child edges."""
        nodes = self.node_count()
        return 0 if nodes == 0 else nodes - 1

    def levelorder_nodes(self) -> list[BTreeNode]:
        """Return B-Tree nodes in level-order."""
        return [item["node"] for item in self._levelorder_entries()]

    def levelorder(self) -> list[dict[str, Any]]:
        """Return level-order traversal with metadata for visualization."""
        result: list[dict[str, Any]] = []
        for entry in self._levelorder_entries():
            node = entry["node"]
            result.append({
                "id": self._node_id(node),
                "keys": list(node.keys),
                "leaf": node.leaf,
                "level": entry["level"],
                "parentId": entry["parentId"],
                "parentKeys": entry["parentKeys"],
                "childIndex": entry["childIndex"],
                "keyCount": len(node.keys),
            })
        return result

    def inorder(self) -> list[Any]:
        """Return all keys in sorted order."""
        result: list[Any] = []

        def visit(node: Optional[BTreeNode]) -> None:
            if node is None:
                return
            if node.leaf:
                result.extend(node.keys)
                return
            for index, key in enumerate(node.keys):
                visit(node.children[index])
                result.append(key)
            visit(node.children[len(node.keys)])

        visit(self._root)
        return result

    def clear(self) -> None:
        """Remove all keys and split history."""
        self._root = None
        self._size = 0
        self._split_events.clear()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full B-Tree state."""
        return {
            "order": self._order,
            "maxKeys": self.max_keys,
            "minKeys": self.min_keys,
            "size": self._size,
            "height": self.height(),
            "levels": self.levels_count(),
            "root": self._root.to_dict() if self._root else None,
            "levelorder": self.levelorder(),
            "splitEvents": self.split_events,
        }

    def validate_invariants(self) -> bool:
        """Return True when core B-Tree invariants are satisfied."""
        if self._root is None:
            return self._size == 0

        leaf_levels: set[int] = set()

        def validate(node: BTreeNode, level: int, is_root: bool) -> bool:
            if len(node.keys) > self.max_keys:
                return False
            if not is_root and len(node.keys) < self.min_keys:
                return False
            if any(self._compare(node.keys[i], node.keys[i + 1]) >= 0 for i in range(len(node.keys) - 1)):
                return False
            if node.leaf:
                if node.children:
                    return False
                leaf_levels.add(level)
                return True
            if len(node.children) != len(node.keys) + 1:
                return False
            return all(validate(child, level + 1, False) for child in node.children)

        return validate(self._root, 0, True) and len(leaf_levels) == 1 and len(self.inorder()) == self._size

    def _insert_recursive(
        self,
        node: BTreeNode,
        key: Any,
        level: int,
    ) -> Optional[tuple[Any, BTreeNode, BTreeNode, dict[str, Any]]]:
        if node.leaf:
            position = self._find_insert_position(node.keys, key)
            node.keys.insert(position, key)
        else:
            child_index = self._find_insert_position(node.keys, key)
            split_result = self._insert_recursive(node.children[child_index], key, level + 1)
            if split_result is not None:
                promoted_key, left_child, right_child, event = split_result
                node.keys.insert(child_index, promoted_key)
                node.children[child_index] = left_child
                node.children.insert(child_index + 1, right_child)
                event["parentKeysAfter"] = list(node.keys)
                self._split_events.append(event)

        if len(node.keys) <= self.max_keys:
            return None

        return self._split_node(node, level)

    def _split_node(self, node: BTreeNode, level: int) -> tuple[Any, BTreeNode, BTreeNode, dict[str, Any]]:
        before_keys = list(node.keys)
        median_index = len(node.keys) // 2
        promoted_key = node.keys[median_index]

        left_node = BTreeNode(
            keys=node.keys[:median_index],
            children=node.children[: median_index + 1] if not node.leaf else [],
            leaf=node.leaf,
        )
        right_node = BTreeNode(
            keys=node.keys[median_index + 1 :],
            children=node.children[median_index + 1 :] if not node.leaf else [],
            leaf=node.leaf,
        )

        event = {
            "type": "SPLIT",
            "level": level,
            "promotedKey": promoted_key,
            "beforeKeys": before_keys,
            "leftKeys": list(left_node.keys),
            "rightKeys": list(right_node.keys),
            "leaf": node.leaf,
            "createdNewRoot": False,
        }
        return promoted_key, left_node, right_node, event

    def _levelorder_entries(self) -> list[dict[str, Any]]:
        if self._root is None:
            return []

        result: list[dict[str, Any]] = []
        queue = Queue()
        queue.enqueue({
            "node": self._root,
            "level": 0,
            "parentId": None,
            "parentKeys": None,
            "childIndex": None,
        })

        while not queue.is_empty():
            entry = queue.dequeue()
            node = entry["node"]
            result.append(entry)

            for child_index, child in enumerate(node.children):
                queue.enqueue({
                    "node": child,
                    "level": entry["level"] + 1,
                    "parentId": self._node_id(node),
                    "parentKeys": list(node.keys),
                    "childIndex": child_index,
                })

        return result

    def _node_id(self, node: BTreeNode) -> str:
        return "btree-" + "-".join(str(key) for key in node.keys)

    def _find_insert_position(self, keys: list[Any], key: Any) -> int:
        position = 0
        while position < len(keys) and self._compare(key, keys[position]) > 0:
            position += 1
        return position

    @staticmethod
    def _validate_order(order: int) -> None:
        if not isinstance(order, int):
            raise ValueError("ORDER_MUST_BE_INTEGER")
        if order < 3:
            raise ValueError("ORDER_MUST_BE_AT_LEAST_3")

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
        except TypeError as exc:
            raise ValueError("INCOMPARABLE_KEY") from exc
