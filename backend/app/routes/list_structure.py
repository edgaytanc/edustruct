from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

list_structure_bp = Blueprint(
    "list",
    __name__,
    url_prefix="/api/list"
)


@list_structure_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="list",
        operation="state"
    )
    return jsonify(response), 200


@list_structure_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="list",
        operation="insert"
    )
    return jsonify(response), 200


@list_structure_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="list",
        operation="delete"
    )
    return jsonify(response), 200


@list_structure_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="list",
        operation="search"
    )
    return jsonify(response), 200


@list_structure_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="list",
        operation="demo-load"
    )
    return jsonify(response), 200


@list_structure_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="list",
        operation="traverse"
    )
    return jsonify(response), 200


@list_structure_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="list",
        operation="reset"
    )
    return jsonify(response), 200
