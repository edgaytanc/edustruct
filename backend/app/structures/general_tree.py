"""
General tree implementation for EduStruct.

This module represents an academic curriculum as a general tree where each
node can have multiple children. It belongs to the pure data-structures layer:
it must not import Flask, serializers, routes, services, or HTTP concerns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

try:
    from .queue import Queue
except ImportError:  # Allows direct execution in isolated unit tests.
    from queue import Queue


@dataclass
class GeneralTreeNode:
    """Node for a general tree with multiple children."""

    node_id: str
    label: str
    category: str = "academic"
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list["GeneralTreeNode"] = field(default_factory=list)

    def add_child(self, child: "GeneralTreeNode") -> None:
        """Attach a child node preserving insertion order."""
        self.children.append(child)

    def remove_child_by_id(self, node_id: str) -> Optional["GeneralTreeNode"]:
        """Remove and return a direct child by id."""
        for index, child in enumerate(self.children):
            if child.node_id == node_id:
                return self.children.pop(index)
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the node and its descendants to a plain dictionary."""
        return {
            "id": self.node_id,
            "label": self.label,
            "category": self.category,
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children],
        }


class GeneralTree:
    """
    Manual general tree.

    Responsibilities:
    - Store academic hierarchy nodes using custom node objects.
    - Insert nodes by parent id.
    - Delete a node and its full subtree.
    - Search nodes and calculate levels/depth.
    - Provide preorder, postorder and levelorder traversals.
    """

    def __init__(self) -> None:
        self._root: Optional[GeneralTreeNode] = None
        self._size: int = 0

    @property
    def root(self) -> Optional[GeneralTreeNode]:
        """Return the root node."""
        return self._root

    def is_empty(self) -> bool:
        """Return True when the tree has no nodes."""
        return self._root is None

    def size(self) -> int:
        """Return the number of nodes stored in the tree."""
        return self._size

    def insert(
        self,
        node_id: str,
        label: str,
        parent_id: Optional[str] = None,
        category: str = "academic",
        metadata: Optional[dict[str, Any]] = None,
    ) -> GeneralTreeNode:
        """
        Insert a node into the tree.

        If the tree is empty, parent_id must be None and the inserted node
        becomes the root. Otherwise, parent_id is required and must exist.
        """
        normalized_id = self._normalize_text(node_id)
        normalized_label = self._normalize_text(label)
        normalized_category = self._normalize_text(category or "academic")

        if self.search(normalized_id) is not None:
            raise ValueError("DUPLICATE_NODE_ID")

        new_node = GeneralTreeNode(
            node_id=normalized_id,
            label=normalized_label,
            category=normalized_category,
            metadata=metadata or {},
        )

        if self._root is None:
            if parent_id is not None:
                raise ValueError("PARENT_NOT_FOUND")
            self._root = new_node
            self._size = 1
            return new_node

        if parent_id is None:
            raise ValueError("PARENT_REQUIRED")

        parent = self.search(parent_id)
        if parent is None:
            raise ValueError("PARENT_NOT_FOUND")

        parent.add_child(new_node)
        self._size += 1
        return new_node

    def delete(self, node_id: str) -> Optional[GeneralTreeNode]:
        """
        Delete a node and its descendants.

        Returns the deleted subtree root when found, otherwise None.
        """
        normalized_id = self._normalize_text(node_id)

        if self._root is None:
            return None

        if self._root.node_id == normalized_id:
            removed_root = self._root
            self.clear()
            return removed_root

        parent = self._find_parent(normalized_id)
        if parent is None:
            return None

        removed = parent.remove_child_by_id(normalized_id)
        if removed is None:
            return None

        self._size -= self._count_subtree_nodes(removed)
        return removed

    def search(self, node_id: str) -> Optional[GeneralTreeNode]:
        """Return the node matching node_id or None when it does not exist."""
        normalized_id = self._normalize_text(node_id)

        if self._root is None:
            return None

        for node in self.preorder_nodes():
            if node.node_id == normalized_id:
                return node

        return None

    def contains(self, node_id: str) -> bool:
        """Return True when node_id exists in the tree."""
        return self.search(node_id) is not None

    def get_level(self, node_id: str) -> Optional[int]:
        """Return the zero-based level of a node, or None when not found."""
        normalized_id = self._normalize_text(node_id)

        for item in self.levelorder_nodes_with_levels():
            node = item["node"]
            if node.node_id == normalized_id:
                return item["level"]

        return None

    def height(self) -> int:
        """
        Return the tree height as maximum zero-based level.

        Empty tree height is 0 to preserve the existing metrics contract that
        uses numeric values for visual structures.
        """
        if self._root is None:
            return 0

        max_level = 0
        for item in self.levelorder_nodes_with_levels():
            if item["level"] > max_level:
                max_level = item["level"]
        return max_level

    def levels_count(self) -> int:
        """Return the total number of visual levels in the tree."""
        if self._root is None:
            return 0
        return self.height() + 1

    def leaf_count(self) -> int:
        """Return the number of nodes without children."""
        leaves = 0
        for node in self.preorder_nodes():
            if len(node.children) == 0:
                leaves += 1
        return leaves

    def max_children(self) -> int:
        """Return the maximum number of children owned by a single node."""
        maximum = 0
        for node in self.preorder_nodes():
            if len(node.children) > maximum:
                maximum = len(node.children)
        return maximum

    def preorder_nodes(self) -> list[GeneralTreeNode]:
        """Return nodes in preorder: parent before children."""
        result: list[GeneralTreeNode] = []

        def visit(node: GeneralTreeNode) -> None:
            result.append(node)
            for child in node.children:
                visit(child)

        if self._root is not None:
            visit(self._root)

        return result

    def postorder_nodes(self) -> list[GeneralTreeNode]:
        """Return nodes in postorder: children before parent."""
        result: list[GeneralTreeNode] = []

        def visit(node: GeneralTreeNode) -> None:
            for child in node.children:
                visit(child)
            result.append(node)

        if self._root is not None:
            visit(self._root)

        return result

    def levelorder_nodes_with_levels(self) -> list[dict[str, Any]]:
        """Return nodes by level using the project's manual Queue."""
        result: list[dict[str, Any]] = []

        if self._root is None:
            return result

        queue = Queue()
        queue.enqueue({"node": self._root, "level": 0, "parentId": None})

        while not queue.is_empty():
            current = queue.dequeue()
            node = current["node"]
            level = current["level"]
            parent_id = current["parentId"]

            result.append({"node": node, "level": level, "parentId": parent_id})

            for child in node.children:
                queue.enqueue({"node": child, "level": level + 1, "parentId": node.node_id})

        return result

    def preorder(self) -> list[dict[str, Any]]:
        """Return preorder traversal as serializable dictionaries."""
        return [self._node_to_plain(node) for node in self.preorder_nodes()]

    def postorder(self) -> list[dict[str, Any]]:
        """Return postorder traversal as serializable dictionaries."""
        return [self._node_to_plain(node) for node in self.postorder_nodes()]

    def levelorder(self) -> list[dict[str, Any]]:
        """Return levelorder traversal as serializable dictionaries."""
        return [
            self._node_to_plain(item["node"], level=item["level"], parent_id=item["parentId"])
            for item in self.levelorder_nodes_with_levels()
        ]

    def to_dict(self) -> dict[str, Any]:
        """Return the full tree as a serializable dictionary."""
        return {
            "root": self._root.to_dict() if self._root else None,
            "size": self._size,
            "height": self.height(),
            "levels": self.levels_count(),
        }

    def clear(self) -> None:
        """Remove all nodes from the tree."""
        self._root = None
        self._size = 0

    def _find_parent(self, node_id: str) -> Optional[GeneralTreeNode]:
        if self._root is None or self._root.node_id == node_id:
            return None

        for node in self.preorder_nodes():
            for child in node.children:
                if child.node_id == node_id:
                    return node
        return None

    def _count_subtree_nodes(self, node: GeneralTreeNode) -> int:
        count = 1
        for child in node.children:
            count += self._count_subtree_nodes(child)
        return count

    @staticmethod
    def _node_to_plain(
        node: GeneralTreeNode,
        level: Optional[int] = None,
        parent_id: Optional[str] = None,
    ) -> dict[str, Any]:
        data = {
            "id": node.node_id,
            "label": node.label,
            "category": node.category,
            "metadata": node.metadata,
            "childrenCount": len(node.children),
        }

        if level is not None:
            data["level"] = level

        if parent_id is not None:
            data["parentId"] = parent_id

        return data

    @staticmethod
    def _normalize_text(value: Any) -> str:
        return str(value).strip()
