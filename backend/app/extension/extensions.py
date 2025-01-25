from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from passlib.context import CryptContext

type Extension = Extensions


class Extensions:
    def __init__(self: Extension) -> None:
        self._db_ext: MongoEngine = MongoEngine()
        self._ma_ext: Marshmallow = Marshmallow()
        self._jwt_ext: JWTManager = JWTManager()
        self._pwd_context_ext: CryptContext = CryptContext(
            schemes=["pbkdf2_sha256"], deprecated="auto"
        )

    @property
    def db_ext(self: Extension) -> MongoEngine:
        return self._db_ext

    @property
    def ma_ext(self: Extension) -> Marshmallow:
        return self._ma_ext

    @property
    def jwt_ext(self: Extension) -> JWTManager:
        return self._jwt_ext

    @property
    def pwd_context_ext(self: Extension) -> CryptContext:
        return self._pwd_context_ext


ext: Extension = Extensions()
