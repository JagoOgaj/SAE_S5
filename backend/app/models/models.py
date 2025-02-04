from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DateTimeField,
    IntField,
    EmbeddedDocumentListField,
    ReferenceField,
    BinaryField,
)

from backend.app.core import ENUM_COLECTION_NAME
from backend.app.core import get_paris_time


class MODEL_USER(Document):
    """
    Modèle représentant un utilisateur.

    Attributes:
        id (int): Identifiant unique de l'utilisateur.
        email (str): Adresse email de l'utilisateur.
        username (str): Nom d'utilisateur.
        password_hash (str): Hachage du mot de passe de l'utilisateur.
        created_at (datetime): Date et heure de création de l'utilisateur.
    """

    id = IntField(primary_key=True)
    email = StringField(required=True, unique=True, max_length=255)
    username = StringField(required=True, unique=True, max_length=255)
    password_hash = StringField(required=True, max_length=255)
    created_at = DateTimeField(default=get_paris_time())

    meta = {"collection": ENUM_COLECTION_NAME.USERS.value}


class MODEL_MESSAGE(EmbeddedDocument):
    """
    Modèle représentant un message dans une conversation.

    Attributes:
        type (str): Type de message (utilisateur ou IA).
        content (str): Contenu du message.
        image (binary): Image associée au message.
        created_at (datetime): Date et heure de création du message.
    """

    type = StringField(required=True, choices=["user", "ia"])
    content = StringField()
    image = BinaryField()
    created_at = DateTimeField(default=get_paris_time())


class MODEL_CONVERSATION(Document):
    """
    Modèle représentant une conversation.

    Attributes:
        id (int): Identifiant unique de la conversation.
        user_id (ReferenceField): Référence à l'utilisateur propriétaire de la conversation.
        name (str): Nom de la conversation.
        created_at (datetime): Date et heure de création de la conversation.
        updated_at (datetime): Date et heure de la dernière mise à jour de la conversation.
        messages (list): Liste des messages dans la conversation.
    """

    id = IntField(
        primary_key=True,
    )
    user_id = ReferenceField(MODEL_USER, required=True, reverse_delete_rule=2)
    name = StringField(required=True, max_length=255)
    created_at = DateTimeField(default=get_paris_time())
    updated_at = DateTimeField(default=get_paris_time())
    messages = EmbeddedDocumentListField(MODEL_MESSAGE)

    meta = {"collection": ENUM_COLECTION_NAME.CONVERSATIONS.value}


class MODEL_TokenBlockList(Document):
    """
    Modèle représentant une liste de tokens révoqués.

    Attributes:
        id (int): Identifiant unique du token révoqué.
        jti (str): Identifiant unique du token.
        token_type (str): Type de token.
        user_id (ReferenceField): Référence à l'utilisateur propriétaire du token.
        revoked_at (datetime): Date et heure de révocation du token.
        expires (datetime): Date et heure d'expiration du token.
    """

    id = IntField(primary_key=True)
    jti = StringField(required=True, unique=True)
    token_type = StringField(required=True, max_length=50)
    user_id = ReferenceField(MODEL_USER, required=True, reverse_delete_rule=2)
    revoked_at = DateTimeField()
    expires = DateTimeField(required=True)

    meta = {"collection": ENUM_COLECTION_NAME.TOKEN.value}


class MODEL_Sequence(Document):
    """
    Modèle pour gérer les séquences d'ID auto-incrémentées.

    Attributes:
        id (str): Nom de la séquence.
        sequence_value (int): Valeur actuelle de la séquence.
    """

    id = StringField(primary_key=True)
    sequence_value = IntField(default=0)

    meta = {"collection": ENUM_COLECTION_NAME.SEQUENCES.value}
