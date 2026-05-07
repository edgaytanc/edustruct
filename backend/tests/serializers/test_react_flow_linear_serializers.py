from app.serializers.react_flow_serializer import (
    serialize_linked_list,
    serialize_queue,
    serialize_stack,
)


def test_serialize_linked_list_adds_head_tail_markers_and_edges():
    visualization = serialize_linked_list(["A", "B"])

    assert len(visualization["nodes"]) == 4
    assert len(visualization["edges"]) == 3
    assert visualization["nodes"][0]["data"]["label"] == "HEAD"
    assert visualization["nodes"][-1]["data"]["label"] == "TAIL"
    assert visualization["nodes"][1]["data"]["metadata"]["isHead"] is True
    assert visualization["nodes"][2]["data"]["metadata"]["isTail"] is True
    assert visualization["edges"][0]["animated"] is True


def test_serialize_empty_linked_list_keeps_visual_markers():
    visualization = serialize_linked_list([])

    assert [node["data"]["label"] for node in visualization["nodes"]] == ["HEAD", "TAIL"]
    assert len(visualization["edges"]) == 1


def test_serialize_queue_adds_front_rear_markers():
    visualization = serialize_queue(["Turno 1", "Turno 2"])

    assert len(visualization["nodes"]) == 4
    assert visualization["nodes"][0]["data"]["label"] == "FRONT"
    assert visualization["nodes"][-1]["data"]["label"] == "REAR"
    assert visualization["nodes"][1]["data"]["metadata"]["indexFromFront"] == 0
    assert visualization["nodes"][2]["data"]["metadata"]["isRear"] is True


def test_serialize_stack_uses_vertical_layout_from_top():
    visualization = serialize_stack(["Curso", "Pensum"])

    assert len(visualization["nodes"]) == 3
    assert len(visualization["edges"]) == 2
    assert visualization["nodes"][0]["data"]["label"] == "TOP"
    assert visualization["nodes"][1]["position"]["y"] < visualization["nodes"][2]["position"]["y"]
    assert visualization["edges"][0]["type"] == "straight"
    assert visualization["edges"][0]["data"]["relationship"] == "below"
