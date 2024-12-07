from backend.app.models.models import Model_USER
from backend.app.extension import ext
from flask_jwt_extended import create_access_token, create_refresh_token

from backend.app.exeptions.custom_exeptions import (
    UserNotFound,
    UserPasswordNotFound,
    PayloadError,
)

from backend.app.services.db_service import service_db


def login(data: dict[...:...]):
    if (email := data.get("email")) and (password := data.get("password")):
        user = service_db.find_user_by_filters(_email=email)

        if not user:
            raise UserNotFound(email=email)

        if not ext.pwd_context_ext.verify(password, user.password_hash):
            raise UserPasswordNotFound(user.id)

    raise PayloadError("email", "password")
