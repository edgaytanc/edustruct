from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

queue_bp = Blueprint(
    "queue",
    __name__,
    url_prefix="/api/queue"
)


@queue_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="queue",
        operation="state"
    )
    return jsonify(response), 200


@queue_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="queue",
        operation="insert"
    )
    return jsonify(response), 200


@queue_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="queue",
        operation="delete"
    )
    return jsonify(response), 200


@queue_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="queue",
        operation="search"
    )
    return jsonify(response), 200


@queue_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="queue",
        operation="demo-load"
    )
    return jsonify(response), 200


@queue_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="queue",
        operation="traverse"
    )
    return jsonify(response), 200


@queue_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="queue",
        operation="reset"
    )
    return jsonify(response), 200
