"""
Application service for the stack structure.

The service owns the in-memory stack instance used by the REST endpoints and
keeps HTTP-specific code outside the pure Stack implementation.
"""

from __future__ import annotations

from typing import Any

from app.errors.exceptions import StructureEmptyError, ValidationError
from app.serializers.react_flow_serializer import serialize_stack
from app.structures.stack import Stack


class StackService:
    """Service that exposes educational stack operations."""

    DEFAULT_NAVIGATION_HISTORY = [
        "Dashboard Académico",
        "Pensum Ingeniería en Sistemas",
        "Curso CUR-013 - Programación III",
        "Prerrequisitos del curso",
        "Expediente Estudiantil",
    ]

    def __init__(self) -> None:
        self._stack = Stack()

    def state(self) -> dict[str, Any]:
        """Return the current stack state from top to bottom."""
        return self._build_result()

    def push(self, value: Any) -> dict[str, Any]:
        """Push a value onto the stack."""
        self._validate_value(value)
        self._stack.push(value)

        result = self._build_result()
        result["pushed"] = value
        return result

    def pop(self) -> dict[str, Any]:
        """Pop the top value from the stack."""
        if self._stack.is_empty():
            raise StructureEmptyError(
                message="No se puede desapilar porque la pila está vacía.",
                details=[{"operation": "pop", "issue": "EMPTY_STACK"}],
            )

        value = self._stack.pop()
        result = self._build_result()
        result["popped"] = value
        return result

    def peek(self) -> dict[str, Any]:
        """Return the top value without removing it."""
        if self._stack.is_empty():
            raise StructureEmptyError(
                message="No se puede consultar el tope porque la pila está vacía.",
                details=[{"operation": "peek", "issue": "EMPTY_STACK"}],
            )

        result = self._build_result()
        result["peek"] = self._stack.peek()
        return result

    def search(self, value: Any) -> dict[str, Any]:
        """Search for a value from top to bottom."""
        self._validate_value(value)
        items = self._stack.to_list()

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
        result["indexFromTop"] = index
        return result

    def traverse(self) -> dict[str, Any]:
        """Return the stack traversal order from top to bottom."""
        items = self._stack.to_list()
        result = self._build_result()
        result["traversal"] = {
            "type": "stack-top-to-bottom",
            "start": "top",
            "order": items,
            "steps": [
                {"indexFromTop": index, "value": value}
                for index, value in enumerate(items)
            ],
        }
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load the default academic navigation history demo."""
        return self.load_navigation_history_demo()

    def load_navigation_history_demo(self) -> dict[str, Any]:
        """Load a contextual academic navigation history into the stack."""
        self._stack.clear()

        for module in self.DEFAULT_NAVIGATION_HISTORY:
            self._stack.push(module)

        result = self._build_result()
        result["loaded"] = list(self.DEFAULT_NAVIGATION_HISTORY)
        result["context"] = "Historial de navegación académica"
        result["navigationPolicy"] = "LIFO"
        result["businessCase"] = "Botón atrás / deshacer navegación dentro del sistema académico"
        return result

    def navigate_to_module(self, module: Any) -> dict[str, Any]:
        """Push a newly visited academic module onto the navigation stack."""
        self._validate_value(module, field="module")
        self._stack.push(module)

        result = self._build_result()
        result["navigatedTo"] = module
        result["navigationAction"] = "push"
        result["context"] = "Nueva consulta académica registrada en el historial"
        result["navigationPolicy"] = "LIFO"
        return result

    def back(self) -> dict[str, Any]:
        """Go back by popping the current academic module from the stack."""
        if self._stack.is_empty():
            raise StructureEmptyError(
                message="No se puede retroceder porque el historial académico está vacío.",
                details=[{"operation": "navigation-back", "issue": "EMPTY_STACK"}],
            )

        previous_top = self._stack.pop()
        result = self._build_result()
        result["backFrom"] = previous_top
        result["navigationAction"] = "back"
        result["currentModule"] = result.get("top")
        result["context"] = "Retroceso de navegación académica ejecutado"
        result["navigationPolicy"] = "LIFO"
        return result

    def reset(self) -> dict[str, Any]:
        """Clear the stack."""
        self._stack.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        items = self._stack.to_list()
        visualization = serialize_stack(items)
        return {
            "items": items,
            "size": self._stack.size(),
            "top": items[0] if items else None,
            "isEmpty": self._stack.is_empty(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
            "context": "Historial de navegación académica",
            "navigationPolicy": "LIFO",
        }

    @staticmethod
    def _validate_value(value: Any, field: str = "value") -> None:
        if value is None:
            raise ValidationError(
                message=f"El campo {field} es obligatorio.",
                details=[{"field": field, "issue": "REQUIRED"}],
            )

        if isinstance(value, str) and not value.strip():
            raise ValidationError(
                message=f"El campo {field} no puede estar vacío.",
                details=[{"field": field, "issue": "EMPTY_STRING"}],
            )
