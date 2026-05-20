"""
Dataset loading helpers for EduStruct.

This module centralizes read-only access to the JSON demo datasets used by
services. It stays independent from Flask, routes, serializers, and HTTP code.

The loader is intentionally defensive because the project can run from:
- backend root during pytest: /app or /project/backend
- repository root during local execution
- Docker containers with datasets mounted at /datasets
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.errors.exceptions import DatasetError


def _candidate_dataset_dirs() -> list[Path]:
    """
    Return possible dataset directories ordered from most explicit to fallback.

    __file__ is usually:
    backend/app/utils/dataset_loader.py

    parents:
    - parents[0] = backend/app/utils
    - parents[1] = backend/app
    - parents[2] = backend
    - parents[3] = repository root, when running from the monorepo
    """
    current_file = Path(__file__).resolve()
    backend_dir = current_file.parents[2]
    repository_root = backend_dir.parent

    return [
        Path("/datasets"),
        repository_root / "datasets",
        backend_dir / "datasets",
        Path.cwd() / "datasets",
        Path.cwd().parent / "datasets",
    ]


def get_datasets_dir() -> Path:
    """Return the first existing datasets directory."""
    for candidate in _candidate_dataset_dirs():
        if candidate.exists() and candidate.is_dir():
            return candidate

    searched = [str(path) for path in _candidate_dataset_dirs()]
    raise DatasetError(
        message="No se encontró la carpeta datasets del proyecto.",
        details=[{"issue": "DATASETS_DIR_NOT_FOUND", "searched": searched}],
    )


def dataset_path(filename: str) -> Path:
    """Return the absolute path for a dataset filename."""
    clean_filename = str(filename).strip()
    if not clean_filename:
        raise DatasetError(
            message="El nombre del archivo de dataset es obligatorio.",
            details=[{"field": "filename", "issue": "REQUIRED"}],
        )

    return get_datasets_dir() / clean_filename


def load_json_dataset(filename: str) -> list[dict[str, Any]]:
    """Load a JSON dataset file from the project datasets directory."""
    path = dataset_path(filename)

    if not path.exists():
        raise DatasetError(
            message="El archivo de dataset solicitado no existe.",
            details=[
                {
                    "dataset": filename,
                    "path": str(path),
                    "issue": "FILE_NOT_FOUND",
                }
            ],
        )

    try:
        raw_content = path.read_text(encoding="utf-8")
        data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise DatasetError(
            message="El archivo de dataset no contiene JSON válido.",
            details=[
                {
                    "dataset": filename,
                    "path": str(path),
                    "issue": "INVALID_JSON",
                    "error": str(exc),
                }
            ],
        ) from exc

    if not isinstance(data, list):
        raise DatasetError(
            message="El dataset debe contener una lista de registros.",
            details=[
                {
                    "dataset": filename,
                    "path": str(path),
                    "issue": "INVALID_ROOT_TYPE",
                }
            ],
        )

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise DatasetError(
                message="Todos los registros del dataset deben ser objetos JSON.",
                details=[
                    {
                        "dataset": filename,
                        "path": str(path),
                        "index": index,
                        "issue": "INVALID_RECORD_TYPE",
                    }
                ],
            )

    return data


def load_students() -> list[dict[str, Any]]:
    """Load students.json."""
    return load_json_dataset("students.json")


def load_enrollments() -> list[dict[str, Any]]:
    """Load enrollments.json."""
    return load_json_dataset("enrollments.json")


def load_courses() -> list[dict[str, Any]]:
    """Load courses.json."""
    return load_json_dataset("courses.json")


def load_advisory_turns() -> list[dict[str, Any]]:
    """Load advisory_turns.json."""
    return load_json_dataset("advisory_turns.json")


def load_students_by_carnet() -> dict[str, dict[str, Any]]:
    """Return students indexed by carnet."""
    students = load_students()
    students_by_carnet: dict[str, dict[str, Any]] = {}

    for student in students:
        carnet = student.get("carnet")
        if carnet is None or not str(carnet).strip():
            raise DatasetError(
                message="El dataset de estudiantes contiene un registro sin carnet.",
                details=[{"dataset": "students.json", "issue": "MISSING_CARNET"}],
            )

        students_by_carnet[str(carnet)] = student

    return students_by_carnet


def load_courses_by_id() -> dict[str, dict[str, Any]]:
    """Return courses indexed by id."""
    courses = load_courses()
    courses_by_id: dict[str, dict[str, Any]] = {}

    for course in courses:
        course_id = course.get("id") or course.get("course_id")
        if course_id is None or not str(course_id).strip():
            raise DatasetError(
                message="El dataset de cursos contiene un registro sin id.",
                details=[{"dataset": "courses.json", "issue": "MISSING_COURSE_ID"}],
            )

        courses_by_id[str(course_id)] = course

    return courses_by_id


def find_enrollment_by_course_id(course_id: str) -> dict[str, Any] | None:
    """Return the enrollment record matching a course id, or None."""
    normalized_course_id = str(course_id).strip()

    for enrollment in load_enrollments():
        if str(enrollment.get("course_id", "")).strip() == normalized_course_id:
            return enrollment

    return None
