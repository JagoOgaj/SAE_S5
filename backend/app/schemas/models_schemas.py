from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError
)
import re

class PredictRequestSchema(Schema):
    image_fields: str = "image"
    
    image = fields.Str(
        required=True,
        error_messages={
            "required": "L'image est un champ requis.",
            "null": "L'image ne peut pas être vide.",
            "invalid": "Veuillez fournir une image valide en base64."
        }
    )
    
    @validates(image_fields)
    def validate_image(self, value: str):
        if not value.startswith("data:image"):
            raise ValidationError("L'image doit être au format base64.")
        
    