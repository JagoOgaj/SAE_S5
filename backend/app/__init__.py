from flask import Flask
from dotenv import load_dotenv
from backend.app.core import (
    ENUM_DB_ENV,
    ENUM_FLASK_ENV,
    ENUM_JWT_ENV,
    ENUM_CORS,
    ENUM_URL_PREFIX,
)
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.app.extension import ext
from backend.app.controllers import bp_user, bp_auth, bp_admin, bp_model
from backend.app.core.decorator import Decorators
from typing import Callable
import os

load_dotenv()


class Config:
    # Flask #
    FLASK_HOST = os.environ.get(ENUM_FLASK_ENV.HOST.value)
    FLASK_DEBUG = os.environ.get(ENUM_FLASK_ENV.DEBUG.value)
    FLASK_ENV = os.environ.get(ENUM_FLASK_ENV.ENV.value)
    FLASK_PORT = os.environ.get(ENUM_FLASK_ENV.PORT.value)

    # DB #
    SQLALCHEMY_DATABASE_URI = os.environ.get(ENUM_DB_ENV.URI.value)

    # JWT #
    JWT_SECRET_KEY = os.environ.get(ENUM_JWT_ENV.SECRET_KEY.value)
    JWT_IDENTITY_CLAIM = os.environ.get(ENUM_JWT_ENV.IDENTITY_CLAIM.value)
    JWT_TOKEN_LOCATION = [os.environ.get(ENUM_JWT_ENV.TOKEN_LOCATION.value)]
    JWT_ACCESS_TOKEN_EXPIRES = int(
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
        app.register_blueprint(bp_admin, url_prefix=ENUM_URL_PREFIX.ADMIN.value)
        app.register_blueprint(bp_auth, url_prefix=ENUM_URL_PREFIX.AUTH.value)
        app.register_blueprint(bp_user, url_prefix=ENUM_URL_PREFIX.USER.value)
        app.register_blueprint(bp_model, url_prefix=ENUM_URL_PREFIX.MODEL.value)

        return app


@Decorators.singleton
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
