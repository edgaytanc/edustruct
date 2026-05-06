from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

binary_tree_bp = Blueprint(
    "binary-tree",
    __name__,
    url_prefix="/api/binary-tree"
)


@binary_tree_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="binary-tree",
        operation="state"
    )
    return jsonify(response), 200


@binary_tree_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="binary-tree",
        operation="insert"
    )
    return jsonify(response), 200


@binary_tree_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="binary-tree",
        operation="delete"
    )
    return jsonify(response), 200


@binary_tree_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="binary-tree",
        operation="search"
    )
    return jsonify(response), 200


@binary_tree_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="binary-tree",
        operation="demo-load"
    )
    return jsonify(response), 200


@binary_tree_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="binary-tree",
        operation="traverse"
    )
    return jsonify(response), 200


@binary_tree_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="binary-tree",
        operation="reset"
    )
    return jsonify(response), 200
