import pytest

from app.errors.exceptions import StructureEmptyError, ValidationError
from app.services.queue_service import QueueService


def test_enqueue_stores_values_fifo_order():
    service = QueueService()

    service.enqueue("Turno 1")
    result = service.enqueue("Turno 2")

    assert result["items"] == ["Turno 1", "Turno 2"]
    assert result["front"] == "Turno 1"
    assert result["rear"] == "Turno 2"


def test_dequeue_removes_front_value():
    service = QueueService()
    service.enqueue("A")
    service.enqueue("B")

    result = service.dequeue()

    assert result["dequeued"] == "A"
    assert result["items"] == ["B"]


def test_front_returns_value_without_removing():
    service = QueueService()
    service.enqueue("A")

    result = service.front()

    assert result["front"] == "A"
    assert result["items"] == ["A"]


def test_dequeue_empty_queue_raises_structure_empty_error():
    service = QueueService()

    with pytest.raises(StructureEmptyError):
        service.dequeue()


def test_enqueue_without_value_raises_validation_error():
    service = QueueService()

    with pytest.raises(ValidationError):
        service.enqueue(None)


def test_search_returns_index_from_front():
    service = QueueService()
    service.enqueue("A")
    service.enqueue("B")

    result = service.search("B")

    assert result["found"] is True
    assert result["indexFromFront"] == 1
