import pytest

from app.errors.exceptions import NotFoundError, ValidationError
from app.services.list_service import ListService


def test_insert_appends_values_by_default():
    service = ListService()

    result = service.insert("MAT101")
    service.insert("PROGIII")

    assert result["inserted"] == "MAT101"
    assert service.state()["items"] == ["MAT101", "PROGIII"]
    assert service.state()["size"] == 2


def test_insert_can_prepend_values():
    service = ListService()

    service.insert("B", position="tail")
    service.insert("A", position="head")

    assert service.state()["items"] == ["A", "B"]
    assert service.state()["head"] == "A"
    assert service.state()["tail"] == "B"


def test_delete_removes_existing_value():
    service = ListService()
    service.insert("A")
    service.insert("B")

    result = service.delete("A")

    assert result["deleted"] == "A"
    assert result["items"] == ["B"]


def test_delete_unknown_value_raises_not_found():
    service = ListService()
    service.insert("A")

    with pytest.raises(NotFoundError):
        service.delete("Z")


def test_search_returns_found_metadata():
    service = ListService()
    service.insert("A")
    service.insert("B")

    result = service.search("B")

    assert result["found"] is True
    assert result["index"] == 1


def test_insert_without_value_raises_validation_error():
    service = ListService()

    with pytest.raises(ValidationError):
        service.insert(None)


def test_reset_clears_list():
    service = ListService()
    service.insert("A")

    result = service.reset()

    assert result["reset"] is True
    assert result["items"] == []


def test_get_available_courses_returns_enrollment_courses():
    service = ListService()

    result = service.get_available_courses()

    assert result["size"] >= 2
    assert result["courses"][0]["courseId"] == "CUR-013"
    assert result["courses"][0]["enrolledCount"] == 3
    assert result["courses"][0]["label"] == "SIS-304 - Programación III"


def test_load_course_enrollments_uses_real_dataset_students():
    service = ListService()

    result = service.load_course_enrollments("CUR-013")

    assert result["courseId"] == "CUR-013"
    assert result["course"]["label"] == "SIS-304 - Programación III"
    assert result["items"] == [
        "2024001 - Ana López",
        "2024002 - Carlos Pérez",
        "2024003 - María García",
    ]
    assert result["head"] == "2024001 - Ana López"
    assert result["tail"] == "2024003 - María García"
    assert result["students"][0]["email"] == "ana.lopez@edustruct.edu"


def test_load_demo_uses_default_real_course_dataset():
    service = ListService()

    result = service.load_demo()

    assert result["courseId"] == "CUR-013"
    assert result["items"][0] == "2024001 - Ana López"
    assert result["context"] == "Lista enlazada de estudiantes inscritos por curso"


def test_load_unknown_course_raises_not_found():
    service = ListService()

    with pytest.raises(NotFoundError):
        service.load_course_enrollments("CUR-999")


def test_load_course_without_course_id_raises_validation_error():
    service = ListService()

    with pytest.raises(ValidationError):
        service.load_course_enrollments(None)
