from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.tree_service import TreeService

tree_bp = Blueprint(
    "tree",
    __name__,
    url_prefix="/api/tree"
)

tree_service = TreeService()


def _payload():
    return request.get_json(silent=True) or {}


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


def _metrics(result):
    return result.get("metrics")


@tree_bp.route("/state", methods=["GET"])
def get_state():
    result = tree_service.state()
    response = success_response(
        message="Estado del árbol general obtenido correctamente.",
        structure="tree",
        operation="state",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@tree_bp.route("/insert", methods=["POST"])
def insert():
    payload = _payload()
    result = tree_service.insert(
        node_id=payload.get("id"),
        label=payload.get("label"),
        parent_id=payload.get("parentId"),
        category=payload.get("category", "academic"),
        metadata=payload.get("metadata") or {},
    )
    response = success_response(
        message="Nodo insertado correctamente en el árbol general.",
        structure="tree",
        operation="insert",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 201


@tree_bp.route("/delete", methods=["DELETE"])
def delete():
    payload = _payload()
    node_id = payload.get("id") or request.args.get("id")
    result = tree_service.delete(node_id)
    response = success_response(
        message="Nodo eliminado correctamente del árbol general.",
        structure="tree",
        operation="delete",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@tree_bp.route("/search", methods=["GET"])
def search():
    result = tree_service.search(request.args.get("id"))
    response = success_response(
        message="Búsqueda ejecutada correctamente en el árbol general.",
        structure="tree",
        operation="search",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@tree_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = tree_service.load_demo()
    response = success_response(
        message="Dataset demo cargado correctamente en el árbol general.",
        structure="tree",
        operation="demo-load",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@tree_bp.route("/traverse", methods=["GET"])
def traverse():
    traversal_type = request.args.get("type", "levelorder")
    result = tree_service.traverse(traversal_type)
    response = success_response(
        message="Recorrido del árbol general obtenido correctamente.",
        structure="tree",
        operation="traverse",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=result.get("traversal"),
        result=result,
    )
    return jsonify(response), 200


@tree_bp.route("/metrics", methods=["GET"])
def metrics():
    result = tree_service.metrics()
    response = success_response(
        message="Métricas del árbol general obtenidas correctamente.",
        structure="tree",
        operation="metrics",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@tree_bp.route("/reset", methods=["POST"])
def reset():
    result = tree_service.reset()
    response = success_response(
        message="Árbol general reiniciado correctamente.",
        structure="tree",
        operation="reset",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200
