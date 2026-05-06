from flask import Blueprint, jsonify

from app.serializers.response_serializer import success_response

btree_bp = Blueprint(
    "btree",
    __name__,
    url_prefix="/api/btree"
)


@btree_bp.route("/state", methods=["GET"])
def get_state():
    response = success_response(
        message="Estado obtenido correctamente.",
        structure="btree",
        operation="state"
    )
    return jsonify(response), 200


@btree_bp.route("/insert", methods=["POST"])
def insert():
    response = success_response(
        message="Endpoint insert preparado.",
        structure="btree",
        operation="insert"
    )
    return jsonify(response), 200


@btree_bp.route("/delete", methods=["DELETE"])
def delete():
    response = success_response(
        message="Endpoint delete preparado.",
        structure="btree",
        operation="delete"
    )
    return jsonify(response), 200


@btree_bp.route("/search", methods=["GET"])
def search():
    response = success_response(
        message="Endpoint search preparado.",
        structure="btree",
        operation="search"
    )
    return jsonify(response), 200


@btree_bp.route("/demo/load", methods=["POST"])
def load_demo():
    response = success_response(
        message="Endpoint demo/load preparado.",
        structure="btree",
        operation="demo-load"
    )
    return jsonify(response), 200


@btree_bp.route("/traverse", methods=["GET"])
def traverse():
    response = success_response(
        message="Endpoint traverse preparado.",
        structure="btree",
        operation="traverse"
    )
    return jsonify(response), 200


@btree_bp.route("/reset", methods=["POST"])
def reset():
    response = success_response(
        message="Endpoint reset preparado.",
        structure="btree",
        operation="reset"
    )
    return jsonify(response), 200
