"""
Binary search tree implementation for EduStruct.

This module represents a binary tree specialized as a Binary Search Tree (BST).
It belongs to the pure data-structures layer: it must not import Flask,
serializers, routes, services, or HTTP concerns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

try:
    from .queue import Queue
except ImportError:  # Allows direct execution in isolated unit tests.
    from queue import Queue


@dataclass
class BinaryTreeNode:
    """Node for a binary search tree."""

    value: Any
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the node and its descendants to a plain dictionary."""
        return {
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }


class BinaryTree:
    """
    Manual binary search tree.

    Responsibilities:
    - Store comparable values using custom binary nodes.
    - Insert values preserving BST ordering.
    - Delete values while preserving BST ordering.
    - Search values and calculate levels/depth.
    - Provide preorder, inorder, postorder and levelorder traversals.
    """

    def __init__(self) -> None:
        self._root: Optional[BinaryTreeNode] = None
        self._size: int = 0

    @property
    def root(self) -> Optional[BinaryTreeNode]:
        """Return the root node."""
        return self._root

    def is_empty(self) -> bool:
        """Return True when the tree has no nodes."""
        return self._root is None

    def size(self) -> int:
        """Return the number of nodes stored in the tree."""
        return self._size

    def insert(self, value: Any) -> BinaryTreeNode:
        """
        Insert a value into the BST.

        Duplicate values are rejected because this tree is used as a visual
        educational BST where each node must be uniquely identifiable.
        """
        normalized_value = self._normalize_value(value)
        new_node = BinaryTreeNode(value=normalized_value)

        if self._root is None:
            self._root = new_node
            self._size = 1
            return new_node

        current = self._root
        while current is not None:
            comparison = self._compare(normalized_value, current.value)

            if comparison == 0:
                raise ValueError("DUPLICATE_VALUE")

            if comparison < 0:
                if current.left is None:
                    current.left = new_node
                    self._size += 1
                    return new_node
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    self._size += 1
                    return new_node
                current = current.right

        return new_node

    def delete(self, value: Any) -> Optional[BinaryTreeNode]:
        """
        Delete a value from the BST.

        Returns the deleted node snapshot when found, otherwise None.
        The internal tree is reorganized using the inorder successor when the
        deleted node has two children.
        """
        normalized_value = self._normalize_value(value)

        removed_snapshot: Optional[BinaryTreeNode] = None

        def remove_node(node: Optional[BinaryTreeNode], target: Any) -> Optional[BinaryTreeNode]:
            nonlocal removed_snapshot

            if node is None:
                return None

            comparison = self._compare(target, node.value)

            if comparison < 0:
                node.left = remove_node(node.left, target)
                return node

            if comparison > 0:
                node.right = remove_node(node.right, target)
                return node

            removed_snapshot = BinaryTreeNode(value=node.value, left=node.left, right=node.right)

            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            successor = self._min_node(node.right)
            node.value = successor.value
            node.right = self._delete_min(node.right)
            return node

        self._root = remove_node(self._root, normalized_value)

        if removed_snapshot is not None:
            self._size -= 1

        return removed_snapshot

    def search(self, value: Any) -> Optional[BinaryTreeNode]:
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

        Empty tree height is 0 to preserve the existing metrics contract that
        uses numeric values for visual structures.
        """
        if self._root is None:
            return 0

        def calculate(node: Optional[BinaryTreeNode]) -> int:
            if node is None:
                return -1
            return 1 + max(calculate(node.left), calculate(node.right))

        return calculate(self._root)

    def levels_count(self) -> int:
        """Return the total number of visual levels in the tree."""
        if self._root is None:
            return 0
        return self.height() + 1

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
        return self._subtree_height(self._root.left) - self._subtree_height(self._root.right)

    def preorder_nodes(self) -> list[BinaryTreeNode]:
        """Return nodes in preorder: root, left, right."""
        result: list[BinaryTreeNode] = []

        def visit(node: Optional[BinaryTreeNode]) -> None:
            if node is None:
                return
            result.append(node)
            visit(node.left)
            visit(node.right)

        visit(self._root)
        return result

    def inorder_nodes(self) -> list[BinaryTreeNode]:
        """Return nodes in inorder: left, root, right."""
        result: list[BinaryTreeNode] = []

        def visit(node: Optional[BinaryTreeNode]) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node)
            visit(node.right)

        visit(self._root)
        return result

    def postorder_nodes(self) -> list[BinaryTreeNode]:
        """Return nodes in postorder: left, right, root."""
        result: list[BinaryTreeNode] = []

        def visit(node: Optional[BinaryTreeNode]) -> None:
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
            "type": "binary-search-tree",
        }

    def clear(self) -> None:
        """Remove all nodes from the tree."""
        self._root = None
        self._size = 0

    def _min_node(self, node: BinaryTreeNode) -> BinaryTreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_min(self, node: BinaryTreeNode) -> Optional[BinaryTreeNode]:
        if node.left is None:
            return node.right
        node.left = self._delete_min(node.left)
        return node

    def _subtree_height(self, node: Optional[BinaryTreeNode]) -> int:
        if node is None:
            return -1
        return 1 + max(self._subtree_height(node.left), self._subtree_height(node.right))

    @staticmethod
    def _node_to_plain(
        node: BinaryTreeNode,
        level: Optional[int] = None,
        parent_value: Optional[Any] = None,
        direction: Optional[str] = None,
    ) -> dict[str, Any]:
        data = {
            "id": str(node.value),
            "value": node.value,
            "label": str(node.value),
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
