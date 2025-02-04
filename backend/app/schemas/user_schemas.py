from marshmallow import Schema, fields, validates, ValidationError, validate


class ConversationOverviewRequestSchema(Schema):
    """
    Schéma de validation pour les requêtes de vue d'ensemble des conversations.

    Attributes:
        page_fields (str): Nom du champ page.
        per_page_fields (str): Nom du champ per_page.
        page (fields.Int): Champ pour le numéro de page.
        per_page (fields.Int): Champ pour le nombre d'éléments par page.
    """

    page_fields = "page"
    per_page_fields = "per_page"

    page = fields.Int(
        missing=1, error_messages={"invalid": "Veuillez fournir la donnée en type int"}
    )
    per_page = fields.Int(
        missing=10, error_message={"invalid": "Veuillez fournir la donnée en type int"}
    )

    @validates(page_fields)
    def validate_page(self, value):
        if not isinstance(int, value):
            raise ValidationError(
                f"Le type {type(value)} n'est pas adapté pour cette request il faut en entier"
            )
        if value < 0:
            raise ValidationError("Le nombre de page doit etre supérieur a 0")

    @validates(per_page_fields)
    def validate_per_page(self, value):
        if not isinstance(int, value):
            raise ValidationError(
                f"Le type {type(value)} n'est pas adapté pour cette request il faut en entier"
            )
        if 0 < value > 100:
            raise ValidationError(
                "Le nombre d'item par page doit etre supérieur a 0 et inférieur a 100"
            )


class ConversationImageSchema(Schema):
    """
    Schéma de validation pour les images dans une conversation.

    Attributes:
        image_data (fields.String): Champ pour l'image encodée en base64.
        image_size (fields.Integer): Champ pour la taille de l'image en octets.
        created_at (fields.DateTime): Champ pour la date de création de l'image.
    """

    image_data = fields.String(
        required=True, validate=validate.Length(min=1), description="Image en base64."
    )
    image_size = fields.Integer(
        required=True, description="Taille de l'image en octets."
    )
    created_at = fields.DateTime(
        required=True, description="Date de création de l'image, sinon actuelle."
    )


class ConversationMessageSchema(Schema):
    """
    Schéma de validation pour les messages dans une conversation.

    Attributes:
        message_type (fields.String): Champ pour le type de message (utilisateur ou IA).
        content (fields.String): Champ pour le contenu du message.
        created_at (fields.DateTime): Champ pour la date de création du message.
    """

    message_type = fields.String(
        required=True,
        validate=validate.OneOf(["user_message", "ia_response"]),
        description="Type de message.",
    )
    content = fields.String(required=True, description="Contenu du message.")
    created_at = fields.DateTime(
        required=False, description="Date de création du message, sinon actuelle."
    )


class ConversationSchema(Schema):
    """
    Schéma de validation pour une conversation.

    Attributes:
        name (fields.String): Champ pour le nom de la conversation.
        images (fields.List): Champ pour la liste des images liées à la conversation.
        messages (fields.List): Champ pour la liste des messages de la conversation.
    """

    name = fields.String(required=True, description="Nom de la conversation.")
    images = fields.List(
        fields.Nested(ConversationImageSchema),
        required=False,
        description="Liste des images liées à la conversation.",
    )
    messages = fields.List(
        fields.Nested(ConversationMessageSchema),
        required=False,
        description="Liste des messages de la conversation.",
    )
