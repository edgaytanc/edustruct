"""REST routes for the EduStruct course prerequisite graph module."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.graph_service import GraphService

graph_bp = Blueprint(
    "graph",
    __name__,
    url_prefix="/api/graph"
)

graph_service = GraphService()


def _payload():
    """Return a safe JSON payload for POST requests."""
    return request.get_json(silent=True) or {}


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


def _metrics(result):
    return result.get("metrics")


def _traversal(result):
    return result.get("traversal")


def _build_success(message, operation, result, status=200, traversal=None):
    """Build a standard EduStruct API response for graph operations."""
    response = success_response(
        message=message,
        structure="graph",
        operation=operation,
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=traversal if traversal is not None else _traversal(result),
        result=result,
    )
    return jsonify(response), status


def _first_present(payload, *keys):
    """Return the first present key from a payload, preserving falsy values."""
    for key in keys:
        if key in payload:
            return payload.get(key)
    return None


@graph_bp.route("/state", methods=["GET"])
def get_state():
    """Return the current graph state and React Flow visualization contract."""
    result = graph_service.state()
    return _build_success(
        message="Estado del grafo de prerrequisitos obtenido correctamente.",
        operation="state",
        result=result,
    )


@graph_bp.route("/nodes", methods=["POST"])
@graph_bp.route("/add-node", methods=["POST"])
def add_node():
    """Add a course node to the prerequisite graph."""
    payload = _payload()
    node_id = _first_present(payload, "id", "nodeId", "courseId")
    value = _first_present(payload, "value", "course")
    result = graph_service.add_node(node_id, value)
    return _build_success(
        message="Nodo de curso agregado correctamente al grafo.",
        operation="add-node",
        result=result,
        status=201,
    )


@graph_bp.route("/edges", methods=["POST"])
@graph_bp.route("/add-edge", methods=["POST"])
def add_edge():
    """Add a directed prerequisite edge: prerequisite -> course."""
    payload = _payload()
    source_id = _first_present(payload, "source", "sourceId", "prerequisiteId", "prerequisite_id")
    target_id = _first_present(payload, "target", "targetId", "courseId", "course_id")
    result = graph_service.add_edge(source_id, target_id)
    return _build_success(
        message="Arista de prerrequisito agregada correctamente al grafo.",
        operation="add-edge",
        result=result,
        status=201,
    )


@graph_bp.route("/insert", methods=["POST"])
def insert():
    """Compatibility endpoint for inserting nodes or edges from a generic UI action."""
    payload = _payload()

    if any(key in payload for key in ("source", "sourceId", "prerequisiteId", "prerequisite_id")):
        source_id = _first_present(payload, "source", "sourceId", "prerequisiteId", "prerequisite_id")
        target_id = _first_present(payload, "target", "targetId", "courseId", "course_id")
        result = graph_service.add_edge(source_id, target_id)
        return _build_success(
            message="Arista de prerrequisito insertada correctamente en el grafo.",
            operation="add-edge",
            result=result,
            status=201,
        )

    node_id = _first_present(payload, "id", "nodeId", "courseId")
    value = _first_present(payload, "value", "course")
    result = graph_service.add_node(node_id, value)
    return _build_success(
        message="Nodo de curso insertado correctamente en el grafo.",
        operation="add-node",
        result=result,
        status=201,
    )


@graph_bp.route("/search", methods=["GET"])
def search():
    """Search a course node by id."""
    node_id = request.args.get("id") or request.args.get("nodeId") or request.args.get("courseId")
    result = graph_service.search(node_id)
    return _build_success(
        message="Búsqueda ejecutada correctamente en el grafo.",
        operation="search",
        result=result,
    )


@graph_bp.route("/demo/load", methods=["POST"])
def load_demo():
    """Load the prerequisite graph from the project demo datasets."""
    result = graph_service.load_demo()
    return _build_success(
        message="Dataset demo cargado correctamente en el grafo de prerrequisitos.",
        operation="demo-load",
        result=result,
    )


@graph_bp.route("/traverse", methods=["GET"])
def traverse():
    """Execute DFS or BFS from the selected start node."""
    algorithm = request.args.get("algorithm") or request.args.get("type")
    start_node_id = request.args.get("start") or request.args.get("startNodeId") or request.args.get("courseId")
    result = graph_service.traverse(algorithm, start_node_id)
    return _build_success(
        message="Recorrido del grafo obtenido correctamente.",
        operation="traverse",
        result=result,
        traversal=_traversal(result),
    )


@graph_bp.route("/dfs", methods=["GET"])
def dfs():
    """Execute DFS from the selected start node."""
    start_node_id = request.args.get("start") or request.args.get("startNodeId") or request.args.get("courseId")
    result = graph_service.dfs(start_node_id)
    return _build_success(
        message="Recorrido DFS del grafo obtenido correctamente.",
        operation="dfs",
        result=result,
        traversal=_traversal(result),
    )


@graph_bp.route("/bfs", methods=["GET"])
def bfs():
    """Execute BFS from the selected start node."""
    start_node_id = request.args.get("start") or request.args.get("startNodeId") or request.args.get("courseId")
    result = graph_service.bfs(start_node_id)
    return _build_success(
        message="Recorrido BFS del grafo obtenido correctamente.",
        operation="bfs",
        result=result,
        traversal=_traversal(result),
    )


@graph_bp.route("/metrics", methods=["GET"])
def metrics():
    """Return graph connectivity and degree metrics."""
    result = graph_service.metrics()
    return _build_success(
        message="Métricas del grafo obtenidas correctamente.",
        operation="metrics",
        result=result,
    )


@graph_bp.route("/reset", methods=["POST"])
def reset():
    """Clear the current graph state."""
    result = graph_service.reset()
    return _build_success(
        message="Grafo de prerrequisitos reiniciado correctamente.",
        operation="reset",
        result=result,
    )
