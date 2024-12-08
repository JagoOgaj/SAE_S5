from marshmallow import Schema, ValidationError, fields, validates
from backend.app.core.const.enum import ENUM_LOGIN_SCHEMA

import re


class LoginSchema(Schema):
    email_fields: str = "email"
    password_fields: str = "password"

    email = fields.Str(
        required=True,
         error_messages={
            "required" : "L'email est un champs requis",
            "null" : "L'email est un champs qui ne peux pas etre vide",
            "invalid" : "Veuillez fournir une adresse email valide"
        }
    )
    password = fields.Str(
        required=True,
         error_messages={
            "required" : "Le mot de passe est un champs requis",
            "null" : "Le mot de passe ne peux pas etre un champs requis",
            "invalide" : "Veuillez fournir un mot de passe valide"
        }
    )

    @validates(email_fields)
    def validator_email(self, value):
        if not value:
            raise ValidationError(ENUM_LOGIN_SCHEMA.EMAIL_EMPTY_ERROR_MESSAGE.value)

        if not re.match(ENUM_LOGIN_SCHEMA.EMAIL_PATERN.value, value):
            raise ValidationError(ENUM_LOGIN_SCHEMA.EMAIL_REGEX_ERROR_MESSAGE.value)

    @validates(password_fields)
    def validator_password(self, value):
        if not value:
            raise ValidationError(ENUM_LOGIN_SCHEMA.PASSWORD_ERROR.value)

class ResgistrySchema(Schema):
    email_fields: str = "email"
    pseudo_fields: str = "pseudo"
    password: str = "password"
    
    email = fields.Str(
        required=True,
        error_messages={
            "required" : "L'email est un champs requis",
            "null" : "L'email est un champs qui ne peux pas etre vide",
            "invalid" : "Veuillez fournir une adresse email valide"
        }
    )
    
    pseudo = fields.Str(
        required=True,
        validate=[
            fields.Lenght(
                min=2,
                max=50,
                error="Le pseudo doit contenir entre 2 et 50 caractéres"
            )
        ],
        error_messages={
            "required" : "Le pseudo est un champs requis",
            "null" : "Le pseudo est un champs qui ne peux pas etre vide",
            "invalid" : "Veuillez fournir un pseudo valide"
        }
    )
    
    password = fields.Str(
        required=True,
        load_only=True,
        error_messages={
            "required" : "Le mot de passe est un champs requis",
            "null" : "Le mot de passe ne peux pas etre un champs requis",
            "invalid" : "Veuillez fournir un mot de passe valide"
        }
    )
    
    @validates(email_fields)
    def validate_email(self, value):
        if not value:
            raise ValidationError("L'email est requis et ne peut pas être vide.")

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", value):
            raise ValidationError("Format d'email invalide.")

    @validates(password)
    def validate_password_strength(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères."
            )
        if not any(char.islower() for char in value):
            raise ValidationError(
                "Le mot de passe doit contenir au moins une lettre minuscule."
            )
        if not any(char.isupper() for char in value):
            raise ValidationError(
                "Le mot de passe doit contenir au moins une lettre majuscule."
            )
        if not any(char.isdigit() for char in value):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in value):
            raise ValidationError(
                "Le mot de passe doit contenir au moins un caractère spécial."
            )
            
    @validates(pseudo_fields)
    def validate_pseudo(self, value):
        if not value.strip():
            raise ValidationError(
                "Le pseudo ne peux pas etre composé uniquement d'espace"
            )
        