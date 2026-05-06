from app.errors.exceptions import ValidationError


def validate_key_payload(payload):
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

    if "key" not in payload or payload.get("key") in (None, ""):
        raise ValidationError(
            message="El campo key es obligatorio.",
            details=[
                {
                    "field": "key",
                    "message": "El campo key es obligatorio."
                }
            ]
        )

    return payload


def validate_insert_payload(payload):
    validate_key_payload(payload)

    if "value" not in payload or payload.get("value") is None:
        raise ValidationError(
            message="El campo value es obligatorio.",
            details=[
                {
                    "field": "value",
                    "message": "El campo value es obligatorio."
                }
            ]
        )

    if not isinstance(payload.get("value"), dict):
        raise ValidationError(
            message="El campo value debe ser un objeto.",
            details=[
                {
                    "field": "value",
                    "message": "El campo value debe ser un objeto JSON."
                }
            ]
        )

    return payload
