import pytest

from app.structures.graph import Graph, GraphNode, GraphSearchResult, GraphTraversalResult


def build_course_graph():
    graph = Graph(directed=True)
    courses = [
        ("CS-101", {"name": "Programación I"}),
        ("CS-201", {"name": "Programación II"}),
        ("CS-301", {"name": "Estructuras de Datos"}),
        ("CS-401", {"name": "Algoritmos"}),
        ("DB-101", {"name": "Bases de Datos I"}),
        ("DB-201", {"name": "Bases de Datos II"}),
        ("AI-401", {"name": "Inteligencia Artificial"}),
    ]
    for course_id, course in courses:
        graph.add_node(course_id, course)

    graph.add_edge("CS-101", "CS-201")
    graph.add_edge("CS-201", "CS-301")
    graph.add_edge("CS-301", "CS-401")
    graph.add_edge("CS-301", "AI-401")
    graph.add_edge("DB-101", "DB-201")
    graph.add_edge("CS-201", "DB-201")
    return graph


def test_empty_graph_uses_directed_adjacency_list_by_default():
    graph = Graph()

    assert graph.directed is True
    assert graph.is_empty() is True
    assert graph.vertices_count == 0
    assert graph.edges_count == 0
    assert graph.connected_components_count() == 0
    assert graph.adjacency_list == {}
    assert graph.last_operation is None


def test_directed_flag_must_be_boolean():
    with pytest.raises(ValueError, match="DIRECTED_MUST_BE_BOOLEAN"):
        Graph(directed="yes")


def test_add_node_stores_id_value_and_empty_neighbors():
    graph = Graph()
    node = graph.add_node(" CS-301 ", {"name": "Estructuras de Datos"})

    assert isinstance(node, GraphNode)
    assert node.id == "CS-301"
    assert node.value["name"] == "Estructuras de Datos"
    assert node.neighbors == []
    assert node.degree() == 0
    assert graph.vertices_count == 1
    assert graph.last_operation["operation"] == "ADD_NODE"


def test_add_node_uses_id_as_default_value():
    graph = Graph()
    node = graph.add_node("CS-101")

    assert node.value == "CS-101"


def test_add_node_rejects_invalid_or_duplicate_ids():
    graph = Graph()

    with pytest.raises(ValueError, match="NODE_ID_REQUIRED"):
        graph.add_node(None)

    with pytest.raises(ValueError, match="NODE_ID_REQUIRED"):
        graph.add_node("   ")

    graph.add_node("CS-101")
    with pytest.raises(ValueError, match="DUPLICATE_NODE"):
        graph.add_node("CS-101")


def test_add_edge_connects_existing_nodes_and_counts_once():
    graph = Graph()
    graph.add_node("CS-201")
    graph.add_node("CS-301")

    edge = graph.add_edge("CS-201", "CS-301")

    assert edge == ("CS-201", "CS-301")
    assert graph.adjacency_list["CS-201"].neighbors == ["CS-301"]
    assert graph.adjacency_list["CS-301"].neighbors == []
    assert graph.edges_count == 1
    assert graph.last_operation["operation"] == "ADD_EDGE"


def test_add_edge_validates_nodes_self_loops_and_duplicates():
    graph = Graph()
    graph.add_node("CS-101")
    graph.add_node("CS-201")

    with pytest.raises(ValueError, match="SELF_LOOPS_NOT_ALLOWED"):
        graph.add_edge("CS-101", "CS-101")

    with pytest.raises(ValueError, match="SOURCE_NODE_NOT_FOUND"):
        graph.add_edge("CS-999", "CS-201")

    with pytest.raises(ValueError, match="TARGET_NODE_NOT_FOUND"):
        graph.add_edge("CS-101", "CS-999")

    graph.add_edge("CS-101", "CS-201")
    with pytest.raises(ValueError, match="DUPLICATE_EDGE"):
        graph.add_edge("CS-101", "CS-201")


def test_undirected_graph_stores_reverse_neighbor_but_counts_logical_edge_once():
    graph = Graph(directed=False)
    graph.add_node("A")
    graph.add_node("B")

    graph.add_edge("A", "B")

    assert graph.adjacency_list["A"].neighbors == ["B"]
    assert graph.adjacency_list["B"].neighbors == ["A"]
    assert graph.edges_count == 1
    assert graph.edges() == [{"source": "A", "target": "B"}]


def test_search_existing_and_missing_course_nodes():
    graph = build_course_graph()

    found = graph.search("CS-301")
    missing = graph.search("MATH-999")

    assert isinstance(found, GraphSearchResult)
    assert found.found is True
    assert found.node.id == "CS-301"
    assert found.comparisons >= 1
    assert missing.found is False
    assert missing.node is None
    assert graph.contains("CS-301") is True
    assert graph.contains("MATH-999") is False


def test_dfs_traversal_is_depth_first_and_includes_animation_steps():
    graph = build_course_graph()

    result = graph.dfs("CS-101")

    assert isinstance(result, GraphTraversalResult)
    assert result.algorithm == "DFS"
    assert result.start_node_id == "CS-101"
    assert result.order == ["CS-101", "CS-201", "CS-301", "CS-401", "AI-401", "DB-201"]
    assert result.steps[0].action == "VISIT"
    assert result.steps[0].node_id == "CS-101"
    assert any(step.action == "DISCOVER" and step.edge == ("CS-201", "CS-301") for step in result.steps)
    assert graph.last_operation["operation"] == "DFS"


def test_bfs_traversal_is_breadth_first_and_differs_from_dfs():
    graph = build_course_graph()

    bfs = graph.bfs("CS-101")
    dfs = graph.dfs("CS-101")

    assert bfs.algorithm == "BFS"
    assert bfs.order == ["CS-101", "CS-201", "CS-301", "DB-201", "CS-401", "AI-401"]
    assert bfs.order != dfs.order
    assert bfs.steps[0].action == "VISIT"
    assert any(step.action == "DISCOVER" and step.edge == ("CS-201", "DB-201") for step in bfs.steps)


def test_traversals_reject_missing_start_node():
    graph = build_course_graph()

    with pytest.raises(ValueError, match="START_NODE_NOT_FOUND"):
        graph.dfs("CS-999")

    with pytest.raises(ValueError, match="START_NODE_NOT_FOUND"):
        graph.bfs("CS-999")


def test_degree_and_in_degree_measure_basic_connectivity():
    graph = build_course_graph()

    assert graph.degree("CS-201") == 2
    assert graph.in_degree("DB-201") == 2
    assert graph.degree("AI-401") == 0

    with pytest.raises(ValueError, match="START_NODE_NOT_FOUND"):
        graph.degree("CS-999")


def test_connected_components_count_uses_weak_connectivity_for_directed_graphs():
    graph = build_course_graph()

    assert graph.connected_components_count() == 1

    graph.add_node("HIST-101", {"name": "Historia"})
    assert graph.connected_components_count() == 2


def test_nodes_edges_and_to_dict_return_json_friendly_state():
    graph = build_course_graph()
    payload = graph.to_dict()

    assert len(graph.nodes()) == graph.vertices_count
    assert len(graph.edges()) == graph.edges_count
    assert payload["directed"] is True
    assert payload["verticesCount"] == 7
    assert payload["edgesCount"] == 6
    assert payload["connectedComponents"] == 1
    assert payload["nodes"][0]["id"] == "CS-101"
    assert payload["nodes"][0]["degree"] == 1
    assert {"source": "CS-201", "target": "DB-201"} in payload["edges"]


def test_result_objects_serialize_to_dict():
    graph = build_course_graph()

    node_payload = graph.search("CS-301").to_dict()
    dfs_payload = graph.dfs("CS-101").to_dict()

    assert node_payload["found"] is True
    assert node_payload["node"]["id"] == "CS-301"
    assert dfs_payload["algorithm"] == "DFS"
    assert dfs_payload["startNodeId"] == "CS-101"
    assert isinstance(dfs_payload["steps"], list)
    assert dfs_payload["steps"][0]["visitedOrder"] == ["CS-101"]
