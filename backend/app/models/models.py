from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DateTimeField,
    IntField,
    EmbeddedDocumentListField,
    ReferenceField,
    BinaryField
)

from backend.app.core import ENUM_COLECTION_NAME
from backend.app.core import get_paris_time

class MODEL_USER(Document):
    id = IntField(primary_key=True)
    email = StringField(required=True, unique=True, max_length=255)
    username = StringField(required=True, unique=True, max_length=255)
    password_hash = StringField(required=True, max_length=255)
    created_at = DateTimeField(default=get_paris_time())

    meta = {'collection': ENUM_COLECTION_NAME.USERS.value}

class MODEL_MESSAGE(EmbeddedDocument):
    type = StringField(required=True, choices=['user', 'ia'])
    content = StringField() 
    image = BinaryField()  
    created_at = DateTimeField(default=get_paris_time())

class MODEL_CONVERSATION(Document):
    id = IntField(primary_key=True)
    user_id = ReferenceField(MODEL_USER, required=True, reverse_delete_rule=2) 
    name = StringField(required=True, max_length=255)
    created_at = DateTimeField(default=get_paris_time())
    updated_at = DateTimeField(default=get_paris_time())
    messages = EmbeddedDocumentListField(MODEL_MESSAGE)
    
    meta = {'collection': ENUM_COLECTION_NAME.CONVERSATIONS.value}

class MODEL_TokenBlockList(Document):
    id = IntField(primary_key=True)
    jti = StringField(required=True, unique=True)
    token_type = StringField(required=True, max_length=50)
    user_id = ReferenceField(MODEL_USER, required=True, reverse_delete_rule=2)
    revoked_at = DateTimeField()
    expires = DateTimeField(required=True)

    meta = {'collection': ENUM_COLECTION_NAME.TOKEN.value}