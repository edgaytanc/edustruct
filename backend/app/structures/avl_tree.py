"""
AVL tree implementation for EduStruct.

This module contains a pure Python AVL tree built manually for educational
visualization. It does not depend on Flask, serializers, routes, services, or
third-party tree libraries.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Optional

try:
    from .queue import Queue
except ImportError:  # Allows direct execution in isolated unit tests.
    from queue import Queue


@dataclass
class AVLNode:
    """Node for an AVL self-balancing binary search tree."""

    value: Any
    left: Optional["AVLNode"] = None
    right: Optional["AVLNode"] = None
    height: int = 1

    def balance_factor(self) -> int:
        """Return left subtree height minus right subtree height."""
        return AVLTree.node_height(self.left) - AVLTree.node_height(self.right)

    def to_dict(self) -> dict[str, Any]:
        """Serialize this node and descendants to a plain dictionary."""
        balance_factor = self.balance_factor()
        return {
            "value": self.value,
            "height": self.height,
            "balanceFactor": balance_factor,
            "isUnbalanced": abs(balance_factor) > 1,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }


class AVLTree:
    """
    Manual AVL tree.

    Responsibilities:
    - Store unique comparable values using custom AVL nodes.
    - Insert and delete while preserving BST ordering.
    - Rebalance through LL, RR, LR and RL rotations.
    - Keep node heights updated after every structural change.
    - Register rotation events with before/after snapshots for visualization.
    """

    def __init__(self) -> None:
        self._root: Optional[AVLNode] = None
        self._size: int = 0
        self._rotation_events: list[dict[str, Any]] = []

    @property
    def root(self) -> Optional[AVLNode]:
        """Return the root node."""
        return self._root

    @property
    def rotation_events(self) -> list[dict[str, Any]]:
        """Return a defensive copy of registered rotation events."""
        return deepcopy(self._rotation_events)

    def clear_rotation_events(self) -> None:
        """Remove stored rotation events without changing the tree."""
        self._rotation_events = []

    def is_empty(self) -> bool:
        """Return True when the tree has no nodes."""
        return self._root is None

    def size(self) -> int:
        """Return the number of nodes stored in the tree."""
        return self._size

    def insert(self, value: Any) -> AVLNode:
        """Insert a unique value and rebalance the tree if needed."""
        normalized_value = self._normalize_value(value)
        self.clear_rotation_events()
        inserted_node: Optional[AVLNode] = None

        def insert_node(node: Optional[AVLNode], target: Any) -> AVLNode:
            nonlocal inserted_node

            if node is None:
                inserted_node = AVLNode(value=target)
                self._size += 1
                return inserted_node

            comparison = self._compare(target, node.value)

            if comparison == 0:
                raise ValueError("DUPLICATE_VALUE")

            if comparison < 0:
                node.left = insert_node(node.left, target)
            else:
                node.right = insert_node(node.right, target)

            return self._rebalance(node)

        self._root = insert_node(self._root, normalized_value)
        return inserted_node if inserted_node is not None else self._root

    def delete(self, value: Any) -> Optional[AVLNode]:
        """
        Delete a value and rebalance the tree if the value exists.

        Returns a snapshot of the deleted node when found, otherwise None.
        """
        normalized_value = self._normalize_value(value)
        self.clear_rotation_events()
        removed_snapshot: Optional[AVLNode] = None

        def delete_node(node: Optional[AVLNode], target: Any) -> Optional[AVLNode]:
            nonlocal removed_snapshot

            if node is None:
                return None

            comparison = self._compare(target, node.value)

            if comparison < 0:
                node.left = delete_node(node.left, target)
            elif comparison > 0:
                node.right = delete_node(node.right, target)
            else:
                removed_snapshot = AVLNode(
                    value=node.value,
                    left=node.left,
                    right=node.right,
                    height=node.height,
                )

                if node.left is None:
                    self._size -= 1
                    return node.right

                if node.right is None:
                    self._size -= 1
                    return node.left

                successor = self._min_node(node.right)
                node.value = successor.value
                node.right = self._delete_successor(node.right)
                self._size -= 1

            if node is None:
                return None

            return self._rebalance(node)

        self._root = delete_node(self._root, normalized_value)
        return removed_snapshot

    def search(self, value: Any) -> Optional[AVLNode]:
        """Return the node matching value or None when it does not exist."""
        normalized_value = self._normalize_value(value)
        current = self._root

        while current is not None:
            comparison = self._compare(normalized_value, current.value)

            if comparison == 0:
                return current

            current = current.left if comparison < 0 else current.right

        return None

    def contains(self, value: Any) -> bool:
        """Return True when value exists in the tree."""
        return self.search(value) is not None

    def get_level(self, value: Any) -> Optional[int]:
        """Return the zero-based level of a value, or None when not found."""
        normalized_value = self._normalize_value(value)
        current = self._root
        level = 0

        while current is not None:
            comparison = self._compare(normalized_value, current.value)

            if comparison == 0:
                return level

            current = current.left if comparison < 0 else current.right
            level += 1

        return None

    def height(self) -> int:
        """
        Return the tree height as maximum zero-based level.

        Empty tree height is 0 to preserve the current EduStruct metrics style.
        Node heights stored internally are one-based, as is standard for AVL.
        """
        if self._root is None:
            return 0
        return self._root.height - 1

    def levels_count(self) -> int:
        """Return the total number of visual levels in the tree."""
        if self._root is None:
            return 0
        return self._root.height

    def leaf_count(self) -> int:
        """Return the number of nodes without children."""
        leaves = 0
        for node in self.preorder_nodes():
            if node.left is None and node.right is None:
                leaves += 1
        return leaves

    def edges_count(self) -> int:
        """Return the number of parent-child edges in the tree."""
        if self._size == 0:
            return 0
        return self._size - 1

    def balance_factor(self) -> int:
        """Return root balance factor as left subtree height minus right subtree height."""
        if self._root is None:
            return 0
        return self._root.balance_factor()

    def is_balanced(self) -> bool:
        """Return True when every node has balance factor between -1 and 1."""
        return all(abs(node.balance_factor()) <= 1 for node in self.preorder_nodes())

    def preorder_nodes(self) -> list[AVLNode]:
        """Return nodes in preorder: root, left, right."""
        result: list[AVLNode] = []

        def visit(node: Optional[AVLNode]) -> None:
            if node is None:
                return
            result.append(node)
            visit(node.left)
            visit(node.right)

        visit(self._root)
        return result

    def inorder_nodes(self) -> list[AVLNode]:
        """Return nodes in inorder: left, root, right."""
        result: list[AVLNode] = []

        def visit(node: Optional[AVLNode]) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node)
            visit(node.right)

        visit(self._root)
        return result

    def postorder_nodes(self) -> list[AVLNode]:
        """Return nodes in postorder: left, right, root."""
        result: list[AVLNode] = []

        def visit(node: Optional[AVLNode]) -> None:
            if node is None:
                return
            visit(node.left)
            visit(node.right)
            result.append(node)

        visit(self._root)
        return result

    def levelorder_nodes_with_levels(self) -> list[dict[str, Any]]:
        """Return nodes by level using the project's manual Queue."""
        result: list[dict[str, Any]] = []

        if self._root is None:
            return result

        queue = Queue()
        queue.enqueue({"node": self._root, "level": 0, "parentValue": None, "direction": None})

        while not queue.is_empty():
            current = queue.dequeue()
            node = current["node"]
            level = current["level"]
            result.append(current)

            if node.left is not None:
                queue.enqueue({
                    "node": node.left,
                    "level": level + 1,
                    "parentValue": node.value,
                    "direction": "left",
                })

            if node.right is not None:
                queue.enqueue({
                    "node": node.right,
                    "level": level + 1,
                    "parentValue": node.value,
                    "direction": "right",
                })

        return result

    def preorder(self) -> list[dict[str, Any]]:
        """Return preorder traversal as serializable dictionaries."""
        return [self._node_to_plain(node) for node in self.preorder_nodes()]

    def inorder(self) -> list[dict[str, Any]]:
        """Return inorder traversal as serializable dictionaries."""
        return [self._node_to_plain(node) for node in self.inorder_nodes()]

    def postorder(self) -> list[dict[str, Any]]:
        """Return postorder traversal as serializable dictionaries."""
        return [self._node_to_plain(node) for node in self.postorder_nodes()]

    def levelorder(self) -> list[dict[str, Any]]:
        """Return levelorder traversal as serializable dictionaries."""
        return [
            self._node_to_plain(
                item["node"],
                level=item["level"],
                parent_value=item["parentValue"],
                direction=item["direction"],
            )
            for item in self.levelorder_nodes_with_levels()
        ]

    def to_dict(self) -> dict[str, Any]:
        """Return the full tree as a serializable dictionary."""
        return {
            "root": self._root.to_dict() if self._root else None,
            "size": self._size,
            "height": self.height(),
            "levels": self.levels_count(),
            "balanceFactor": self.balance_factor(),
            "isBalanced": self.is_balanced(),
            "rotationEvents": self.rotation_events,
            "type": "avl-tree",
        }

    def clear(self) -> None:
        """Remove all nodes and rotation events from the tree."""
        self._root = None
        self._size = 0
        self.clear_rotation_events()

    def _delete_successor(self, node: AVLNode) -> Optional[AVLNode]:
        """Remove the minimum node from a subtree without changing total size."""
        if node.left is None:
            return node.right

        node.left = self._delete_successor(node.left)
        return self._rebalance(node)

    def _min_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self._update_height(node)
        balance = node.balance_factor()

        if balance > 1:
            if node.left is not None and node.left.balance_factor() >= 0:
                return self._rotate_right(node, "LL")

            if node.left is not None:
                before = self._snapshot(node)
                pivot = node.value
                node.left = self._rotate_left(node.left, None)
                rotated = self._rotate_right(node, None)
                self._record_rotation("LR", pivot, before, self._snapshot(rotated))
                return rotated

        if balance < -1:
            if node.right is not None and node.right.balance_factor() <= 0:
                return self._rotate_left(node, "RR")

            if node.right is not None:
                before = self._snapshot(node)
                pivot = node.value
                node.right = self._rotate_right(node.right, None)
                rotated = self._rotate_left(node, None)
                self._record_rotation("RL", pivot, before, self._snapshot(rotated))
                return rotated

        return node

    def _rotate_left(self, node: AVLNode, rotation_type: Optional[str]) -> AVLNode:
        before = self._snapshot(node) if rotation_type else None
        pivot = node.value
        new_root = node.right

        if new_root is None:
            return node

        transferred_subtree = new_root.left
        new_root.left = node
        node.right = transferred_subtree

        self._update_height(node)
        self._update_height(new_root)

        if rotation_type is not None:
            self._record_rotation(rotation_type, pivot, before, self._snapshot(new_root))

        return new_root

    def _rotate_right(self, node: AVLNode, rotation_type: Optional[str]) -> AVLNode:
        before = self._snapshot(node) if rotation_type else None
        pivot = node.value
        new_root = node.left

        if new_root is None:
            return node

        transferred_subtree = new_root.right
        new_root.right = node
        node.left = transferred_subtree

        self._update_height(node)
        self._update_height(new_root)

        if rotation_type is not None:
            self._record_rotation(rotation_type, pivot, before, self._snapshot(new_root))

        return new_root

    def _record_rotation(
        self,
        rotation_type: str,
        pivot: Any,
        before: Optional[dict[str, Any]],
        after: Optional[dict[str, Any]],
    ) -> None:
        self._rotation_events.append({
            "type": rotation_type,
            "pivot": pivot,
            "before": before,
            "after": after,
        })

    @classmethod
    def node_height(cls, node: Optional[AVLNode]) -> int:
        """Return AVL internal one-based height for a node."""
        return node.height if node is not None else 0

    @classmethod
    def _update_height(cls, node: AVLNode) -> None:
        node.height = 1 + max(cls.node_height(node.left), cls.node_height(node.right))

    @staticmethod
    def _snapshot(node: Optional[AVLNode]) -> Optional[dict[str, Any]]:
        return node.to_dict() if node is not None else None

    @staticmethod
    def _node_to_plain(
        node: AVLNode,
        level: Optional[int] = None,
        parent_value: Optional[Any] = None,
        direction: Optional[str] = None,
    ) -> dict[str, Any]:
        balance_factor = node.balance_factor()
        data = {
            "id": str(node.value),
            "value": node.value,
            "label": str(node.value),
            "height": node.height,
            "visualHeight": node.height - 1,
            "balanceFactor": balance_factor,
            "isUnbalanced": abs(balance_factor) > 1,
            "hasLeft": node.left is not None,
            "hasRight": node.right is not None,
            "childrenCount": int(node.left is not None) + int(node.right is not None),
        }

        if level is not None:
            data["level"] = level

        if parent_value is not None:
            data["parentId"] = str(parent_value)
            data["parentValue"] = parent_value

        if direction is not None:
            data["direction"] = direction

        return data

    @staticmethod
    def _normalize_value(value: Any) -> Any:
        if value is None:
            raise ValueError("VALUE_REQUIRED")

        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                raise ValueError("VALUE_REQUIRED")
            return normalized

        return value

    @staticmethod
    def _compare(left: Any, right: Any) -> int:
        try:
            if left < right:
                return -1
            if left > right:
                return 1
            return 0
        except TypeError as error:
            raise ValueError("INCOMPARABLE_VALUE") from error
