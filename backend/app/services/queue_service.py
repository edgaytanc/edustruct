"""
Application service for the queue structure.

The service owns the in-memory queue instance used by the REST endpoints and
keeps HTTP-specific code outside the pure Queue implementation.
"""

from __future__ import annotations

from typing import Any

from app.errors.exceptions import StructureEmptyError, ValidationError
from app.structures.queue import Queue


class QueueService:
    """Service that exposes educational queue operations."""

    def __init__(self) -> None:
        self._queue = Queue()

    def state(self) -> dict[str, Any]:
        """Return the current queue state from front to rear."""
        return self._build_result()

    def enqueue(self, value: Any) -> dict[str, Any]:
        """Add a value to the rear of the queue."""
        self._validate_value(value)
        self._queue.enqueue(value)

        result = self._build_result()
        result["enqueued"] = value
        return result

    def dequeue(self) -> dict[str, Any]:
        """Remove the value at the front of the queue."""
        if self._queue.is_empty():
            raise StructureEmptyError(
                message="No se puede desencolar porque la cola está vacía.",
                details=[{"operation": "dequeue", "issue": "EMPTY_QUEUE"}],
            )

        value = self._queue.dequeue()
        result = self._build_result()
        result["dequeued"] = value
        return result

    def front(self) -> dict[str, Any]:
        """Return the front value without removing it."""
        if self._queue.is_empty():
            raise StructureEmptyError(
                message="No se puede consultar el frente porque la cola está vacía.",
                details=[{"operation": "front", "issue": "EMPTY_QUEUE"}],
            )

        result = self._build_result()
        result["front"] = self._queue.front()
        return result

    def search(self, value: Any) -> dict[str, Any]:
        """Search for a value from front to rear."""
        self._validate_value(value)
        items = self._queue.to_list()

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
        result["indexFromFront"] = index
        return result

    def traverse(self) -> dict[str, Any]:
        """Return the queue traversal order from front to rear."""
        items = self._queue.to_list()
        result = self._build_result()
        result["traversal"] = {
            "type": "queue-front-to-rear",
            "start": "front",
            "order": items,
            "steps": [
                {"indexFromFront": index, "value": value}
                for index, value in enumerate(items)
            ],
        }
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load an educational demo queue for advisory turns."""
        self._queue.clear()
        demo_values = [
            "Turno 1 - Ana López",
            "Turno 2 - Carlos Méndez",
            "Turno 3 - Sofía Ramírez",
        ]

        for value in demo_values:
            self._queue.enqueue(value)

        result = self._build_result()
        result["loaded"] = demo_values
        result["context"] = "Cola de turnos de asesoría académica"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the queue."""
        self._queue.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        items = self._queue.to_list()
        return {
            "items": items,
            "size": self._queue.size(),
            "front": items[0] if items else None,
            "rear": items[-1] if items else None,
            "isEmpty": self._queue.is_empty(),
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
