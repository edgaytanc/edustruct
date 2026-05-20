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


def test_get_advisory_turns_returns_real_dataset_records():
    service = QueueService()

    result = service.get_advisory_turns()

    assert result["count"] == 4
    assert result["sourceDataset"] == "advisory_turns.json"
    assert result["turns"][0]["id"] == "TURN-001"
    assert result["turns"][0]["studentCarnet"] == "2024001"
    assert result["turns"][0]["studentName"] == "Ana López"
    assert result["turns"][0]["reason"] == "Asignación de curso"
    assert result["turns"][0]["isFront"] is True


def test_load_advisory_turns_demo_preserves_fifo_order():
    service = QueueService()

    result = service.load_advisory_turns_demo()

    assert result["size"] == 4
    assert result["queuePolicy"] == "FIFO"
    assert result["sourceDataset"] == "advisory_turns.json"
    assert result["front"].startswith("TURN-001 - 2024001 - Ana López")
    assert result["rear"].startswith("TURN-004 - 2024004 - Luis Ramírez")
    assert result["items"][1].startswith("TURN-002 - 2024002 - Carlos Pérez")
    assert result["advisoryTurns"][1]["reason"] == "Validación de prerrequisitos"


def test_load_demo_uses_real_advisory_dataset():
    service = QueueService()

    result = service.load_demo()

    assert result["size"] == 4
    assert result["context"] == "Cola de turnos de asesoría académica"
    assert result["items"][0].startswith("TURN-001")
