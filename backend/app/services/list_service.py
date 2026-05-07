"""
Application service for the linked-list structure.

This module coordinates use cases for the REST layer while keeping the pure
LinkedList implementation independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any

from app.errors.exceptions import NotFoundError, ValidationError
from app.structures.list_model import LinkedList


class ListService:
    """Service that exposes educational linked-list operations."""

    def __init__(self) -> None:
        self._list = LinkedList()

    def state(self) -> dict[str, Any]:
        """Return the current linked-list state."""
        return self._build_result()

    def insert(self, value: Any, position: str = "tail") -> dict[str, Any]:
        """Insert a value at the head or tail of the linked list."""
        self._validate_value(value)

        normalized_position = self._normalize_position(position)

        if normalized_position == "head":
            self._list.prepend(value)
        else:
            self._list.append(value)

        result = self._build_result()
        result["inserted"] = value
        result["position"] = normalized_position
        return result

    def delete(self, value: Any) -> dict[str, Any]:
        """Delete the first matching value from the linked list."""
        self._validate_value(value)

        removed = self._list.remove(value)
        if not removed:
            raise NotFoundError(
                message="El valor solicitado no existe en la lista.",
                details=[{"field": "value", "issue": "VALUE_NOT_FOUND"}],
            )

        result = self._build_result()
        result["deleted"] = value
        return result

    def search(self, value: Any) -> dict[str, Any]:
        """Search for a value in the linked list."""
        self._validate_value(value)
        items = self._list.to_list()

        found = False
        index = None

        for current_index, item in enumerate(items):
            if item == value:
                found = True
                index = current_index
                break

        result = self._build_result()
        result["query"] = value
        result["found"] = found
        result["index"] = index
        return result

    def traverse(self) -> dict[str, Any]:
        """Return the traversal order from head to tail."""
        result = self._build_result()
        result["traversal"] = {
            "type": "linear",
            "start": "head",
            "order": self._list.to_list(),
            "steps": [
                {"index": index, "value": value}
                for index, value in enumerate(self._list.to_list())
            ],
        }
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load an educational demo list of enrolled students."""
        self._list.clear()
        demo_values = [
            "2024001 - Ana López",
            "2024002 - Carlos Méndez",
            "2024003 - Sofía Ramírez",
        ]

        for value in demo_values:
            self._list.append(value)

        result = self._build_result()
        result["loaded"] = demo_values
        result["context"] = "Lista de estudiantes inscritos"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the linked list."""
        self._list.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        items = self._list.to_list()
        return {
            "items": items,
            "size": self._list.size(),
            "head": items[0] if items else None,
            "tail": items[-1] if items else None,
            "isEmpty": self._list.is_empty(),
        }

    @staticmethod
    def _validate_value(value: Any) -> None:
        if value is None:
            raise ValidationError(
                message="El campo value es obligatorio.",
                details=[{"field": "value", "issue": "REQUIRED"}],
            )

        if isinstance(value, str) and not value.strip():
            raise ValidationError(
                message="El campo value no puede estar vacío.",
                details=[{"field": "value", "issue": "EMPTY_STRING"}],
            )

    @staticmethod
    def _normalize_position(position: str) -> str:
        if position is None:
            return "tail"

        normalized_position = str(position).strip().lower()
        if normalized_position not in {"head", "tail"}:
            raise ValidationError(
                message="La posición debe ser head o tail.",
                details=[{"field": "position", "issue": "INVALID_POSITION"}],
            )

        return normalized_position
