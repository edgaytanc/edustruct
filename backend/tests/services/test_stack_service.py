import pytest

from app.errors.exceptions import StructureEmptyError, ValidationError
from app.services.stack_service import StackService


def test_push_stores_values_lifo_order():
    service = StackService()

    service.push("Dashboard")
    result = service.push("Curso MAT101")

    assert result["items"] == ["Curso MAT101", "Dashboard"]
    assert result["top"] == "Curso MAT101"


def test_pop_removes_top_value():
    service = StackService()
    service.push("A")
    service.push("B")

    result = service.pop()

    assert result["popped"] == "B"
    assert result["items"] == ["A"]


def test_peek_returns_top_without_removing():
    service = StackService()
    service.push("A")

    result = service.peek()

    assert result["peek"] == "A"
    assert result["items"] == ["A"]


def test_pop_empty_stack_raises_structure_empty_error():
    service = StackService()

    with pytest.raises(StructureEmptyError):
        service.pop()


def test_push_without_value_raises_validation_error():
    service = StackService()

    with pytest.raises(ValidationError):
        service.push(None)


def test_search_returns_index_from_top():
    service = StackService()
    service.push("A")
    service.push("B")

    result = service.search("A")

    assert result["found"] is True
    assert result["indexFromTop"] == 1


def test_load_navigation_history_demo_builds_contextual_stack():
    service = StackService()

    result = service.load_navigation_history_demo()

    assert result["size"] == 5
    assert result["navigationPolicy"] == "LIFO"
    assert result["top"] == "Expediente Estudiantil"
    assert result["items"] == [
        "Expediente Estudiantil",
        "Prerrequisitos del curso",
        "Curso CUR-013 - Programación III",
        "Pensum Ingeniería en Sistemas",
        "Dashboard Académico",
    ]


def test_load_demo_uses_navigation_history_context():
    service = StackService()

    result = service.load_demo()

    assert result["size"] == 5
    assert result["context"] == "Historial de navegación académica"
    assert result["top"] == "Expediente Estudiantil"


def test_navigate_to_module_pushes_new_academic_view():
    service = StackService()
    service.navigate_to_module("Dashboard Académico")

    result = service.navigate_to_module("Curso CUR-013")

    assert result["navigatedTo"] == "Curso CUR-013"
    assert result["navigationAction"] == "push"
    assert result["top"] == "Curso CUR-013"
    assert result["items"] == ["Curso CUR-013", "Dashboard Académico"]


def test_navigate_to_module_requires_module_value():
    service = StackService()

    with pytest.raises(ValidationError):
        service.navigate_to_module("")


def test_back_pops_current_module_and_exposes_previous_top():
    service = StackService()
    service.navigate_to_module("Dashboard Académico")
    service.navigate_to_module("Curso CUR-013")

    result = service.back()

    assert result["backFrom"] == "Curso CUR-013"
    assert result["currentModule"] == "Dashboard Académico"
    assert result["items"] == ["Dashboard Académico"]


def test_back_empty_history_raises_structure_empty_error():
    service = StackService()

    with pytest.raises(StructureEmptyError):
        service.back()
