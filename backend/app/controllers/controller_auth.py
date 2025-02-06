from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from backend.app.core import ENUM_BLUEPRINT_ID
from backend.app.core.const.enum import ENUM_ENDPOINT_AUTH, ENUM_METHODS
from backend.app.schemas.auth_schemas import (
    LoginSchema, 
    ResgistrySchema,
    ResetPasswordRequestSchema,
    ResetPasswordSchema
)
from marshmallow import ValidationError
from backend.app.services.auth_service import service_auth
from backend.app.services.jwt_service import service_jwt
from backend.app.exeptions import (
    UserNotFound,
    PayloadError,
    UserPasswordNotFound,
    EmailAlreadyUsed,
)
from backend.app.core.utility import create_json_response

bp_auth = Blueprint(ENUM_BLUEPRINT_ID.AUTH.value, __name__)


@bp_auth.route(ENUM_ENDPOINT_AUTH.LOGIN.value, methods=[ENUM_METHODS.POST.value])
def login_endpoint():
    """
    Endpoint pour la connexion de l'utilisateur.

    Valide les données de connexion et retourne des tokens d'accès et de rafraîchissement si la connexion est réussie.

    Exemple de payload d'entrée:
    {
        "email": "user@example.com",
        "password": "password123"
    }

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Connexion acceptée",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }

    Retourne:
        Réponse JSON avec les tokens d'accès et de rafraîchissement ou un message d'erreur.
    """
    try:
        data = LoginSchema().load(request.get_json())
        access_token, refresh_token = service_auth.login(data)
        return create_json_response(
            status="success",
            message="Connexion accepter",
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}",
        )
    except UserNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Utilisateur pas trouver",
            details=f"{str(e)}",
        )
    except UserPasswordNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Le mot de passe ne correspond pas",
            details=f"{str(e)}",
        )
    except PayloadError as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Erreur dans la payload",
            details=f"{str(e)}",
        )
    except Exception as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )


@bp_auth.route(ENUM_ENDPOINT_AUTH.REGISTRY.value, methods=[ENUM_METHODS.POST.value])
def registry_endpoint():
    """
    Endpoint pour l'enregistrement de l'utilisateur.

    Valide les données d'enregistrement et crée un nouvel utilisateur.

    Exemple de payload d'entrée:
    {
        "email": "user@example.com",
        "username": "username",
        "password": "password123"
    }

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Enregistrement réalisé",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        data = ResgistrySchema().load(request.get_json())
        access_token, refresh_token = service_auth.registry(data)
        return create_json_response(
            status_code=201,
            status="sucess",
            message="Enregistrement réaliser",
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}",
        )
    except EmailAlreadyUsed as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="L'email est déjà utiliser",
            details=f"{str(e)}",
        )
    except Exception as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )


@bp_auth.route(ENUM_ENDPOINT_AUTH.LOGOUT.value, methods=[ENUM_METHODS.POST.value])
@jwt_required()
def logout_endpoint():
    """
    Endpoint pour la déconnexion de l'utilisateur.

    Révoque le token d'accès de l'utilisateur actuel.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Déconnexion réussie"
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        service_jwt.revoke_token(get_jwt()["jti"], get_jwt_identity())
        return create_json_response(
            status_code=201, status="success", message="Deconnexion reussite"
        )

    except Exception as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )


@bp_auth.route(ENUM_ENDPOINT_AUTH.REQUEST_RESET_PASSWORD.value, methods=[ENUM_METHODS.POST.value])
def request_reset_password():
    """
    Endpoint pour demander la réinitialisation du mot de passe.

    Reçoit l'email de l'utilisateur et envoie un email avec un lien de réinitialisation contenant un token JWT.
    """
    try:
        data = ResetPasswordRequestSchema().load(request.get_json())
        email = data["email"]
        service_auth.send_reset_password_email(email)
        return create_json_response(
            status_code=200,
            status="success",
            message="Un email de réinitialisation a été envoyé.",
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournies",
            details=str(e),
        )
    except UserNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Utilisateur non trouvé",
            details=str(e),
        )
    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur est survenue",
            details=str(e),
        )


@bp_auth.route(ENUM_ENDPOINT_AUTH.RESET_PASSWORD.value, methods=[ENUM_METHODS.POST.value])
@jwt_required()
def reset_password():
    """
    Endpoint pour réinitialiser le mot de passe.

    Reçoit le token JWT et le nouveau mot de passe, et met à jour le mot de passe de l'utilisateur.
    """
    try:
        data = ResetPasswordSchema().load(request.get_json())
        new_password = data["password"]
        user_id = get_jwt_identity()
        service_auth.reset_password(user_id, new_password)
        return create_json_response(
            status_code=200,
            status="success",
            message="Le mot de passe a été réinitialisé avec succès.",
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournies",
            details=str(e),
        )
    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur est survenue",
            details=str(e),
        )

@bp_auth.route(
    ENUM_ENDPOINT_AUTH.REFRESH_TOKEN.value, methods=[ENUM_METHODS.POST.value]
)
@jwt_required(refresh=True)
def refresh_endpoint():
    """
    Endpoint pour rafraîchir le token d'accès.

    Génère un nouveau token d'accès pour l'utilisateur actuel.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Le token a bien été rafraîchi",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        access_token = service_auth.getNewAccessToken(get_jwt_identity())
        return create_json_response(
            status_code=201, status="success", 
            message="Le token a bien été refresh",
            access_token=access_token,
        )
    except Exception as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )


@bp_auth.route(
    ENUM_ENDPOINT_AUTH.REVOKE_ACCESS_TOKEN.value, methods=[ENUM_METHODS.DELETE.value]
)
@jwt_required()
def revoke_access_endpoint():
    """
    Endpoint pour révoquer le token d'accès.

    Révoque le token d'accès de l'utilisateur actuel.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Le token d'accès a été révoqué"
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        service_jwt.revoke_token(get_jwt()["jti"], get_jwt_identity())
        return create_json_response(
            status_code=201, status="success", message="L'access token a été revoker"
        )
    except Exception as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )


@bp_auth.route(
    ENUM_ENDPOINT_AUTH.REVOKE_REFRESH_TOKEN.value, methods=[ENUM_METHODS.DELETE.value]
)
@jwt_required(refresh=True)
def revoke_refresh_token_endpoint():
    """
    Endpoint pour révoquer le token de rafraîchissement.

    Révoque le token de rafraîchissement de l'utilisateur actuel.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Le token de rafraîchissement a été révoqué"
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        service_jwt.revoke_token(get_jwt()["jti"], get_jwt_identity())
        return create_json_response(
            status_code=201, status="success", message="Le refresh token a été revoker"
        )
    except Exception as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )
