"""
Application service for the binary tree structure.

The service coordinates educational BST use cases for the REST layer while
keeping BinaryTree independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any, Optional

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.structures.binary_tree import BinaryTree, BinaryTreeNode


class BinaryTreeService:
    """Service that exposes binary-search-tree operations."""

    def __init__(self) -> None:
        self._tree = BinaryTree()

    def state(self) -> dict[str, Any]:
        """Return the current binary tree state."""
        return self._build_result()

    def insert(self, value: Any) -> dict[str, Any]:
        """Insert a comparable value into the BST."""
        normalized_value = self._validate_required_value(value, "value")

        try:
            inserted = self._tree.insert(normalized_value)
        except ValueError as error:
            self._raise_insert_error(str(error), normalized_value)
            raise

        result = self._build_result()
        result["inserted"] = self._node_to_result(inserted)
        return result

    def delete(self, value: Any) -> dict[str, Any]:
        """Delete a value from the BST."""
        normalized_value = self._validate_required_value(value, "value")

        if self._tree.is_empty():
            raise StructureEmptyError(
                message="No se puede eliminar porque el árbol binario está vacío.",
                details=[{"operation": "delete", "issue": "EMPTY_TREE"}],
            )

        removed = self._tree.delete(normalized_value)
        if removed is None:
            raise NotFoundError(
                message="El valor solicitado no existe en el árbol binario.",
                details=[{"field": "value", "value": normalized_value, "issue": "VALUE_NOT_FOUND"}],
            )

        result = self._build_result()
        result["deleted"] = self._node_to_result(removed)
        return result

    def search(self, value: Any) -> dict[str, Any]:
        """Search a value in the BST."""
        normalized_value = self._validate_required_value(value, "value")
        node = self._tree.search(normalized_value)
        result = self._build_result()
        result["query"] = normalized_value
        result["found"] = node is not None
        result["node"] = self._node_to_result(node) if node else None
        result["level"] = self._tree.get_level(normalized_value) if node else None
        return result

    def traverse(self, traversal_type: str = "levelorder") -> dict[str, Any]:
        """Return preorder, inorder, postorder, or levelorder traversal."""
        normalized_type = str(traversal_type or "levelorder").strip().lower()

        if normalized_type not in {"preorder", "inorder", "postorder", "levelorder"}:
            raise ValidationError(
                message="El tipo de recorrido debe ser preorder, inorder, postorder o levelorder.",
                details=[{"field": "type", "issue": "INVALID_TRAVERSAL_TYPE"}],
            )

        if normalized_type == "preorder":
            order = self._tree.preorder()
        elif normalized_type == "inorder":
            order = self._tree.inorder()
        elif normalized_type == "postorder":
            order = self._tree.postorder()
        else:
            order = self._tree.levelorder()

        result = self._build_result()
        result["traversal"] = {
            "type": normalized_type,
            "start": self._tree.root.value if self._tree.root else None,
            "order": [item["value"] for item in order],
            "steps": [
                {
                    "step": index + 1,
                    "id": item["id"],
                    "value": item["value"],
                    "label": item["label"],
                    "level": item.get("level"),
                    "direction": item.get("direction"),
                }
                for index, item in enumerate(order)
            ],
        }
        return result

    def metrics(self) -> dict[str, Any]:
        """Return binary tree metrics."""
        result = self._build_result()
        result["metricsOnly"] = True
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load a deterministic educational BST demo."""
        self._tree.clear()
        demo_values = self._demo_values()

        for value in demo_values:
            self._tree.insert(value)

        result = self._build_result()
        result["loaded"] = demo_values
        result["context"] = "Árbol binario de decisión académica por prioridad numérica"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the binary tree."""
        self._tree.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        nodes = self._tree.levelorder()
        return {
            "tree": self._tree.to_dict(),
            "size": self._tree.size(),
            "root": self._node_to_result(self._tree.root) if self._tree.root else None,
            "isEmpty": self._tree.is_empty(),
            "nodes": nodes,
            "edges": self._build_plain_edges(nodes),
            "metrics": self._build_metrics(),
        }

    def _build_metrics(self) -> dict[str, Any]:
        return {
            "count": self._tree.size(),
            "height": self._tree.height(),
            "balanceFactor": self._tree.balance_factor(),
            "collisions": None,
            "levels": self._tree.levels_count(),
            "edgesCount": self._tree.edges_count(),
            "leafCount": self._tree.leaf_count(),
        }

    @staticmethod
    def _build_plain_edges(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        edges: list[dict[str, Any]] = []
        for node in nodes:
            parent_id = node.get("parentId")
            if parent_id is not None:
                edges.append(
                    {
                        "id": f"binary-tree-edge-{parent_id}-{node['id']}",
                        "source": parent_id,
                        "target": node["id"],
                        "relationship": node.get("direction"),
                    }
                )
        return edges

    @staticmethod
    def _node_to_result(node: Optional[BinaryTreeNode]) -> Optional[dict[str, Any]]:
        if node is None:
            return None
        return {
            "id": str(node.value),
            "value": node.value,
            "label": str(node.value),
            "hasLeft": node.left is not None,
            "hasRight": node.right is not None,
            "childrenCount": int(node.left is not None) + int(node.right is not None),
        }

    @staticmethod
    def _validate_required_value(value: Any, field: str) -> Any:
        if value is None:
            raise ValidationError(
                message=f"El campo {field} es obligatorio.",
                details=[{"field": field, "issue": "REQUIRED"}],
            )

        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                raise ValidationError(
                    message=f"El campo {field} no puede estar vacío.",
                    details=[{"field": field, "issue": "EMPTY_STRING"}],
                )
            return normalized

        return value

    @staticmethod
    def _raise_insert_error(code: str, value: Any) -> None:
        if code == "DUPLICATE_VALUE":
            raise DuplicateKeyError(
                message="Ya existe un nodo con el valor indicado.",
                details=[{"field": "value", "value": value, "issue": "DUPLICATE_VALUE"}],
            )

        if code == "VALUE_REQUIRED":
            raise ValidationError(
                message="El campo value es obligatorio.",
                details=[{"field": "value", "issue": "REQUIRED"}],
            )

        if code == "INCOMPARABLE_VALUE":
            raise ValidationError(
                message="El valor no puede compararse con los valores existentes del árbol.",
                details=[{"field": "value", "value": value, "issue": "INCOMPARABLE_VALUE"}],
            )

        raise ValidationError(
            message="No se pudo insertar el valor en el árbol binario.",
            details=[{"field": "value", "value": value, "issue": code}],
        )

    @staticmethod
    def _demo_values() -> list[int]:
        return [50, 25, 75, 10, 40, 60, 90]
