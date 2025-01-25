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
    DB_NAME: str = "MONGO_DB_NAME"
    DB_HOST: str = "MONGO_HOST"
    DB_PORT: str = "MONGO_PORT"
    DB_USERNAME: str = "MONGO_USERNAME"
    DB_PWD: str = "MONGO_USERNAME"


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
    AUTH: str = "AUTH"
    MODEL: str = "MODEL"
    USER: str = "USER"


############################################################
#                                                          #
#                     ENDPOINT-ENUM                        #
#                                                          #
############################################################


class ENUM_URL_PREFIX(e):
    AUTH: str = "/auth"
    MODEL: str = "/model"
    USER: str = "/user"


class ENUM_ENDPOINT_AUTH(e):
    LOGIN: str = "/login"
    REGISTRY: str = "/registry/<string:type>"
    LOGOUT: str = "/logout"
    REFRESH_TOKEN: str = "/refresh"
    REVOKE_ACCESS_TOKEN: str = "/revoke_access"
    REVOKE_REFRESH_TOKEN: str = "/revoke_refresh"


class ENUM_ENDPOINT_MODEL(e):
    PREDICT: str = "/predict/<string:typeModel>"

class ENUM_ENDPOINT_USER(e):
    CONVERSTAION_OVERVIEW: str = "/conversation/overview"
    CONVERSATION_TO_DELETE: str = "/conversations/<int:conversation_id>"
    NEW_CONVERSATION: str = "/new-conversation/"
    CONTINUE_CONVERSATION: str = "/update-conversation/<int:conversation_id>"
    GET_CONVERSATION: str = "/conversation/<int:conversation_id>"


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

class ENUM_COLECTION_NAME(e):
    USERS: str = 'users'
    CONVERSATIONS: str = 'conversations'
    TOKEN: str = 'token_block_list'

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
    FILTERS: list[str] = ["id", "email", "username"]

class ENUM_FIELDS_USER(e):
    FIELDS: list[str] = ['email', 'username', 'password']

class ENUM_FILTERS_TOKEN(e):
    FILTERS: list[str] = [
        "id",
        "jti",
        "token_type",
        "user_id",
        "revoked_at",
        "expires",
    ]
    
class ENUM_CONFIG_DB_KEY(e):
    DB: str = 'db'
    HOST: str = 'host'
    PORT: str = 'port'
    USERNAME: str = 'username'
    PASSWORD: str = 'password'


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



############################################################
#                                                          #
#                     Model Type Enum                      #
#                                                          #
############################################################

class ENUM_MODELS_TYPE(e):
    GENDER_SCRATCH: str = "gs"
    AGE_SCRATCH: str = "as"
    GENDER_AND_AGE_SCRATCH: str = "gas"
    GENDER_AND_AGE_TRANSFER: str = "gat" # sous steorïde

    