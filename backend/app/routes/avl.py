from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

avl_bp = Blueprint(
    "avl",
    __name__,
    url_prefix="/api/avl"
)


@avl_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="avl",
        operation="state"
    )
    return jsonify(response), 200


@avl_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="avl",
        operation="insert"
    )
    return jsonify(response), 200


@avl_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="avl",
        operation="delete"
    )
    return jsonify(response), 200


@avl_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="avl",
        operation="search"
    )
    return jsonify(response), 200


@avl_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="avl",
        operation="demo-load"
    )
    return jsonify(response), 200


@avl_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="avl",
        operation="traverse"
    )
    return jsonify(response), 200


@avl_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="avl",
        operation="reset"
    )
    return jsonify(response), 200
