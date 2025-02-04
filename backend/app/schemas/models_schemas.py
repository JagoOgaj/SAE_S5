from marshmallow import Schema, fields, validates, ValidationError


class PredictRequestSchema(Schema):
    """
    Schéma de validation pour les requêtes de prédiction de modèle.

    Attributes:
        image_fields (str): Nom du champ image.
        image (fields.Str): Champ pour l'image encodée en base64.
    """

    image_fields: str = "image"

    image = fields.Str(
        required=True,
        error_messages={
            "required": "L'image est un champ requis.",
            "null": "L'image ne peut pas être vide.",
            "invalid": "Veuillez fournir une image valide en base64.",
        },
    )

    @validates(image_fields)
    def validate_image(self, value: str):
        if not value.startswith("data:image"):
            raise ValidationError("L'image doit être au format base64.")
