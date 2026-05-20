from app.services.list_service import ListService
from app.services.queue_service import QueueService
from app.services.stack_service import StackService


def test_list_service_returns_react_flow_visualization():
    service = ListService()
    result = service.insert("MAT101")

    assert result["items"] == ["MAT101"]
    assert len(result["nodes"]) == 3
    assert len(result["edges"]) == 2
    assert result["nodes"][0]["data"]["category"] == "head"
    assert result["nodes"][-1]["data"]["category"] == "tail"


def test_stack_service_returns_react_flow_visualization():
    service = StackService()
    service.push("Dashboard")
    result = service.push("Pensum")

    assert result["items"] == ["Pensum", "Dashboard"]
    assert result["nodes"][0]["data"]["label"] == "TOP"
    assert result["nodes"][1]["data"]["metadata"]["isTop"] is True
    assert len(result["edges"]) == 2


def test_queue_service_returns_react_flow_visualization():
    service = QueueService()
    service.enqueue("Turno 1")
    result = service.enqueue("Turno 2")

    assert result["items"] == ["Turno 1", "Turno 2"]
    assert result["nodes"][0]["data"]["label"] == "FRONT"
    assert result["nodes"][-1]["data"]["label"] == "REAR"
    assert len(result["edges"]) == 3


def test_queue_advisory_demo_returns_react_flow_visualization():
    service = QueueService()

    result = service.load_advisory_turns_demo()

    assert result["size"] == 4
    assert result["nodes"][0]["data"]["label"] == "FRONT"
    assert result["nodes"][1]["data"]["label"].startswith("TURN-001")
    assert result["nodes"][1]["data"]["metadata"]["isFront"] is True
    assert result["nodes"][-1]["data"]["label"] == "REAR"
    assert len(result["edges"]) == 5


def test_stack_navigation_history_demo_returns_react_flow_visualization():
    service = StackService()

    result = service.load_navigation_history_demo()

    assert result["size"] == 5
    assert result["nodes"][0]["data"]["label"] == "TOP"
    assert result["nodes"][1]["data"]["label"] == "Expediente Estudiantil"
    assert result["nodes"][1]["data"]["metadata"]["isTop"] is True
    assert len(result["edges"]) == 5
