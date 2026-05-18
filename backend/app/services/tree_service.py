"""
Application service for the general tree structure.

The service coordinates educational use cases for the REST layer while keeping
GeneralTree independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any, Optional

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.serializers.react_flow_serializer import serialize_general_tree
from app.structures.general_tree import GeneralTree, GeneralTreeNode


class TreeService:
    """Service that exposes academic general-tree operations."""

    def __init__(self) -> None:
        self._tree = GeneralTree()

    def state(self) -> dict[str, Any]:
        """Return the current tree state."""
        return self._build_result()

    def insert(
        self,
        node_id: Any,
        label: Any,
        parent_id: Optional[Any] = None,
        category: str = "academic",
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Insert a node under parent_id, or as root when the tree is empty."""
        normalized_id = self._validate_required_text(node_id, "id")
        normalized_label = self._validate_required_text(label, "label")
        normalized_parent = self._normalize_optional_text(parent_id)
        normalized_category = self._normalize_optional_text(category) or "academic"

        try:
            inserted = self._tree.insert(
                node_id=normalized_id,
                label=normalized_label,
                parent_id=normalized_parent,
                category=normalized_category,
                metadata=metadata or {},
            )
        except ValueError as error:
            self._raise_insert_error(str(error), normalized_id, normalized_parent)
            raise

        result = self._build_result()
        result["inserted"] = self._node_to_result(inserted)
        result["parentId"] = normalized_parent
        return result

    def delete(self, node_id: Any) -> dict[str, Any]:
        """Delete a node and its subtree."""
        normalized_id = self._validate_required_text(node_id, "id")

        if self._tree.is_empty():
            raise StructureEmptyError(
                message="No se puede eliminar porque el árbol está vacío.",
                details=[{"operation": "delete", "issue": "EMPTY_TREE"}],
            )

        removed = self._tree.delete(normalized_id)
        if removed is None:
            raise NotFoundError(
                message="El nodo solicitado no existe en el árbol.",
                details=[{"field": "id", "value": normalized_id, "issue": "NODE_NOT_FOUND"}],
            )

        result = self._build_result()
        result["deleted"] = self._node_to_result(removed)
        return result

    def search(self, node_id: Any) -> dict[str, Any]:
        """Search a node by id."""
        normalized_id = self._validate_required_text(node_id, "id")
        node = self._tree.search(normalized_id)
        result = self._build_result()
        result["query"] = normalized_id
        result["found"] = node is not None
        result["node"] = self._node_to_result(node) if node else None
        result["level"] = self._tree.get_level(normalized_id) if node else None
        return result

    def traverse(self, traversal_type: str = "levelorder") -> dict[str, Any]:
        """Return preorder, postorder, or levelorder traversal."""
        normalized_type = str(traversal_type or "levelorder").strip().lower()

        if normalized_type not in {"preorder", "postorder", "levelorder"}:
            raise ValidationError(
                message="El tipo de recorrido debe ser preorder, postorder o levelorder.",
                details=[{"field": "type", "issue": "INVALID_TRAVERSAL_TYPE"}],
            )

        if normalized_type == "preorder":
            order = self._tree.preorder()
        elif normalized_type == "postorder":
            order = self._tree.postorder()
        else:
            order = self._tree.levelorder()

        result = self._build_result()
        result["traversal"] = {
            "type": normalized_type,
            "start": self._tree.root.node_id if self._tree.root else None,
            "order": [item["id"] for item in order],
            "steps": [
                {
                    "step": index + 1,
                    "id": item["id"],
                    "label": item["label"],
                    "level": item.get("level"),
                }
                for index, item in enumerate(order)
            ],
        }
        return result

    def metrics(self) -> dict[str, Any]:
        """Return tree metrics."""
        result = self._build_result()
        result["metricsOnly"] = True
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load the main academic curriculum demo tree."""
        self._tree.clear()
        demo_nodes = self._demo_nodes()

        for item in demo_nodes:
            self._tree.insert(
                node_id=item["id"],
                label=item["label"],
                parent_id=item.get("parentId"),
                category=item["category"],
                metadata=item.get("metadata", {}),
            )

        result = self._build_result()
        result["loaded"] = demo_nodes
        result["context"] = "Pensum académico jerárquico"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the general tree."""
        self._tree.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        visualization = serialize_general_tree(self._tree.levelorder())
        metrics = self._build_metrics(edges_count=len(visualization["edges"]))
        return {
            "tree": self._tree.to_dict(),
            "size": self._tree.size(),
            "root": self._node_to_result(self._tree.root) if self._tree.root else None,
            "isEmpty": self._tree.is_empty(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
            "metrics": metrics,
        }

    def _build_metrics(self, edges_count: int) -> dict[str, Any]:
        return {
            "count": self._tree.size(),
            "height": self._tree.height(),
            "balanceFactor": None,
            "collisions": None,
            "levels": self._tree.levels_count(),
            "edgesCount": edges_count,
            "leafCount": self._tree.leaf_count(),
            "maxChildren": self._tree.max_children(),
        }

    @staticmethod
    def _node_to_result(node: Optional[GeneralTreeNode]) -> Optional[dict[str, Any]]:
        if node is None:
            return None
        return {
            "id": node.node_id,
            "label": node.label,
            "category": node.category,
            "metadata": node.metadata,
            "childrenCount": len(node.children),
        }

    @staticmethod
    def _validate_required_text(value: Any, field: str) -> str:
        if value is None:
            raise ValidationError(
                message=f"El campo {field} es obligatorio.",
                details=[{"field": field, "issue": "REQUIRED"}],
            )

        normalized = str(value).strip()
        if not normalized:
            raise ValidationError(
                message=f"El campo {field} no puede estar vacío.",
                details=[{"field": field, "issue": "EMPTY_STRING"}],
            )

        return normalized

    @staticmethod
    def _normalize_optional_text(value: Any) -> Optional[str]:
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    @staticmethod
    def _raise_insert_error(code: str, node_id: str, parent_id: Optional[str]) -> None:
        if code == "DUPLICATE_NODE_ID":
            raise DuplicateKeyError(
                message="Ya existe un nodo con el id indicado.",
                details=[{"field": "id", "value": node_id, "issue": "DUPLICATE_NODE_ID"}],
            )

        if code == "PARENT_REQUIRED":
            raise ValidationError(
                message="El campo parentId es obligatorio cuando el árbol ya tiene raíz.",
                details=[{"field": "parentId", "issue": "REQUIRED"}],
            )

        if code == "PARENT_NOT_FOUND":
            raise NotFoundError(
                message="El nodo padre indicado no existe.",
                details=[{"field": "parentId", "value": parent_id, "issue": "PARENT_NOT_FOUND"}],
            )

        raise ValidationError(
            message="No se pudo insertar el nodo en el árbol.",
            details=[{"field": "id", "value": node_id, "issue": code}],
        )

    @staticmethod
    def _demo_nodes() -> list[dict[str, Any]]:
        return [
            {
                "id": "faculty-engineering",
                "label": "Facultad de Ingeniería",
                "category": "faculty",
                "metadata": {"entity": "faculty"},
            },
            {
                "id": "career-systems",
                "label": "Ingeniería en Sistemas",
                "parentId": "faculty-engineering",
                "category": "career",
                "metadata": {"entity": "career"},
            },
            {
                "id": "cycle-1",
                "label": "Ciclo 1",
                "parentId": "career-systems",
                "category": "cycle",
                "metadata": {"entity": "cycle", "number": 1},
            },
            {
                "id": "math-1",
                "label": "Matemática I",
                "parentId": "cycle-1",
                "category": "course",
                "metadata": {"entity": "course", "credits": 5},
            },
            {
                "id": "intro-programming",
                "label": "Introducción a la Programación",
                "parentId": "cycle-1",
                "category": "course",
                "metadata": {"entity": "course", "credits": 5},
            },
            {
                "id": "cycle-2",
                "label": "Ciclo 2",
                "parentId": "career-systems",
                "category": "cycle",
                "metadata": {"entity": "cycle", "number": 2},
            },
            {
                "id": "programming-1",
                "label": "Programación I",
                "parentId": "cycle-2",
                "category": "course",
                "metadata": {"entity": "course", "credits": 5},
            },
            {
                "id": "math-2",
                "label": "Matemática II",
                "parentId": "cycle-2",
                "category": "course",
                "metadata": {"entity": "course", "credits": 5},
            },
        ]
