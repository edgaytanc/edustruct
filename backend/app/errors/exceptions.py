class AppError(Exception):
    status_code = 500
    code = "INTERNAL_ERROR"
    message = "Error interno del servidor."

    def __init__(self, message=None, details=None):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.details = details or []


class ValidationError(AppError):
    status_code = 400
    code = "VALIDATION_ERROR"
    message = "Error de validación."


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"
    message = "Recurso no encontrado."


class DuplicateKeyError(AppError):
    status_code = 409
    code = "DUPLICATE_KEY"
    message = "La clave ya existe en la estructura."


class InvalidOperationError(AppError):
    status_code = 422
    code = "INVALID_OPERATION"
    message = "Operación inválida para la estructura solicitada."


class StructureEmptyError(AppError):
    status_code = 422
    code = "STRUCTURE_EMPTY"
    message = "La estructura está vacía."


class DatasetError(AppError):
    status_code = 422
    code = "DATASET_ERROR"
    message = "El dataset demo no es válido o no es compatible."
