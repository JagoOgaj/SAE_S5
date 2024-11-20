from enum import Enum as e

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
    
class ENUM_CORS(e):
    RESSOURCE : dict[str, dict[str: str]] = {r"/*": {"origins": "*"}}
    
    
class ENUM_BLUEPRINT_ID(e):
    ADMIN : str = "ADMIN"
    AUTH : str = "AUTH"
    MODEL : str = "MODEL"
    USER : str = "USER"
    
class ENUM_URL_PREFIX(e):
    ADMIN : str = "/admin"
    AUTH : str = "/auth"
    MODEL : str = "/model"
    USER : str = "/user"

class ENUM_ENDPOINT_ADMIN(e):
    pass

class ENUM_ENDPOINT_AUTH(e):
    pass

class ENUM_ENDPOINT_MODEL(e):
    pass

class ENUM_ENDPOINT_USER(e):
    pass

class ENUM_TABLE_DB(e):
    USER: str = "users"
    QUOTAS: str = "quotas"
    HISTORY: str = "histories"
    ROLE: str = "role"

class ENUM_COLUMN_TABLE_USER(e):
    PSEUDO: str = "pseudo"
    EMAIL : str = "email"
    PWD_HASH : str = "password_hash"
    ROLE_ID : str = "role_ids"
    
class ENUM_COLUMN_TABLE_QUOTAS(e):
    USER_ID: str = "user_id"
    DAILY_LIMIT: str = "daily_limit"
    REQUESTS_MADE : str = "requests_made"
    RESET_AT : str = "reset_at"
    
class ENUM_COLUMN_TABLE_HISTORY(e):
    pass

class ENUM_MODEL_NAME(e):
    USER: str = "Model_USER"
    ROLE: str = "Model_ROLE"
    
class ENUM_ROLE(e):
    ADMIN = "ADMIN"
    USER = "USER"