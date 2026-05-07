from flask import Blueprint, jsonify, request

from app.serializers.metrics_serializer import create_metrics
from app.serializers.response_serializer import success_response
from app.services.stack_service import StackService

stack_bp = Blueprint(
    "stack",
    __name__,
    url_prefix="/api/stack"
)

stack_service = StackService()


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


@stack_bp.route("/state", methods=["GET"])
def get_state():
    result = stack_service.state()
    response = success_response(
        message="Estado de la pila obtenido correctamente.",
        structure="stack",
        operation="state",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@stack_bp.route("/insert", methods=["POST"])
def insert():
    result = stack_service.push(_payload_value())
    response = success_response(
        message="Elemento apilado correctamente.",
        structure="stack",
        operation="push",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 201


@stack_bp.route("/delete", methods=["DELETE"])
def delete():
    result = stack_service.pop()
    response = success_response(
        message="Elemento desapilado correctamente.",
        structure="stack",
        operation="pop",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@stack_bp.route("/search", methods=["GET"])
def search():
    result = stack_service.search(request.args.get("value"))
    response = success_response(
        message="Búsqueda ejecutada correctamente en la pila.",
        structure="stack",
        operation="search",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@stack_bp.route("/peek", methods=["GET"])
def peek():
    result = stack_service.peek()
    response = success_response(
        message="Tope de la pila obtenido correctamente.",
        structure="stack",
        operation="peek",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@stack_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = stack_service.load_demo()
    response = success_response(
        message="Dataset demo cargado correctamente en la pila.",
        structure="stack",
        operation="demo-load",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200


@stack_bp.route("/traverse", methods=["GET"])
def traverse():
    result = stack_service.traverse()
    response = success_response(
        message="Recorrido de pila obtenido correctamente.",
        structure="stack",
        operation="traverse",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=result.get("traversal"),
        result=result,
    )
    return jsonify(response), 200


@stack_bp.route("/reset", methods=["POST"])
def reset():
    result = stack_service.reset()
    response = success_response(
        message="Pila reiniciada correctamente.",
        structure="stack",
        operation="reset",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), 200
