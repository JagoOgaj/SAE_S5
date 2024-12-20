from marshmallow import (
    Schema,
    fields,
    pre_dump,
    validates,
    ValidationError,
    validate
)
import pytz

class ConversationOverviewSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)        
    start_date = fields.DateTime(required=True)
    
    @pre_dump
    def convert_start_date_to_paris_tz(self, data, **kwargs):
        paris_tz = pytz.timezone("Europe/Paris")
        if data.start_data.tzinfo is None:
            data.start_date = data.start_date.replace(tzinfo=pytz.utc).astimezone(paris_tz)
        else :
            data.start_date = data.start_date.astimezone(paris_tz)
        return data

class ConversationOverviewRequestSchema(Schema):
    page_fields = "page"
    per_page_fields = "per_page"
    
    page = fields.Int(missing=1, error_messages={
        "invalid": "Veuillez fournir la donnée en type int"
    })
    per_page = fields.Int(missing=10, error_message={
        "invalid" : "Veuillez fournir la donnée en type int"
    })
    
    @validates(page_fields)
    def validate_page(self, value):
        if not isinstance(int, value):
            raise ValidationError(f"Le type {type(value)} n'est pas adapté pour cette request il faut en entier")
        if value < 0:
            raise ValidationError("Le nombre de page doit etre supérieur a 0")
    
    @validates(per_page_fields)
    def validate_per_page(self, value):
        if not isinstance(int, value):
            raise ValidationError(f"Le type {type(value)} n'est pas adapté pour cette request il faut en entier")
        if 0 < value > 100:
            raise ValidationError("Le nombre d'item par page doit etre supérieur a 0 et inférieur a 100")
        

class ConversationImageSchema(Schema):
    image_data = fields.String(required=True, validate=validate.Length(min=1), description="Image en base64.")
    image_size = fields.Integer(required=True, description="Taille de l'image en octets.")
    created_at = fields.DateTime(required=True, description="Date de création de l'image, sinon actuelle.")

class ConversationMessageSchema(Schema):
    message_type = fields.String(required=True, validate=validate.OneOf(["user_message", "ia_response"]), description="Type de message.")
    content = fields.String(required=True, description="Contenu du message.")
    created_at = fields.DateTime(required=False, description="Date de création du message, sinon actuelle.")

class ConversationSchema(Schema):
    name = fields.String(required=True, description="Nom de la conversation.")
    images = fields.List(fields.Nested(ConversationImageSchema), required=False, description="Liste des images liées à la conversation.")
    messages = fields.List(fields.Nested(ConversationMessageSchema), required=False, description="Liste des messages de la conversation.")