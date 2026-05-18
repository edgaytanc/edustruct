"""
Application service for the AVL tree structure.

The service coordinates educational AVL use cases for the REST layer while
keeping AVLTree independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any, Optional

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.serializers.react_flow_serializer import serialize_avl_tree
from app.structures.avl_tree import AVLNode, AVLTree


class AVLService:
    """Service that exposes self-balancing AVL tree operations."""

    def __init__(self) -> None:
        self._tree = AVLTree()

    def state(self) -> dict[str, Any]:
        """Return the current AVL tree state."""
        return self._build_result()

    def insert(self, value: Any) -> dict[str, Any]:
        """Insert a comparable value into the AVL tree and report rotations."""
        normalized_value = self._validate_required_value(value, "value")
        before = self._build_visual_snapshot()

        try:
            inserted = self._tree.insert(normalized_value)
        except ValueError as error:
            self._raise_insert_error(str(error), normalized_value)
            raise

        result = self._build_result(before=before)
        result["inserted"] = self._node_to_result(inserted)
        result["operation"] = "insert"
        result["operationValue"] = normalized_value
        return result

    def delete(self, value: Any) -> dict[str, Any]:
        """Delete a value from the AVL tree and rebalance if needed."""
        normalized_value = self._validate_required_value(value, "value")

        if self._tree.is_empty():
            raise StructureEmptyError(
                message="No se puede eliminar porque el árbol AVL está vacío.",
                details=[{"operation": "delete", "issue": "EMPTY_TREE"}],
            )

        before = self._build_visual_snapshot()
        removed = self._tree.delete(normalized_value)
        if removed is None:
            raise NotFoundError(
                message="El valor solicitado no existe en el árbol AVL.",
                details=[{"field": "value", "value": normalized_value, "issue": "VALUE_NOT_FOUND"}],
            )

        result = self._build_result(before=before)
        result["deleted"] = self._node_to_result(removed)
        result["operation"] = "delete"
        result["operationValue"] = normalized_value
        return result

    def search(self, value: Any) -> dict[str, Any]:
        """Search a value in the AVL tree."""
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
                    "height": item.get("height"),
                    "balanceFactor": item.get("balanceFactor"),
                    "level": item.get("level"),
                    "direction": item.get("direction"),
                }
                for index, item in enumerate(order)
            ],
        }
        return result

    def metrics(self) -> dict[str, Any]:
        """Return AVL tree metrics."""
        result = self._build_result()
        result["metricsOnly"] = True
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load a deterministic educational AVL demo with visible rotations."""
        self._tree.clear()
        demo_values = self._demo_values()
        accumulated_rotations: list[dict[str, Any]] = []

        for value in demo_values:
            self._tree.insert(value)
            accumulated_rotations.extend(self._tree.rotation_events)

        result = self._build_result(rotation_events=accumulated_rotations)
        result["loaded"] = demo_values
        result["context"] = "Árbol AVL de búsqueda eficiente por ID académico"
        result["operation"] = "load-demo"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the AVL tree."""
        self._tree.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(
        self,
        before: Optional[dict[str, Any]] = None,
        rotation_events: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        visualization = self._build_visual_snapshot()
        events = self._tree.rotation_events if rotation_events is None else rotation_events
        return {
            "tree": self._tree.to_dict(),
            "size": self._tree.size(),
            "root": self._node_to_result(self._tree.root) if self._tree.root else None,
            "isEmpty": self._tree.is_empty(),
            "isBalanced": self._tree.is_balanced(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
            "before": before,
            "after": visualization,
            "rotationEvents": events,
            "lastRotation": events[-1] if events else None,
            "metrics": self._build_metrics(edges_count=len(visualization["edges"])),
        }

    def _build_visual_snapshot(self) -> dict[str, Any]:
        return serialize_avl_tree(self._tree.levelorder())

    def _build_metrics(self, edges_count: int) -> dict[str, Any]:
        return {
            "count": self._tree.size(),
            "height": self._tree.height(),
            "balanceFactor": self._tree.balance_factor(),
            "collisions": None,
            "levels": self._tree.levels_count(),
            "edgesCount": edges_count,
            "leafCount": self._tree.leaf_count(),
            "isBalanced": self._tree.is_balanced(),
            "rotationCount": len(self._tree.rotation_events),
        }

    @staticmethod
    def _node_to_result(node: Optional[AVLNode]) -> Optional[dict[str, Any]]:
        if node is None:
            return None

        balance_factor = node.balance_factor()
        return {
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
                message="Ya existe un nodo con el valor indicado en el árbol AVL.",
                details=[{"field": "value", "value": value, "issue": "DUPLICATE_VALUE"}],
            )

        if code == "VALUE_REQUIRED":
            raise ValidationError(
                message="El campo value es obligatorio.",
                details=[{"field": "value", "issue": "REQUIRED"}],
            )

        if code == "INCOMPARABLE_VALUE":
            raise ValidationError(
                message="El valor no puede compararse con los valores existentes del árbol AVL.",
                details=[{"field": "value", "value": value, "issue": "INCOMPARABLE_VALUE"}],
            )

        raise ValidationError(
            message="No se pudo insertar el valor en el árbol AVL.",
            details=[{"field": "value", "value": value, "issue": code}],
        )

    @staticmethod
    def _demo_values() -> list[int]:
        return [10, 20, 50, 25, 27, 40, 30]
