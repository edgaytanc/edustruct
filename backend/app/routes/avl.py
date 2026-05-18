from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.avl_service import AVLService

avl_bp = Blueprint(
    "avl",
    __name__,
    url_prefix="/api/avl"
)

avl_service = AVLService()


def _payload():
    return request.get_json(silent=True) or {}


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


def _metrics(result):
    return result.get("metrics")


def _traversal(result):
    return result.get("traversal")


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


@avl_bp.route("/state", methods=["GET"])
def get_state():
    result = avl_service.state()
    response = success_response(
        message="Estado del árbol AVL obtenido correctamente.",
        structure="avl",
        operation="state",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@avl_bp.route("/insert", methods=["POST"])
def insert():
    payload = _payload()
    result = avl_service.insert(_coerce_value(payload.get("value")))
    response = success_response(
        message="Valor insertado correctamente en el árbol AVL.",
        structure="avl",
        operation="insert",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 201


@avl_bp.route("/delete", methods=["DELETE"])
def delete():
    payload = _payload()
    raw_value = payload.get("value") if "value" in payload else request.args.get("value")
    result = avl_service.delete(_coerce_value(raw_value))
    response = success_response(
        message="Valor eliminado correctamente del árbol AVL.",
        structure="avl",
        operation="delete",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@avl_bp.route("/search", methods=["GET"])
def search():
    result = avl_service.search(_coerce_value(request.args.get("value")))
    response = success_response(
        message="Búsqueda ejecutada correctamente en el árbol AVL.",
        structure="avl",
        operation="search",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@avl_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = avl_service.load_demo()
    response = success_response(
        message="Dataset demo cargado correctamente en el árbol AVL.",
        structure="avl",
        operation="demo-load",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@avl_bp.route("/traverse", methods=["GET"])
def traverse():
    traversal_type = request.args.get("type", "levelorder")
    result = avl_service.traverse(traversal_type)
    response = success_response(
        message="Recorrido del árbol AVL obtenido correctamente.",
        structure="avl",
        operation="traverse",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=_traversal(result),
        result=result,
    )
    return jsonify(response), 200


@avl_bp.route("/metrics", methods=["GET"])
def metrics():
    result = avl_service.metrics()
    response = success_response(
        message="Métricas del árbol AVL obtenidas correctamente.",
        structure="avl",
        operation="metrics",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@avl_bp.route("/reset", methods=["POST"])
def reset():
    result = avl_service.reset()
    response = success_response(
        message="Árbol AVL reiniciado correctamente.",
        structure="avl",
        operation="reset",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200
