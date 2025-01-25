from flask import Flask
from dotenv import load_dotenv
from backend.app.core import (
    ENUM_DB_ENV,
    ENUM_FLASK_ENV,
    ENUM_JWT_ENV,
    ENUM_CORS,
    ENUM_URL_PREFIX,
    ENUM_CONFIG_DB_KEY
)
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.app.extension import ext
from backend.app.controllers import bp_user, bp_auth, bp_model
from typing import Callable
import os

load_dotenv()


class Config:
    # Flask #
    FLASK_HOST: str = os.environ.get(ENUM_FLASK_ENV.HOST.value)
    FLASK_DEBUG: str = os.environ.get(ENUM_FLASK_ENV.DEBUG.value)
    FLASK_ENV: str = os.environ.get(ENUM_FLASK_ENV.ENV.value)
    FLASK_PORT: str = os.environ.get(ENUM_FLASK_ENV.PORT.value)

    # DB #
    MONGODB_CONFIG: dict[str, str] = {
        ENUM_CONFIG_DB_KEY.DB.value : os.environ.get(ENUM_DB_ENV.DB_NAME.value),
        ENUM_CONFIG_DB_KEY.HOST.value : os.environ.get(ENUM_DB_ENV.DB_HOST.value),
        ENUM_CONFIG_DB_KEY.PORT.value : os.environ.get(ENUM_DB_ENV.DB_PORT.value),
        ENUM_CONFIG_DB_KEY.USERNAME.value : os.environ.get(ENUM_DB_ENV.DB_USERNAME.value),
        ENUM_CONFIG_DB_KEY.PASSWORD.value : os.environ.get(ENUM_DB_ENV.DB_PWD.value) 
    }

    # JWT #
    JWT_SECRET_KEY: str = os.environ.get(ENUM_JWT_ENV.SECRET_KEY.value)
    JWT_IDENTITY_CLAIM: str = os.environ.get(ENUM_JWT_ENV.IDENTITY_CLAIM.value)
    JWT_TOKEN_LOCATION: list[str] = [os.environ.get(ENUM_JWT_ENV.TOKEN_LOCATION.value)]
    JWT_ACCESS_TOKEN_EXPIRES: int = int(
        os.environ.get(ENUM_JWT_ENV.ACCESS_TOKEN_EXPIRES.value)
    )


class App:
    @staticmethod
    def create_app() -> Flask:
        app = Flask(__name__)

        # Load Config object #
        app.config.from_object(Config)

        # Cors #
        CORS(app, resources=ENUM_CORS.RESSOURCE.value)

        # Extensions #
        ext.db_ext.init_app(app)
        ext.ma_ext.init_app(app)
        ext.jwt_ext.init_app(app)

        # Routes with blueprint #
        app.register_blueprint(bp_auth, url_prefix=ENUM_URL_PREFIX.AUTH.value)
        app.register_blueprint(bp_user, url_prefix=ENUM_URL_PREFIX.USER.value)
        app.register_blueprint(bp_model, url_prefix=ENUM_URL_PREFIX.MODEL.value)

        return app


class Quotas:
    def __init__(self, app: Flask, func: Callable[..., str]) -> None:
        self._limiter = Limiter(app, key_func=func)

    @property
    def limiter(self) -> Limiter:
        return self._limiter

    @limiter.setter
    def limiter(self, limiter: Limiter) -> None:
        self._limiter = limiter


app: Flask = App.create_app()
quotas: Quotas = Quotas(app, get_remote_address)
