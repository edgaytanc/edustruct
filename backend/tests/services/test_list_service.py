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
