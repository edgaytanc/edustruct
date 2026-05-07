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
