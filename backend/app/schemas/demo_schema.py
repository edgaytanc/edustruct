from app.errors.exceptions import ValidationError


ALLOWED_DEMO_MODES = {"replace", "append"}


def validate_demo_payload(payload):
    if not payload:
        raise ValidationError(
            message="El payload es obligatorio.",
            details=[
                {
                    "field": "body",
                    "message": "Debe enviar un cuerpo JSON válido."
                }
            ]
        )

    if "dataset" not in payload or payload.get("dataset") in (None, ""):
        raise ValidationError(
            message="El campo dataset es obligatorio.",
            details=[
                {
                    "field": "dataset",
                    "message": "Debe indicar el dataset demo a cargar."
                }
            ]
        )

    mode = payload.get("mode", "replace")

    if mode not in ALLOWED_DEMO_MODES:
        raise ValidationError(
            message="El modo de carga demo no es válido.",
            details=[
                {
                    "field": "mode",
                    "message": "Los modos permitidos son replace y append."
                }
            ]
        )

    return {
        "dataset": payload["dataset"],
        "mode": mode
    }
