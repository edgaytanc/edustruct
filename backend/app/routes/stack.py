from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

stack_bp = Blueprint(
    "stack",
    __name__,
    url_prefix="/api/stack"
)


@stack_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="stack",
        operation="state"
    )
    return jsonify(response), 200


@stack_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="stack",
        operation="insert"
    )
    return jsonify(response), 200


@stack_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="stack",
        operation="delete"
    )
    return jsonify(response), 200


@stack_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="stack",
        operation="search"
    )
    return jsonify(response), 200


@stack_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="stack",
        operation="demo-load"
    )
    return jsonify(response), 200


@stack_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="stack",
        operation="traverse"
    )
    return jsonify(response), 200


@stack_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="stack",
        operation="reset"
    )
    return jsonify(response), 200
