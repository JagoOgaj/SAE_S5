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
    