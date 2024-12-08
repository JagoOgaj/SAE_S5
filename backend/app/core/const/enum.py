from enum import Enum as e

############################################################
#                                                          #
#                       ENV-ENUM                           #
#                                                          #
############################################################


class ENUM_FLASK_ENV(e):
    HOST: str = "FLASK_HOST"
    DEBUG: str = "FLASK_DEBUG"
    ENV: str = "FLASK_ENV"
    PORT: str = "FLASK_PORT"


class ENUM_DB_ENV(e):
    URI: str = "SQLALCHEMY_DATABASE_URI"


class ENUM_JWT_ENV(e):
    SECRET_KEY: str = "JWT_SECRET_KEY"
    IDENTITY_CLAIM: str = "JWT_IDENTITY_CLAIM"
    TOKEN_LOCATION: str = "JWT_TOKEN_LOCATION"
    ACCESS_TOKEN_EXPIRES: str = "JWT_ACCESS_TOKEN_EXPIRES"


############################################################
#                                                          #
#                      CORS-ENUM                           #
#                                                          #
############################################################


class ENUM_CORS(e):
    RESSOURCE: dict[str, dict[str:str]] = {r"/*": {"origins": "*"}}


############################################################
#                                                          #
#                    BLUEPRINT-ENUM                        #
#                                                          #
############################################################


class ENUM_BLUEPRINT_ID(e):
    ADMIN: str = "ADMIN"
    AUTH: str = "AUTH"
    MODEL: str = "MODEL"
    USER: str = "USER"


############################################################
#                                                          #
#                     ENDPOINT-ENUM                        #
#                                                          #
############################################################


class ENUM_URL_PREFIX(e):
    ADMIN: str = "/admin"
    AUTH: str = "/auth"
    MODEL: str = "/model"
    USER: str = "/user"


class ENUM_ENDPOINT_ADMIN(e):
    pass


class ENUM_ENDPOINT_AUTH(e):
    LOGIN: str = "/login"
    REGISTRY: str = "/registry/<string:type>"
    LOGOUT: str = "/logout"
    REFRESH_TOKEN: str = "/refresh"
    REVOKE_ACCESS_TOKEN: str = "/revoke_access"
    REVOKE_REFRESH_TOKEN: str = "/revoke_refresh"


class ENUM_ENDPOINT_MODEL(e):
    pass


class ENUM_ENDPOINT_USER(e):
    pass


class ENUM_METHODS(e):
    POST: str = "POST"
    GET: str = "GET"
    PUT: str = "PUT"
    DELETE: str = "DELETE"


############################################################
#                                                          #
#                       DB-ENUM                            #
#                                                          #
############################################################


class ENUM_TABLE_DB(e):
    USER: str = "users"
    CONVERSATION: str = "conversations"
    CONVERSATION_MESSAGES: str = "conversation_messages"
    CONVERSATION_IMAGES: str = "conversation_images"
    ROLE: str = "roles"
    TOKEN_BLOCK_LIST: str = "token_block_list"


class ENUM_COLUMN_TABLE_ROLE(e):
    NAME: str = "name"


class ENUM_COLUMN_TABLE_USER(e):
    NAME: str = "name"
    EMAIL: str = "email"
    PWD_HASH: str = "password_hash"
    ROLE_ID: str = "role_ids"
    CREATED_AT: str = "created_at"


class ENUM_COLUMN_TABLE_CONVERSATION(e):
    USER_ID: str = "user_id"
    NAME: str = "name"
    START_DATE: str = "start_date"
    UPDATE_AT: str = "updated_at"


class ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE(e):
    CONVERSATION_ID: str = "conversation_id"
    MESSAGE_TYPE: str = "message_type"
    CONTENT: str = "content"
    CREATED_AT: str = "created_at"


class ENUM_COLUMN_TABLE_CONVERSATION_IMAGES(e):
    CONVERSATION_ID: str = "conversation_id"
    IMAGE_DATA: str = "image_data"
    IMAGE_SIZE: str = "image_size"
    CREATED_AT: str = "created_at"


class ENUM_COLUMN_TABLE_TOKEN_BLOCK_LIST(e):
    ID: str = "id"
    JTI: str = "jti"
    TOKEN_TYPE: str = "token_type"
    USER_ID: str = "user_id"
    REVOKED_AT: str = "revoked_at"
    EXPIRES: str = "expires"


class ENUM_FOREIGN_KEY(e):
    ROLE: str = f"{ENUM_TABLE_DB.ROLE.value}.id"
    USER: str = f"{ENUM_TABLE_DB.USER.value}.id"
    CONVERSATION: str = f"{ENUM_TABLE_DB.CONVERSATION.value}.id"


class ENUM_ON_ACTION(e):
    CASCADE: str = "CASCADE"
    SET_NULL: str = "SET NULL"


class ENUM_RELATIONSHIP(e):
    CASCADE: str = "all, delete-orphan"


class ENUM_CONTRAINT(e):
    CONVERSATION_IMAGES: list[str] = ["image_size > 0", "check_image_size_positive"]
    QUOTA_DAILY: list[str] = ["daily_quota >= 0", "check_daily_quota_positive"]
    QUOTA_USED: list[str] = ["used_quota >= 0", "check_used_quota_positive"]


############################################################
#                                                          #
#                      MODEL-ENUM                          #
#                                                          #
############################################################


class ENUM_MODEL_NAME(e):
    USER: str = "Model_USER"
    ROLE: str = "Model_ROLE"
    TOKEN_BLOCK_LIST: str = "Model_TOKEN_BLOCK_LIST"
    CONVERSATION: str = "Model_CONVERSATION"
    CONVERSATION_MESSAGE: str = "Model_CONVERSATION_MESSAGE"
    CONVERSATION_IMAGE: str = "Model_CONVERSATION_IMAGE"


############################################################
#                                                          #
#                          ENUM                            #
#                                                          #
############################################################


class ENUM_ROLE(e):
    ADMIN = "ADMIN"
    USER = "USER"


class ENUM_MESSAGE_TYPE(e):
    USER: str = "USER"
    AI: str = "AI"


class ENUM_TIMEZONE(e):
    TIMEZONE_PARIS: str = "Europe/Paris"


class ENUM_DECODED_TOKEN_KEY(e):
    JTI: str = "jti"
    TYPE: str = "type"
    EXP: str = "exp"


class ENUM_FILTERS_USER(e):
    FILTERS: list[str] = ["id", "_pseudo", "_email", "_role_id"]

class ENUM_FIELDS_USER(e):
    FIELDS: list[str] = ['email', 'pseudo', 'password']

class ENUM_FILTERS_TOKEN(e):
    FILTERS: list[str] = [
        "id",
        "jti",
        "token_type",
        "user_id",
        "revoked_at",
        "exxpires",
    ]


############################################################
#                                                          #
#                       Schema Enum                        #
#                                                          #
############################################################


class ENUM_LOGIN_SCHEMA(e):
    EMAIL_PATERN: str = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    EMAIL_EMPTY_ERROR_MESSAGE: str = "L'email est requis et ne peut pas être vide."
    EMAIL_REGEX_ERROR_MESSAGE: str = "Format d'email invalide."

    PASSWORD_ERROR: str = "Format d'email invalide."
