from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

graph_bp = Blueprint(
    "graph",
    __name__,
    url_prefix="/api/graph"
)


@graph_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="graph",
        operation="state"
    )
    return jsonify(response), 200


@graph_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="graph",
        operation="insert"
    )
    return jsonify(response), 200


@graph_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="graph",
        operation="delete"
    )
    return jsonify(response), 200


@graph_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="graph",
        operation="search"
    )
    return jsonify(response), 200


@graph_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="graph",
        operation="demo-load"
    )
    return jsonify(response), 200


@graph_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="graph",
        operation="traverse"
    )
    return jsonify(response), 200


@graph_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="graph",
        operation="reset"
    )
    return jsonify(response), 200
