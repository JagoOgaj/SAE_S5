from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validates
)
from backend.app.core.const.enum import (
    ENUM_LOGIN_SCHEMA
)

import re

class LoginSchema(Schema):
    
    email_fields: str = "email"
    password_fields: str = "password"
    
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    
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
        
                
        
            
        
    