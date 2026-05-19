from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.btree_service import BTreeService

btree_bp = Blueprint(
    "btree",
    __name__,
    url_prefix="/api/btree"
)

btree_service = BTreeService()


def _payload():
    return request.get_json(silent=True) or {}


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


def _metrics(result):
    return result.get("metrics")


def _traversal(result):
    return result.get("traversal")


def _coerce_key(value):
    if not isinstance(value, str):
        return value

    normalized = value.strip()
    if not normalized:
        return normalized

    try:
        return int(normalized)
    except ValueError:
        return normalized


def _coerce_order(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if not isinstance(value, str):
        return value

    normalized = value.strip()
    if not normalized:
        return normalized

    try:
        return int(normalized)
    except ValueError:
        return normalized


def _build_success(message, operation, result, status=200, traversal=None):
    response = success_response(
        message=message,
        structure="btree",
        operation=operation,
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=traversal if traversal is not None else _traversal(result),
        result=result,
    )
    return jsonify(response), status


@btree_bp.route("/state", methods=["GET"])
def get_state():
    result = btree_service.state()
    return _build_success(
        message="Estado del Árbol B obtenido correctamente.",
        operation="state",
        result=result,
    )


@btree_bp.route("/configure", methods=["POST"])
def configure():
    payload = _payload()
    raw_order = payload.get("order", request.args.get("order"))
    result = btree_service.configure(_coerce_order(raw_order))
    return _build_success(
        message="Orden del Árbol B configurado correctamente.",
        operation="configure",
        result=result,
    )


@btree_bp.route("/insert", methods=["POST"])
def insert():
    payload = _payload()

    if "keys" in payload:
        result = btree_service.bulk_insert([_coerce_key(key) for key in payload.get("keys")])
        return _build_success(
            message="Claves insertadas correctamente en el Árbol B.",
            operation="bulk-insert",
            result=result,
            status=201,
        )

    result = btree_service.insert(_coerce_key(payload.get("key")))
    return _build_success(
        message="Clave insertada correctamente en el Árbol B.",
        operation="insert",
        result=result,
        status=201,
    )


@btree_bp.route("/bulk-insert", methods=["POST"])
def bulk_insert():
    payload = _payload()
    keys = payload.get("keys")
    normalized_keys = [_coerce_key(key) for key in keys] if isinstance(keys, list) else keys
    result = btree_service.bulk_insert(normalized_keys)
    return _build_success(
        message="Claves insertadas correctamente en el Árbol B.",
        operation="bulk-insert",
        result=result,
        status=201,
    )


@btree_bp.route("/search", methods=["GET"])
def search():
    result = btree_service.search(_coerce_key(request.args.get("key")))
    return _build_success(
        message="Búsqueda ejecutada correctamente en el Árbol B.",
        operation="search",
        result=result,
    )


@btree_bp.route("/demo/load", methods=["POST"])
def load_demo():
    result = btree_service.load_demo()
    return _build_success(
        message="Dataset demo cargado correctamente en el Árbol B.",
        operation="demo-load",
        result=result,
    )


@btree_bp.route("/traverse", methods=["GET"])
def traverse():
    traversal_type = request.args.get("type", "levelorder")
    result = btree_service.traverse(traversal_type)
    return _build_success(
        message="Recorrido del Árbol B obtenido correctamente.",
        operation="traverse",
        result=result,
        traversal=_traversal(result),
    )


@btree_bp.route("/metrics", methods=["GET"])
def metrics():
    result = btree_service.metrics()
    return _build_success(
        message="Métricas del Árbol B obtenidas correctamente.",
        operation="metrics",
        result=result,
    )


@btree_bp.route("/reset", methods=["POST"])
def reset():
    result = btree_service.reset()
    return _build_success(
        message="Árbol B reiniciado correctamente.",
        operation="reset",
        result=result,
    )
