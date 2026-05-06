def success_response(
    message="Operación realizada correctamente.",
    structure=None,
    operation=None,
    nodes=None,
    edges=None,
    metrics=None,
    traversal=None,
    result=None
):
    return {
        "success": True,
        "message": message,
        "data": {
            "structure": structure,
            "operation": operation,
            "nodes": nodes or [],
            "edges": edges or [],
            "metrics": metrics or default_metrics(),
            "traversal": traversal or default_traversal(),
            "result": result or {}
        },
        "error": None
    }


def error_response(
    message="No se pudo completar la operación.",
    code="INTERNAL_ERROR",
    http_status=500,
    details=None
):
    return {
        "success": False,
        "message": message,
        "data": None,
        "error": {
            "code": code,
            "httpStatus": http_status,
            "details": details or []
        }
    }


def default_metrics():
    return {
        "count": 0,
        "height": None,
        "balanceFactor": None,
        "collisions": None,
        "levels": None,
        "edgesCount": 0
    }


def default_traversal():
    return {
        "type": None,
        "start": None,
        "order": [],
        "steps": []
    }
