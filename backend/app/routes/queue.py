from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.queue_service import QueueService

queue_bp = Blueprint(
    "queue",
    __name__,
    url_prefix="/api/queue"
)

queue_service = QueueService()


def _payload_value():
    payload = request.get_json(silent=True) or {}
    return payload.get("value")


def _metrics(result):
    return {
        "count": result.get("size", 0),
        "height": None,
        "balanceFactor": None,
        "collisions": None,
        "levels": None,
        "edgesCount": 0
    }


@queue_bp.route("/state", methods=["GET"])
def get_state():
    result = queue_service.state()
    response = success_response(
        message="Estado de la cola obtenido correctamente.",
        structure="queue",
        operation="state",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 200


@queue_bp.route("/insert", methods=["POST"])
def insert():
    result = queue_service.enqueue(_payload_value())
    response = success_response(
        message="Elemento encolado correctamente.",
        structure="queue",
        operation="enqueue",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 201


@queue_bp.route("/delete", methods=["DELETE"])
def delete():
    result = queue_service.dequeue()
    response = success_response(
        message="Elemento desencolado correctamente.",
        structure="queue",
        operation="dequeue",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 200


@queue_bp.route("/search", methods=["GET"])
def search():
    result = queue_service.search(request.args.get("value"))
    response = success_response(
        message="Búsqueda ejecutada correctamente en la cola.",
        structure="queue",
        operation="search",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 200


@queue_bp.route("/front", methods=["GET"])
def front():
    result = queue_service.front()
    response = success_response(
        message="Frente de la cola obtenido correctamente.",
        structure="queue",
        operation="front",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 200


@queue_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = queue_service.load_demo()
    response = success_response(
        message="Dataset demo cargado correctamente en la cola.",
        structure="queue",
        operation="demo-load",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 200


@queue_bp.route("/traverse", methods=["GET"])
def traverse():
    result = queue_service.traverse()
    response = success_response(
        message="Recorrido de cola obtenido correctamente.",
        structure="queue",
        operation="traverse",
        metrics=_metrics(result),
        traversal=result.get("traversal"),
        result=result
    )
    return jsonify(response), 200


@queue_bp.route("/reset", methods=["POST"])
def reset():
    result = queue_service.reset()
    response = success_response(
        message="Cola reiniciada correctamente.",
        structure="queue",
        operation="reset",
        metrics=_metrics(result),
        result=result
    )
    return jsonify(response), 200
