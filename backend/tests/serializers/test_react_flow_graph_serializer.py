from app.serializers.react_flow_serializer import serialize_graph


def _graph_payload():
    return {
        "directed": True,
        "verticesCount": 4,
        "edgesCount": 3,
        "connectedComponents": 1,
        "nodes": [
            {
                "id": "CUR-001",
                "value": {"code": "SIS-101", "name": "Introducción a la Programación"},
                "neighbors": ["CUR-005"],
                "degree": 1,
                "inDegree": 0,
            },
            {
                "id": "CUR-005",
                "value": {"code": "SIS-201", "name": "Programación I"},
                "neighbors": ["CUR-009"],
                "degree": 1,
                "inDegree": 1,
            },
            {
                "id": "CUR-009",
                "value": {"code": "SIS-301", "name": "Programación II"},
                "neighbors": ["CUR-010"],
                "degree": 1,
                "inDegree": 1,
            },
            {
                "id": "CUR-010",
                "value": {"code": "SIS-302", "name": "Estructuras de Datos"},
                "neighbors": [],
                "degree": 0,
                "inDegree": 1,
            },
        ],
        "edges": [
            {"source": "CUR-001", "target": "CUR-005"},
            {"source": "CUR-005", "target": "CUR-009"},
            {"source": "CUR-009", "target": "CUR-010"},
        ],
    }


def test_serialize_graph_creates_course_nodes_and_prerequisite_edges():
    result = serialize_graph(_graph_payload())

    assert len(result["nodes"]) == 4
    assert len(result["edges"]) == 3
    assert result["nodes"][0]["type"] == "graphNode"
    assert result["nodes"][0]["data"]["category"] == "source-course"
    assert result["nodes"][-1]["data"]["category"] == "terminal-course"
    assert result["edges"][0]["data"]["relationship"] == "prerequisite"
    assert result["edges"][0]["label"] == "habilita"


def test_serialize_graph_includes_degree_and_neighbor_metadata():
    result = serialize_graph(_graph_payload())
    node = result["nodes"][1]

    assert node["data"]["metadata"]["degree"] == 1
    assert node["data"]["metadata"]["outDegree"] == 1
    assert node["data"]["metadata"]["inDegree"] == 1
    assert node["data"]["metadata"]["neighbors"] == ["CUR-009"]
    assert node["data"]["metadata"]["structure"] == "graph"


def test_serialize_graph_highlights_traversal_nodes_and_edges():
    traversal = {
        "algorithm": "DFS",
        "startNodeId": "CUR-001",
        "order": ["CUR-001", "CUR-005", "CUR-009"],
        "steps": [
            {"step": 0, "action": "VISIT", "nodeId": "CUR-001", "edge": None},
            {"step": 1, "action": "DISCOVER", "nodeId": "CUR-005", "edge": {"source": "CUR-001", "target": "CUR-005"}},
        ],
    }

    result = serialize_graph(_graph_payload(), traversal=traversal)

    visited_nodes = [node for node in result["nodes"] if node["data"]["category"] == "visited"]
    assert len(visited_nodes) == 3
    assert visited_nodes[0]["data"]["metadata"]["visitOrder"] == 0
    assert result["edges"][0]["animated"] is True
    assert result["edges"][0]["data"]["isTraversalEdge"] is True


def test_serialize_graph_highlights_search_match():
    search = {"found": True, "nodeId": "CUR-010"}

    result = serialize_graph(_graph_payload(), search=search)

    matches = [node for node in result["nodes"] if node["data"]["category"] == "search-match"]
    assert len(matches) == 1
    assert matches[0]["id"] == "CUR-010"
    assert matches[0]["data"]["metadata"]["searchMatch"] is True


def test_serialize_graph_returns_empty_contract_for_empty_graph():
    result = serialize_graph({"nodes": [], "edges": []})

    assert result == {"nodes": [], "edges": []}
