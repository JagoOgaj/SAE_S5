from flask import (
    Blueprint, 
    request
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
    create_access_token
)
from backend.app.core import ENUM_BLUEPRINT_ID
from backend.app.core.const.enum import (
    ENUM_ENDPOINT_AUTH, 
    ENUM_METHODS
)
from backend.app.schemas.auth_schemas import (
    LoginSchema,
    ResgistrySchema
)
from marshmallow import ValidationError
from backend.app.services import (
    service_auth,
    service_jwt
)
from backend.app.exeptions import (
    UserNotFound,
    PayloadError,
    UserPasswordNotFound,
    EmailAlreadyUsed
)
from backend.app.core.utility import create_json_response

bp_auth = Blueprint(ENUM_BLUEPRINT_ID.AUTH.value, __name__)


@bp_auth.route(ENUM_ENDPOINT_AUTH.LOGIN.value, methods=[ENUM_METHODS.POST.value])
def login_endpoint():
    try:
        data = LoginSchema().load(request.get_json())
        access_token , refresh_token = service_auth.login(data)
        return create_json_response(
            status="success", 
            message="Connexion accepter", 
            access_token=access_token, 
            refresh_token=refresh_token
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}"
        )
    except UserNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Utilisateur pas trouver",
            details=f"{str(e)}"
        )
    except UserPasswordNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Le mot de passe ne correspond pas",
            details=f"{str(e)}"
        )
    except PayloadError as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Erreur dans la payload",
            details=f"{str(e)}"
        )
    except Exception as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        ) 

@bp_auth.route(ENUM_ENDPOINT_AUTH.REGISTRY.value, methods=[ENUM_METHODS.POST.value])
def registry_endpoint(type: str):
    try:
        data = ResgistrySchema().load(request.get_json())
        service_auth.registry(data, type.strip().lower())
        return create_json_response(
            status_code=201,
            status="sucess",
            message="Enregistrement réaliser"
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}"
        )
    except EmailAlreadyUsed as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="L'email est déjà utiliser",
            details=f"{str(e)}"
        )
    except Exception as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )

@bp_auth.route(ENUM_ENDPOINT_AUTH.LOGOUT.value, methods=[ENUM_METHODS.POST.value])
@jwt_required()
def logout_endpoint():
    try :
        service_jwt.revoke_token(get_jwt()["jti"], get_jwt_identity())
        return create_json_response(
            status_code=201,
            status="success",
            message="Deconnexion reussite"
        )
    
    except Exception as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )
        
@bp_auth.route(ENUM_ENDPOINT_AUTH.REFRESH_TOKEN.value, methods=[ENUM_METHODS.POST.value])
@jwt_required(refresh=True)
def refresh_endpoint():
    try:
        service_jwt.add_token_to_database(
            create_access_token(
                identity=get_jwt_identity()
        ))
        return create_json_response(
            status_code=201,
            status="success",
            message="Le token a bien été refresh"
        )
    except Exception as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )
        
@bp_auth.route(ENUM_ENDPOINT_AUTH.REVOKE_ACCESS_TOKEN.value, methods=[ENUM_METHODS.DELETE.value])
@jwt_required()
def revoke_access_endpoint():
    try :
        service_jwt.revoke_token(get_jwt()["jti"], get_jwt_identity())
        return create_json_response(
            status_code=201,
            status="success",
            message="L'access token a été revoker"
        )
    except Exception as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )


@bp_auth.route(ENUM_ENDPOINT_AUTH.REVOKE_REFRESH_TOKEN.value, methods=[ENUM_METHODS.DELETE.value])
@jwt_required(refresh=True)
def revoke_access_endpoint():
    try :
        service_jwt.revoke_token(get_jwt()["jti"], get_jwt_identity())
        return create_json_response(
            status_code=201,
            status="success",
            message="Le refresh token a été revoker"
        )
    except Exception as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )


