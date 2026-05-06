from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

hash_table_bp = Blueprint(
    "hash",
    __name__,
    url_prefix="/api/hash"
)


@hash_table_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="hash",
        operation="state"
    )
    return jsonify(response), 200


@hash_table_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="hash",
        operation="insert"
    )
    return jsonify(response), 200


@hash_table_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="hash",
        operation="delete"
    )
    return jsonify(response), 200


@hash_table_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="hash",
        operation="search"
    )
    return jsonify(response), 200


@hash_table_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="hash",
        operation="demo-load"
    )
    return jsonify(response), 200


@hash_table_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="hash",
        operation="traverse"
    )
    return jsonify(response), 200


@hash_table_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="hash",
        operation="reset"
    )
    return jsonify(response), 200
