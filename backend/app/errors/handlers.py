from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.errors.exceptions import AppError
from app.serializers.response_serializer import error_response


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = error_response(
            message=error.message,
            code=error.code,
            http_status=error.status_code,
            details=error.details
        )
        return jsonify(response), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = error_response(
            message=error.description,
            code=error.name.upper().replace(" ", "_"),
            http_status=error.code,
            details=[]
        )
        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        response = error_response(
            message="Error interno del servidor.",
            code="INTERNAL_ERROR",
            http_status=500,
            details=[]
        )
        return jsonify(response), 500
