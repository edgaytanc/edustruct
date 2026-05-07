from flask import Blueprint, jsonify, request

from app.serializers.metrics_serializer import create_metrics
from app.serializers.response_serializer import success_response
from app.services.list_service import ListService

list_structure_bp = Blueprint(
    "list",
    __name__,
    url_prefix="/api/list"
)

list_service = ListService()


def _payload_value():
    payload = request.get_json(silent=True) or {}
    return payload.get("value")


def _metrics(result):
    return create_metrics(
        count=result.get("size", 0),
        edges_count=len(result.get("edges", [])),
    )


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


@list_structure_bp.route("/state", methods=["GET"])
def get_state():
    result = list_service.state()
    response = success_response(
        message="Estado de la lista obtenido correctamente.",
        structure="list",
        operation="state",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@list_structure_bp.route("/insert", methods=["POST"])
def insert():
    payload = request.get_json(silent=True) or {}
    result = list_service.insert(
        value=payload.get("value"),
        position=payload.get("position", "tail")
    )
    response = success_response(
        message="Elemento insertado correctamente en la lista.",
        structure="list",
        operation="insert",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 201


@list_structure_bp.route("/delete", methods=["DELETE"])
def delete():
    result = list_service.delete(_payload_value())
    response = success_response(
        message="Elemento eliminado correctamente de la lista.",
        structure="list",
        operation="delete",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@list_structure_bp.route("/search", methods=["GET"])
def search():
    result = list_service.search(request.args.get("value"))
    response = success_response(
        message="Búsqueda ejecutada correctamente en la lista.",
        structure="list",
        operation="search",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@list_structure_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = list_service.load_demo()
    response = success_response(
        message="Dataset demo cargado correctamente en la lista.",
        structure="list",
        operation="demo-load",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@list_structure_bp.route("/traverse", methods=["GET"])
def traverse():
    result = list_service.traverse()
    response = success_response(
        message="Recorrido lineal obtenido correctamente.",
        structure="list",
        operation="traverse",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=result.get("traversal"),
        result=result,
    )
    return jsonify(response), 200


@list_structure_bp.route("/reset", methods=["POST"])
def reset():
    result = list_service.reset()
    response = success_response(
        message="Lista reiniciada correctamente.",
        structure="list",
        operation="reset",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200
