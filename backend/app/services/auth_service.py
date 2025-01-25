from backend.app.extension import ext
from flask_jwt_extended import (
    create_access_token,   
    create_refresh_token
)
from backend.app.exeptions.custom_exeptions import (
    UserNotFound,
    UserPasswordNotFound,
    PayloadError,
    EmailAlreadyUsed
)
from typing import Tuple
from backend.app.services import (
    service_db,
    service_jwt
)

class Service_AUTH:
    def __init__(self) -> None:
        pass
    
    def login(self, data: dict[... : ...]) -> Tuple[str, str]:
        if (email := data.get("email")) and (password := data.get("password")):
            user = service_db.find_user_by_filters(email=email)

            if not user:
                raise UserNotFound(email=email)

            if not ext.pwd_context_ext.verify(password, user.password_hash):
                raise UserPasswordNotFound(user.id)

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            service_jwt.add_token_to_database(access_token)
            service_jwt.add_token_to_database(refresh_token)
            
            return access_token, refresh_token
            
        raise PayloadError("email", "password")
    
    def registry(self, data: dict[... : ...], userType) -> None:
        if(email:=data.get("email")):
            user = service_db.find_user_by_filters(_email=email)
            
            if user:
                raise EmailAlreadyUsed(email)
            
            service_db.create_user(user, userType)

service_auth: Service_AUTH = Service_AUTH()


