"""
Application service for the queue structure.

The service owns the in-memory queue instance used by the REST endpoints and
keeps HTTP-specific code outside the pure Queue implementation.
"""

from __future__ import annotations

from typing import Any

from app.errors.exceptions import DatasetError, StructureEmptyError, ValidationError
from app.serializers.react_flow_serializer import serialize_queue
from app.structures.queue import Queue
from app.utils.dataset_loader import load_advisory_turns, load_students_by_carnet


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

    def get_advisory_turns(self) -> dict[str, Any]:
        """Return advisory turns enriched with student information."""
        turns = self._build_advisory_turns()
        return {
            "turns": turns,
            "count": len(turns),
            "context": "Turnos de asesoría académica",
            "sourceDataset": "advisory_turns.json",
        }

    def load_advisory_turns_demo(self) -> dict[str, Any]:
        """Load real advisory turns into the queue preserving FIFO order."""
        self._queue.clear()
        turns = self._build_advisory_turns()
        labels = []

        for turn in turns:
            label = self._format_advisory_turn_label(turn)
            labels.append(label)
            self._queue.enqueue(label)

        result = self._build_result()
        result["loaded"] = labels
        result["advisoryTurns"] = turns
        result["context"] = "Cola de turnos de asesoría académica"
        result["sourceDataset"] = "advisory_turns.json"
        result["queuePolicy"] = "FIFO"
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load an educational demo queue for advisory turns."""
        return self.load_advisory_turns_demo()

    def reset(self) -> dict[str, Any]:
        """Clear the queue."""
        self._queue.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        items = self._queue.to_list()
        visualization = serialize_queue(items)
        return {
            "items": items,
            "size": self._queue.size(),
            "front": items[0] if items else None,
            "rear": items[-1] if items else None,
            "isEmpty": self._queue.is_empty(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
        }

    def _build_advisory_turns(self) -> list[dict[str, Any]]:
        turns = load_advisory_turns()
        students_by_carnet = load_students_by_carnet()
        enriched_turns = []

        for index, turn in enumerate(turns):
            turn_id = self._required_dataset_field(
                record=turn,
                field="id",
                dataset="advisory_turns.json",
                index=index,
            )
            carnet = self._required_dataset_field(
                record=turn,
                field="student_carnet",
                dataset="advisory_turns.json",
                index=index,
            )
            reason = self._required_dataset_field(
                record=turn,
                field="reason",
                dataset="advisory_turns.json",
                index=index,
            )

            student = students_by_carnet.get(carnet)
            if student is None:
                raise DatasetError(
                    message="El turno de asesoría referencia un estudiante inexistente.",
                    details=[
                        {
                            "dataset": "advisory_turns.json",
                            "student_carnet": carnet,
                            "turnId": turn_id,
                            "issue": "STUDENT_NOT_FOUND",
                        }
                    ],
                )

            enriched_turns.append(
                {
                    "id": turn_id,
                    "studentCarnet": carnet,
                    "studentName": student.get("name"),
                    "studentEmail": student.get("email"),
                    "studentStatus": student.get("status"),
                    "reason": reason,
                    "status": turn.get("status"),
                    "createdAt": turn.get("created_at"),
                    "queuePosition": index,
                    "isFront": index == 0,
                }
            )

        return enriched_turns

    @staticmethod
    def _format_advisory_turn_label(turn: dict[str, Any]) -> str:
        return (
            f"{turn['id']} - {turn['studentCarnet']} - "
            f"{turn['studentName']} - {turn['reason']}"
        )

    @staticmethod
    def _required_dataset_field(
        record: dict[str, Any],
        field: str,
        dataset: str,
        index: int,
    ) -> str:
        value = record.get(field)
        if value is None or not str(value).strip():
            raise DatasetError(
                message="El dataset contiene un registro incompleto.",
                details=[
                    {
                        "dataset": dataset,
                        "index": index,
                        "field": field,
                        "issue": "REQUIRED",
                    }
                ],
            )

        return str(value).strip()

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
