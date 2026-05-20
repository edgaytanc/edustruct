"""REST routes for the EduStruct hash table module."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.serializers.response_serializer import success_response
from app.services.hash_table_service import HashTableService

hash_table_bp = Blueprint(
    "hash",
    __name__,
    url_prefix="/api/hash"
)

hash_table_service = HashTableService()


def _payload():
    return request.get_json(silent=True) or {}


def _nodes(result):
    return result.get("nodes", [])


def _edges(result):
    return result.get("edges", [])


def _metrics(result):
    return result.get("metrics")


def _coerce_capacity(value):
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


def _build_success(message, operation, result, status=200):
    response = success_response(
        message=message,
        structure="hash",
        operation=operation,
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        result=result,
    )
    return jsonify(response), status


@hash_table_bp.route("/state", methods=["GET"])
def get_state():
    """Return the current hash table state."""
    result = hash_table_service.state()
    return _build_success(
        message="Estado de la tabla hash obtenido correctamente.",
        operation="state",
        result=result,
    )


@hash_table_bp.route("/configure", methods=["POST"])
def configure():
    """Configure table capacity and reset current state."""
    payload = _payload()
    raw_capacity = payload.get("capacity", request.args.get("capacity"))
    result = hash_table_service.configure(_coerce_capacity(raw_capacity))
    return _build_success(
        message="Capacidad de la tabla hash configurada correctamente.",
        operation="configure",
        result=result,
    )


@hash_table_bp.route("/insert", methods=["POST"])
def insert():
    """Insert one key/value pair or accept entries alias for bulk insert."""
    payload = _payload()

    if "entries" in payload:
        result = hash_table_service.bulk_insert(payload.get("entries"))
        return _build_success(
            message="Entradas insertadas correctamente en la tabla hash.",
            operation="bulk-insert",
            result=result,
            status=201,
        )

    result = hash_table_service.insert(payload.get("key"), payload.get("value"))
    return _build_success(
        message="Entrada insertada correctamente en la tabla hash.",
        operation="insert",
        result=result,
        status=201,
    )


@hash_table_bp.route("/bulk-insert", methods=["POST"])
def bulk_insert():
    """Insert multiple key/value pairs."""
    payload = _payload()
    result = hash_table_service.bulk_insert(payload.get("entries"))
    return _build_success(
        message="Entradas insertadas correctamente en la tabla hash.",
        operation="bulk-insert",
        result=result,
        status=201,
    )


@hash_table_bp.route("/search", methods=["GET"])
def search():
    """Search one entry by carnet/key."""
    result = hash_table_service.search(request.args.get("key"))
    return _build_success(
        message="Búsqueda ejecutada correctamente en la tabla hash.",
        operation="search",
        result=result,
    )


@hash_table_bp.route("/delete", methods=["DELETE"])
def delete():
    """Delete one entry by carnet/key."""
    payload = _payload()
    raw_key = payload.get("key") if "key" in payload else request.args.get("key")
    result = hash_table_service.delete(raw_key)
    return _build_success(
        message="Entrada eliminada correctamente de la tabla hash.",
        operation="delete",
        result=result,
    )


@hash_table_bp.route("/demo/load", methods=["POST"])
def load_demo():
    """Load deterministic student data designed to produce collisions."""
    result = hash_table_service.load_demo()
    return _build_success(
        message="Dataset demo cargado correctamente en la tabla hash.",
        operation="demo-load",
        result=result,
    )


@hash_table_bp.route("/metrics", methods=["GET"])
def metrics():
    """Return hash table metrics."""
    result = hash_table_service.metrics()
    return _build_success(
        message="Métricas de la tabla hash obtenidas correctamente.",
        operation="metrics",
        result=result,
    )


@hash_table_bp.route("/traverse", methods=["GET"])
def traverse():
    """Expose bucket traversal as a didactic chain-by-chain inspection."""
    result = hash_table_service.state()
    traversal_steps = []
    for bucket in result.get("buckets", []):
        for item in bucket.get("items", []):
            traversal_steps.append({
                "step": len(traversal_steps) + 1,
                "bucketIndex": bucket["bucketIndex"],
                "key": item["key"],
                "value": item["value"],
                "chainPosition": item["chainPosition"],
                "collision": item["collision"],
            })

    result["traversal"] = {
        "type": "buckets",
        "start": 0 if result.get("capacity", 0) > 0 else None,
        "order": [step["key"] for step in traversal_steps],
        "steps": traversal_steps,
    }
    response = success_response(
        message="Recorrido por buckets de la tabla hash obtenido correctamente.",
        structure="hash",
        operation="traverse",
        nodes=_nodes(result),
        edges=_edges(result),
        metrics=_metrics(result),
        traversal=result["traversal"],
        result=result,
    )
    return jsonify(response), 200


@hash_table_bp.route("/reset", methods=["POST"])
def reset():
    """Clear the hash table."""
    result = hash_table_service.reset()
    return _build_success(
        message="Tabla hash reiniciada correctamente.",
        operation="reset",
        result=result,
    )
