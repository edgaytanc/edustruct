from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

tree_bp = Blueprint(
    "tree",
    __name__,
    url_prefix="/api/tree"
)


@tree_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="tree",
        operation="state"
    )
    return jsonify(response), 200


@tree_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="tree",
        operation="insert"
    )
    return jsonify(response), 200


@tree_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="tree",
        operation="delete"
    )
    return jsonify(response), 200


@tree_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="tree",
        operation="search"
    )
    return jsonify(response), 200


@tree_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="tree",
        operation="demo-load"
    )
    return jsonify(response), 200


@tree_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="tree",
        operation="traverse"
    )
    return jsonify(response), 200


@tree_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="tree",
        operation="reset"
    )
    return jsonify(response), 200
