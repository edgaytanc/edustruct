from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.binary_tree_service import BinaryTreeService

binary_tree_bp = Blueprint(
    "binary-tree",
    __name__,
    url_prefix="/api/binary-tree"
)

binary_tree_service = BinaryTreeService()


def _payload():
    return request.get_json(silent=True) or {}


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


def _metrics(result):
    return result.get("metrics")


def _coerce_value(value):
    if not isinstance(value, str):
        return value

    normalized = value.strip()
    if not normalized:
        return normalized

    try:
        return int(normalized)
    except ValueError:
        return normalized


@binary_tree_bp.route("/state", methods=["GET"])
def get_state():
    result = binary_tree_service.state()
    response = success_response(
        message="Estado del árbol binario obtenido correctamente.",
        structure="binary-tree",
        operation="state",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@binary_tree_bp.route("/insert", methods=["POST"])
def insert():
    payload = _payload()
    result = binary_tree_service.insert(payload.get("value"))
    response = success_response(
        message="Valor insertado correctamente en el árbol binario.",
        structure="binary-tree",
        operation="insert",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 201


@binary_tree_bp.route("/delete", methods=["DELETE"])
def delete():
    payload = _payload()
    value = payload.get("value") if "value" in payload else _coerce_value(request.args.get("value"))
    result = binary_tree_service.delete(value)
    response = success_response(
        message="Valor eliminado correctamente del árbol binario.",
        structure="binary-tree",
        operation="delete",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@binary_tree_bp.route("/search", methods=["GET"])
def search():
    result = binary_tree_service.search(_coerce_value(request.args.get("value")))
    response = success_response(
        message="Búsqueda ejecutada correctamente en el árbol binario.",
        structure="binary-tree",
        operation="search",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@binary_tree_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = binary_tree_service.load_demo()
    response = success_response(
        message="Dataset demo cargado correctamente en el árbol binario.",
        structure="binary-tree",
        operation="demo-load",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@binary_tree_bp.route("/traverse", methods=["GET"])
def traverse():
    traversal_type = request.args.get("type", "levelorder")
    result = binary_tree_service.traverse(traversal_type)
    response = success_response(
        message="Recorrido del árbol binario obtenido correctamente.",
        structure="binary-tree",
        operation="traverse",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=result.get("traversal"),
        result=result,
    )
    return jsonify(response), 200


@binary_tree_bp.route("/metrics", methods=["GET"])
def metrics():
    result = binary_tree_service.metrics()
    response = success_response(
        message="Métricas del árbol binario obtenidas correctamente.",
        structure="binary-tree",
        operation="metrics",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@binary_tree_bp.route("/reset", methods=["POST"])
def reset():
    result = binary_tree_service.reset()
    response = success_response(
        message="Árbol binario reiniciado correctamente.",
        structure="binary-tree",
        operation="reset",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200
