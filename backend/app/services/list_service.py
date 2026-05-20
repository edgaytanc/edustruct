"""
Application service for the linked-list structure.

This module coordinates use cases for the REST layer while keeping the pure
LinkedList implementation independent from Flask and HTTP concerns.
"""

from __future__ import annotations

from typing import Any

from app.errors.exceptions import DatasetError, NotFoundError, ValidationError
from app.serializers.react_flow_serializer import serialize_linked_list
from app.structures.list_model import LinkedList
from app.utils.dataset_loader import (
    load_courses_by_id,
    load_enrollments,
    load_students_by_carnet,
)


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
        items = self._list.to_list()
        result = self._build_result()
        result["traversal"] = {
            "type": "linear",
            "start": "head",
            "order": items,
            "steps": [
                {"index": index, "value": value}
                for index, value in enumerate(items)
            ],
        }
        return result

    def get_available_courses(self) -> dict[str, Any]:
        """Return courses that have enrollment records available for the demo."""
        enrollments = load_enrollments()
        courses_by_id = load_courses_by_id()
        courses: list[dict[str, Any]] = []

        for enrollment in enrollments:
            course_id = str(enrollment["course_id"])
            course = courses_by_id.get(course_id, {})
            students = enrollment.get("students", [])
            courses.append(
                {
                    "courseId": course_id,
                    "code": course.get("code"),
                    "name": course.get("name"),
                    "label": self._course_label(course_id=course_id, course=course),
                    "studentsCount": len(students),
                    "enrolledCount": len(students),
                }
            )

        courses_count = len(courses)
        return {
            "courses": courses,
            "count": courses_count,
            "size": courses_count,
            "context": "Cursos con estudiantes inscritos disponibles para lista enlazada",
        }

    def load_course_enrollments(self, course_id: Any) -> dict[str, Any]:
        """Load a linked list using real students enrolled in a course."""
        self._validate_course_id(course_id)
        normalized_course_id = str(course_id).strip()

        enrollment = self._find_enrollment(normalized_course_id)
        students_by_carnet = load_students_by_carnet()
        courses_by_id = load_courses_by_id()
        course = courses_by_id.get(normalized_course_id, {})

        self._list.clear()
        loaded_students: list[dict[str, Any]] = []
        loaded_values: list[str] = []

        for carnet in enrollment.get("students", []):
            student = students_by_carnet.get(str(carnet))
            if student is None:
                raise DatasetError(
                    message="La inscripción referencia un estudiante inexistente.",
                    details=[
                        {
                            "dataset": "enrollments.json",
                            "courseId": normalized_course_id,
                            "studentCarnet": str(carnet),
                            "issue": "STUDENT_NOT_FOUND",
                        }
                    ],
                )

            display_value = self._student_display_value(student)
            self._list.append(display_value)
            loaded_values.append(display_value)
            loaded_students.append(
                {
                    "carnet": str(student.get("carnet")),
                    "name": student.get("name"),
                    "email": student.get("email"),
                    "status": student.get("status"),
                    "careerId": student.get("career_id"),
                    "displayValue": display_value,
                }
            )

        result = self._build_result()
        result["loaded"] = loaded_values
        result["students"] = loaded_students
        result["courseId"] = normalized_course_id
        result["course"] = {
            "id": normalized_course_id,
            "code": course.get("code"),
            "name": course.get("name"),
            "label": self._course_label(course_id=normalized_course_id, course=course),
        }
        result["context"] = "Lista enlazada de estudiantes inscritos por curso"
        return result

    def load_demo(self) -> dict[str, Any]:
        """Load the default educational demo list of enrolled students."""
        return self.load_course_enrollments("CUR-013")

    def reset(self) -> dict[str, Any]:
        """Clear the linked list."""
        self._list.clear()
        result = self._build_result()
        result["reset"] = True
        return result

    def _build_result(self) -> dict[str, Any]:
        items = self._list.to_list()
        visualization = serialize_linked_list(items)
        return {
            "items": items,
            "size": self._list.size(),
            "head": items[0] if items else None,
            "tail": items[-1] if items else None,
            "isEmpty": self._list.is_empty(),
            "nodes": visualization["nodes"],
            "edges": visualization["edges"],
        }

    def _find_enrollment(self, course_id: str) -> dict[str, Any]:
        enrollments = load_enrollments()
        for enrollment in enrollments:
            if str(enrollment.get("course_id")) == course_id:
                return enrollment

        raise NotFoundError(
            message="No existen inscripciones para el curso solicitado.",
            details=[{"field": "courseId", "value": course_id, "issue": "COURSE_NOT_FOUND"}],
        )

    @staticmethod
    def _student_display_value(student: dict[str, Any]) -> str:
        carnet = str(student.get("carnet", "")).strip()
        name = str(student.get("name", "")).strip()
        if not carnet or not name:
            raise DatasetError(
                message="El dataset de estudiantes contiene registros incompletos.",
                details=[{"dataset": "students.json", "issue": "MISSING_STUDENT_DISPLAY_FIELDS"}],
            )
        return f"{carnet} - {name}"

    @staticmethod
    def _course_label(course_id: str, course: dict[str, Any]) -> str:
        code = course.get("code")
        name = course.get("name")
        if code and name:
            return f"{code} - {name}"
        return course_id

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
    def _validate_course_id(course_id: Any) -> None:
        if course_id is None:
            raise ValidationError(
                message="El campo courseId es obligatorio.",
                details=[{"field": "courseId", "issue": "REQUIRED"}],
            )

        if isinstance(course_id, str) and not course_id.strip():
            raise ValidationError(
                message="El campo courseId no puede estar vacío.",
                details=[{"field": "courseId", "issue": "EMPTY_STRING"}],
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
