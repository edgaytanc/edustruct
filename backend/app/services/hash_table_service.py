"""
Application service for the EduStruct hash table.

The service coordinates educational hash-table use cases for the REST layer
while keeping HashTable independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any, Optional

from app.errors.exceptions import DuplicateKeyError, NotFoundError, StructureEmptyError, ValidationError
from app.serializers.react_flow_serializer import serialize_hash_table
from app.structures.hash_table import HashEntry, HashSearchResult, HashTable


class HashTableService:
    """Service that exposes hash-table operations for student carnet lookup."""

    DEFAULT_CAPACITY = 7

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self._table = self._create_table(capacity)

    def state(self) -> dict[str, Any]:
        """Return the current hash table state."""
        return self._build_result()

    def configure(self, capacity: Any) -> dict[str, Any]:
        """Reset the hash table with a new bucket capacity."""
        normalized_capacity = self._validate_capacity(capacity)
        self._table = HashTable(capacity=normalized_capacity)
        result = self._build_result()
        result["configured"] = True
        result["operation"] = "configure"
        result["operationCapacity"] = normalized_capacity
        return result

    def insert(self, key: Any, value: Any) -> dict[str, Any]:
        """Insert one key/value pair and expose collision metadata."""
        normalized_key = self._validate_required_key(key)
        normalized_value = self._validate_required_value(value)
        before = self._build_visual_snapshot()
        collisions_before = self._table.collisions

        try:
            inserted = self._table.insert(normalized_key, normalized_value)
        except ValueError as error:
            self._raise_structure_error(str(error), normalized_key)
            raise

        collision_occurred = self._table.collisions > collisions_before
        result = self._build_result(before=before)
        result["inserted"] = self._entry_to_result(inserted)
        result["operation"] = "insert"
        result["operationKey"] = normalized_key
        result["collisionOccurred"] = collision_occurred
        return result

    def bulk_insert(self, entries: list[dict[str, Any]]) -> dict[str, Any]:
        """Insert multiple entries preserving manual hash-table behavior."""
        if not isinstance(entries, list):
            raise ValidationError(
                message="El campo entries debe ser una lista.",
                details=[{"field": "entries", "issue": "MUST_BE_LIST"}],
            )

        before = self._build_visual_snapshot()
        inserted: list[dict[str, Any]] = []
        collisions_before = self._table.collisions

        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise ValidationError(
                    message="Cada entrada debe tener formato de objeto con key y value.",
                    details=[{"field": f"entries[{index}]", "issue": "MUST_BE_OBJECT"}],
                )
            normalized_key = self._validate_required_key(entry.get("key"))
            normalized_value = self._validate_required_value(entry.get("value"))
            try:
                created = self._table.insert(normalized_key, normalized_value)
            except ValueError as error:
                self._raise_structure_error(str(error), normalized_key)
            inserted.append(self._entry_to_result(created))

        result = self._build_result(before=before)
        result["inserted"] = inserted
        result["operation"] = "bulk-insert"
        result["collisionOccurred"] = self._table.collisions > collisions_before
        return result

    def search(self, key: Any) -> dict[str, Any]:
        """Search a student by carnet key."""
        normalized_key = self._validate_required_key(key)
        search_result = self._table.search(normalized_key)
        result = self._build_result()
        result["query"] = normalized_key
        result["found"] = search_result.found
        result["search"] = search_result.to_dict()
        result["bucketIndex"] = search_result.bucket_index
        result["chainPosition"] = search_result.chain_position
        result["value"] = search_result.value if search_result.found else None
        return result

    def delete(self, key: Any) -> dict[str, Any]:
        """Delete a key from the hash table."""
        normalized_key = self._validate_required_key(key)

        if self._table.is_empty():
            raise StructureEmptyError(
                message="No se puede eliminar porque la tabla hash está vacía.",
                details=[{"operation": "delete", "issue": "EMPTY_HASH_TABLE"}],
            )

        before = self._build_visual_snapshot()
        search_result = self._table.search(normalized_key)
        deleted = self._table.delete(normalized_key)
        if not deleted:
            raise NotFoundError(
                message="La clave solicitada no existe en la tabla hash.",
                details=[{"field": "key", "value": normalized_key, "issue": "KEY_NOT_FOUND"}],
            )

        result = self._build_result(before=before)
        result["deleted"] = {
            "key": normalized_key,
            "value": search_result.value,
            "bucketIndex": search_result.bucket_index,
            "chainPosition": search_result.chain_position,
        }
        result["operation"] = "delete"
        result["operationKey"] = normalized_key
        return result

    def metrics(self) -> dict[str, Any]:
        """Return hash table metrics."""
        result = self._build_result()
        result["metricsOnly"] = True
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load a deterministic student-carnet demo with visible collisions."""
        self._table.clear()
        demo_entries = self._demo_entries()
        for entry in demo_entries:
            self._table.insert(entry["key"], entry["value"])

        result = self._build_result()
        result["loaded"] = demo_entries
        result["context"] = "Tabla hash para búsqueda de estudiantes por carnet universitario"
        result["operation"] = "load-demo"
        result["collisionOccurred"] = self._table.collisions > 0
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the hash table."""
        self._table.clear()
        result = self._build_result()
        result["reset"] = True
        result["operation"] = "reset"
        return result

    def _build_result(self, before: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        visualization = self._build_visual_snapshot()
        return {
            "table": self._table.to_dict(),
            "capacity": self._table.capacity,
            "size": self._table.size(),
            "isEmpty": self._table.is_empty(),
            "buckets": self._table.buckets_snapshot(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
            "before": before,
            "after": visualization,
            "lastOperation": self._table.last_operation,
            "metrics": self._build_metrics(edges_count=len(visualization["edges"])),
        }

    def _build_visual_snapshot(self) -> dict[str, Any]:
        return serialize_hash_table(
            buckets=self._table.buckets_snapshot(),
            metrics=self._build_metrics(edges_count=0),
            last_operation=self._table.last_operation,
        )

    def _build_metrics(self, edges_count: int) -> dict[str, Any]:
        return {
            "count": self._table.size(),
            "height": None,
            "balanceFactor": None,
            "collisions": self._table.collisions,
            "levels": None,
            "edgesCount": edges_count,
            "capacity": self._table.capacity,
            "loadFactor": self._table.load_factor(),
            "maxChainLength": self._table.max_chain_length(),
            "collisionBucketCount": self._table.collision_bucket_count(),
            "emptyBucketCount": self._table.capacity - sum(1 for bucket in self._table.buckets_snapshot() if bucket["size"] > 0),
        }

    @staticmethod
    def _entry_to_result(entry: HashEntry) -> dict[str, Any]:
        return entry.to_dict()

    @classmethod
    def _create_table(cls, capacity: Any) -> HashTable:
        return HashTable(capacity=cls._validate_capacity(capacity))

    @staticmethod
    def _validate_capacity(capacity: Any) -> int:
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise ValidationError(
                message="La capacidad de la tabla hash debe ser un número entero.",
                details=[{"field": "capacity", "issue": "CAPACITY_MUST_BE_INTEGER"}],
            )
        if capacity < 3:
            raise ValidationError(
                message="La capacidad de la tabla hash debe ser mayor o igual a 3.",
                details=[{"field": "capacity", "issue": "CAPACITY_MUST_BE_AT_LEAST_3"}],
            )
        return capacity

    @staticmethod
    def _validate_required_key(key: Any) -> str:
        if key is None:
            raise ValidationError(
                message="El campo key es obligatorio.",
                details=[{"field": "key", "issue": "REQUIRED"}],
            )
        normalized = str(key).strip()
        if not normalized:
            raise ValidationError(
                message="El campo key no puede estar vacío.",
                details=[{"field": "key", "issue": "EMPTY_STRING"}],
            )
        return normalized

    @staticmethod
    def _validate_required_value(value: Any) -> Any:
        if value is None:
            raise ValidationError(
                message="El campo value es obligatorio.",
                details=[{"field": "value", "issue": "REQUIRED"}],
            )
        return value

    @staticmethod
    def _raise_structure_error(code: str, key: Any) -> None:
        if code == "DUPLICATE_KEY":
            raise DuplicateKeyError(
                message="Ya existe una clave igual en la tabla hash.",
                details=[{"field": "key", "value": key, "issue": "DUPLICATE_KEY"}],
            )
        if code == "KEY_REQUIRED":
            raise ValidationError(
                message="El campo key es obligatorio.",
                details=[{"field": "key", "issue": "REQUIRED"}],
            )
        raise ValidationError(
            message="No fue posible aplicar la operación sobre la tabla hash.",
            details=[{"field": "key", "value": key, "issue": code}],
        )

    @staticmethod
    def _demo_entries() -> list[dict[str, Any]]:
        return [
            {
                "key": "2024001",
                "value": {
                    "student_id": "STU-001",
                    "full_name": "Andrea Morales",
                    "career_id": "CAR-ING-SIS",
                    "status": "active",
                },
            },
            {
                "key": "2024002",
                "value": {
                    "student_id": "STU-010",
                    "full_name": "Luis Hernández",
                    "career_id": "CAR-ING-SIS",
                    "status": "active",
                },
            },
            {
                "key": "2024003",
                "value": {
                    "student_id": "STU-020",
                    "full_name": "María López",
                    "career_id": "CAR-ING-SIS",
                    "status": "active",
                },
            },
            {
                "key": "2024004",
                "value": {
                    "student_id": "STU-030",
                    "full_name": "Carlos Pérez",
                    "career_id": "CAR-ING-SIS",
                    "status": "inactive",
                },
            },
            {
                "key": "2024005",
                "value": {
                    "student_id": "STU-040",
                    "full_name": "Sofía Castillo",
                    "career_id": "CAR-ING-SIS",
                    "status": "active",
                },
            },
        ]
