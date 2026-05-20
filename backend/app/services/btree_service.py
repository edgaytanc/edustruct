"""
Application service for the B-Tree academic index.

The service coordinates educational B-Tree use cases for the REST layer while
keeping the pure structure independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any, Optional

from app.errors.exceptions import DuplicateKeyError, ValidationError
from app.serializers.react_flow_serializer import serialize_btree
from app.structures.btree import BTree, BTreeNode


class BTreeService:
    """Service that exposes B-Tree index operations for academic records."""

    DEFAULT_ORDER = 4

    def __init__(self, order: int = DEFAULT_ORDER) -> None:
        self._tree = self._create_tree(order)

    def state(self) -> dict[str, Any]:
        """Return the current B-Tree state."""
        return self._build_result()

    def configure(self, order: Any) -> dict[str, Any]:
        """Reset the B-Tree using a new order."""
        normalized_order = self._validate_order(order)
        self._tree = BTree(order=normalized_order)
        result = self._build_result()
        result["configured"] = True
        result["operation"] = "configure"
        result["operationOrder"] = normalized_order
        return result

    def insert(self, key: Any) -> dict[str, Any]:
        """Insert one key into the B-Tree and expose split information."""
        normalized_key = self._validate_required_key(key)
        before = self._build_visual_snapshot()
        split_count_before = len(self._tree.split_events)

        try:
            inserted = self._tree.insert(normalized_key)
        except ValueError as error:
            self._raise_structure_error(str(error), normalized_key)
            raise

        new_splits = self._tree.split_events[split_count_before:]
        result = self._build_result(before=before, split_events=new_splits)
        result["inserted"] = inserted
        result["operation"] = "insert"
        result["operationKey"] = inserted
        result["splitOccurred"] = len(new_splits) > 0
        return result

    def bulk_insert(self, keys: list[Any]) -> dict[str, Any]:
        """Insert multiple keys preserving B-Tree invariants after each insert."""
        if not isinstance(keys, list):
            raise ValidationError(
                message="El campo keys debe ser una lista.",
                details=[{"field": "keys", "issue": "MUST_BE_LIST"}],
            )

        before = self._build_visual_snapshot()
        inserted: list[Any] = []
        split_count_before = len(self._tree.split_events)

        for key in keys:
            normalized_key = self._validate_required_key(key)
            try:
                self._tree.insert(normalized_key)
            except ValueError as error:
                self._raise_structure_error(str(error), normalized_key)
            inserted.append(normalized_key)

        new_splits = self._tree.split_events[split_count_before:]
        result = self._build_result(before=before, split_events=new_splits)
        result["inserted"] = inserted
        result["operation"] = "bulk-insert"
        result["splitOccurred"] = len(new_splits) > 0
        return result

    def search(self, key: Any) -> dict[str, Any]:
        """Search a key in the B-Tree academic index."""
        normalized_key = self._validate_required_key(key)
        search_result = self._tree.search(normalized_key)
        result = self._build_result()
        result["query"] = normalized_key
        result["found"] = search_result.found
        result["search"] = search_result.to_dict()
        result["node"] = self._node_to_result(search_result.node) if search_result.node else None
        result["level"] = search_result.level
        result["path"] = search_result.path
        return result

    def traverse(self, traversal_type: str = "levelorder") -> dict[str, Any]:
        """Return levelorder or inorder traversal for the B-Tree."""
        normalized_type = str(traversal_type or "levelorder").strip().lower()

        if normalized_type not in {"levelorder", "inorder"}:
            raise ValidationError(
                message="El tipo de recorrido debe ser levelorder o inorder para el Árbol B.",
                details=[{"field": "type", "issue": "INVALID_TRAVERSAL_TYPE"}],
            )

        result = self._build_result()
        if normalized_type == "inorder":
            order = self._tree.inorder()
            steps = [{"step": index + 1, "key": key} for index, key in enumerate(order)]
        else:
            entries = self._tree.levelorder()
            order = [entry["keys"] for entry in entries]
            steps = [
                {
                    "step": index + 1,
                    "id": entry["id"],
                    "keys": entry["keys"],
                    "leaf": entry["leaf"],
                    "level": entry["level"],
                    "parentId": entry["parentId"],
                    "childIndex": entry["childIndex"],
                }
                for index, entry in enumerate(entries)
            ]

        result["traversal"] = {
            "type": normalized_type,
            "start": self._tree.root.keys if self._tree.root else None,
            "order": order,
            "steps": steps,
        }
        return result

    def metrics(self) -> dict[str, Any]:
        """Return B-Tree metrics."""
        result = self._build_result()
        result["metricsOnly"] = True
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load a deterministic academic-record B-Tree demo."""
        self._tree.clear()
        demo_keys = self._demo_keys()
        for key in demo_keys:
            self._tree.insert(key)

        result = self._build_result(split_events=self._tree.split_events)
        result["loaded"] = demo_keys
        result["context"] = "Árbol B como índice académico de expedientes universitarios"
        result["operation"] = "load-demo"
        result["splitOccurred"] = len(self._tree.split_events) > 0
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the B-Tree state."""
        self._tree.clear()
        result = self._build_result()
        result["reset"] = True
        result["operation"] = "reset"
        return result

    def _build_result(
        self,
        before: Optional[dict[str, Any]] = None,
        split_events: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        visualization = self._build_visual_snapshot()
        events = self._tree.split_events if split_events is None else split_events
        return {
            "tree": self._tree.to_dict(),
            "order": self._tree.order,
            "maxKeys": self._tree.max_keys,
            "minKeys": self._tree.min_keys,
            "size": self._tree.size(),
            "root": self._node_to_result(self._tree.root) if self._tree.root else None,
            "isEmpty": self._tree.is_empty(),
            "isValid": self._tree.validate_invariants(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
            "before": before,
            "after": visualization,
            "splitEvents": events,
            "lastSplit": events[-1] if events else None,
            "metrics": self._build_metrics(edges_count=len(visualization["edges"])),
        }

    def _build_visual_snapshot(self) -> dict[str, Any]:
        items = []
        for entry in self._tree.levelorder():
            item = dict(entry)
            item["maxKeys"] = self._tree.max_keys
            item["label"] = " | ".join(str(key) for key in entry["keys"])
            items.append(item)
        return serialize_btree(items)

    def _build_metrics(self, edges_count: int) -> dict[str, Any]:
        return {
            "count": self._tree.size(),
            "height": self._tree.height(),
            "levels": self._tree.levels_count(),
            "order": self._tree.order,
            "maxKeys": self._tree.max_keys,
            "minKeys": self._tree.min_keys,
            "nodeCount": self._tree.node_count(),
            "leafCount": self._tree.leaf_count(),
            "edgesCount": edges_count,
            "splitCount": len(self._tree.split_events),
            "isValid": self._tree.validate_invariants(),
            "collisions": None,
            "balanceFactor": None,
        }

    @staticmethod
    def _node_to_result(node: Optional[BTreeNode]) -> Optional[dict[str, Any]]:
        if node is None:
            return None
        return {
            "id": "btree-" + "-".join(str(key) for key in node.keys),
            "keys": list(node.keys),
            "label": " | ".join(str(key) for key in node.keys),
            "leaf": node.leaf,
            "keyCount": len(node.keys),
            "childrenCount": len(node.children),
        }

    @classmethod
    def _create_tree(cls, order: Any) -> BTree:
        return BTree(order=cls._validate_order(order))

    @staticmethod
    def _validate_order(order: Any) -> int:
        if isinstance(order, bool) or not isinstance(order, int):
            raise ValidationError(
                message="El orden del Árbol B debe ser un número entero.",
                details=[{"field": "order", "issue": "ORDER_MUST_BE_INTEGER"}],
            )
        if order < 3:
            raise ValidationError(
                message="El orden del Árbol B debe ser mayor o igual a 3.",
                details=[{"field": "order", "issue": "ORDER_MUST_BE_AT_LEAST_3"}],
            )
        return order

    @staticmethod
    def _validate_required_key(key: Any) -> Any:
        if key is None:
            raise ValidationError(
                message="El campo key es obligatorio.",
                details=[{"field": "key", "issue": "REQUIRED"}],
            )
        if isinstance(key, str):
            normalized = key.strip()
            if not normalized:
                raise ValidationError(
                    message="El campo key no puede estar vacío.",
                    details=[{"field": "key", "issue": "EMPTY_STRING"}],
                )
            return normalized
        return key

    @staticmethod
    def _raise_structure_error(code: str, key: Any) -> None:
        if code == "DUPLICATE_KEY":
            raise DuplicateKeyError(
                message="Ya existe una clave igual en el Árbol B.",
                details=[{"field": "key", "value": key, "issue": "DUPLICATE_KEY"}],
            )
        if code == "KEY_REQUIRED":
            raise ValidationError(
                message="El campo key es obligatorio.",
                details=[{"field": "key", "issue": "REQUIRED"}],
            )
        if code == "INCOMPARABLE_KEY":
            raise ValidationError(
                message="La clave no puede compararse con las claves existentes del Árbol B.",
                details=[{"field": "key", "value": key, "issue": "INCOMPARABLE_KEY"}],
            )
        raise ValidationError(
            message="No fue posible aplicar la operación sobre el Árbol B.",
            details=[{"field": "key", "value": key, "issue": code}],
        )

    @staticmethod
    def _demo_keys() -> list[int]:
        return [2024008, 2024016, 2024024, 2024032, 2024040, 2024048, 2024056, 2024064, 2024072, 2024080, 2024088]
