from flask import Blueprint, request
from backend.app.schemas.user_schemas import (
    ConversationOverviewRequestSchema,
    ConversationSchema,
    MessagesSchema,
    UpdatedConversation,
)
from backend.app.core.const.enum import (
    ENUM_ENDPOINT_USER,
    ENUM_BLUEPRINT_ID,
    ENUM_METHODS,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.services.user_service import Service_USER
from marshmallow import ValidationError
from backend.app.core.utility import create_json_response
from backend.app.exeptions.custom_exeptions import (
    ConversationNotFoundError,
    ConversationImagesNotFound,
    ConversationMessagesNotFound,
    NotAllowedToAccessThisConversationError,
)
from mongoengine.errors import MongoEngineException

bp_user = Blueprint(ENUM_BLUEPRINT_ID.USER.value, __name__)


@bp_user.route(
    ENUM_ENDPOINT_USER.CONVERSTAION_OVERVIEW.value, methods=[ENUM_METHODS.POST.value]
)
@jwt_required()
def get_conversations():
    """
    Endpoint pour récupérer les conversations de l'utilisateur.

    Récupère les conversations de l'utilisateur actuel avec pagination.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Conversations récupérées avec succès",
        "data": {
            "Aujourd'hui": [
                {
                    "id": 1,
                    "name": "Conversation 1"
                },
                ...
            ],
            "Hier": [
                {
                    "id": 2,
                    "name": "Conversation 2"
                },
                ...
            ],
            ...
        }
    }

    Retourne:
        Réponse JSON avec les données des conversations ou un message d'erreur.
    """
    try:
        curentUserId = get_jwt_identity()

        data = Service_USER(curentUserId).getUserConversationsByPeriod()
        return create_json_response(
            status="success", message=f"Conversations récupérées avec succès", data=data
        )
    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Paramètres de requête invalides",
            details=f"{str(e)}",
        )
    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur est survenue",
            details=str(e),
        )


@bp_user.route(
    ENUM_ENDPOINT_USER.CONVERSATION_TO_DELETE.value, methods=[ENUM_METHODS.DELETE.value]
)
@jwt_required()
def delete_conversation(conversation_id):
    """
    Endpoint pour supprimer une conversation.

    Supprime la conversation spécifiée pour l'utilisateur actuel.

    Args:
        idConversation (int): ID de la conversation à supprimer.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Conversation et toutes ses données ont été supprimées avec succès"
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        curentUserId = get_jwt_identity()

        Service_USER(curentUserId).deleteConversation(int(conversation_id))
        return create_json_response(
            status="success",
            message="Conversation et toutes ses données ont été supprimées avec succès",
        )
    except TypeError as e:
        return create_json_response(
            status_code=400, status="fail", message="Erreur de type", details=str(e)
        )

    except ConversationNotFoundError as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Conversation non trouvée",
            details=str(e),
        )

    except ConversationMessagesNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Messages de la conversation non trouvés",
            details=str(e),
        )

    except ConversationImagesNotFound as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message="Images de la conversation non trouvées",
            details=str(e),
        )

    except MongoEngineException as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Erreur de base de données lors de la suppression.",
            details=str(e),
        )

    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur est survenue.",
            details=str(e),
        )


@bp_user.route(
    ENUM_ENDPOINT_USER.NEW_CONVERSATION.value, methods=[ENUM_METHODS.POST.value]
)
@jwt_required()
def create_conversation():
    """
    Endpoint pour créer une nouvelle conversation.

    Crée une nouvelle conversation pour l'utilisateur actuel.

    Exemple de payload d'entrée:
    {
        "id": 1,
        "user_id": 1,
        "name": "First Conversation",
        "created_at": "2025-01-25T12:05:00Z",
        "updated_at": "2025-01-25T12:10:00Z",
        "messages": [
            {
                "type": "user",
                "image": "base64_encoded_image_data",
                "content": null,
                "created_at": "2025-01-25T12:05:30Z"
            },
            {
                "type": "ia",
                "content": "Hello, how can I assist you?",
                "image": null,
                "created_at": "2025-01-25T12:06:00Z"
            }
        ]
    }
    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Conversation créée avec succès"
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        curentUserId = get_jwt_identity()
        data = ConversationSchema().load(request.get_json())

        newConversation_id = Service_USER(curentUserId).createConversation(data)
        return create_json_response(
            status_code=201,
            status="success",
            message="La conversation a été créée avec succès",
            details={"newConversation_id": newConversation_id},
        )

    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur de validation des données",
            details=str(e.messages),
        )

    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur interne est survenue",
            details=str(e),
        )


@bp_user.route(
    ENUM_ENDPOINT_USER.CONTINUE_CONVERSATION.value, methods=[ENUM_METHODS.PUT.value]
)
@jwt_required()
def update_conversation(conversation_id):
    """
    Endpoint pour mettre à jour une conversation existante.

    Met à jour les détails de la conversation spécifiée pour l'utilisateur actuel.

    Args:
        idConversation (int): ID de la conversation à mettre à jour.

    Exemple de payload d'entrée:
    {
        "name": "Conversation Mise à Jour",
        "messages": [
            {
                "message_type": "user_message",
                "content": "Message mis à jour",
                "created_at": "2023-01-01T00:00:00Z"
            }
        ],
        "images": [
            {
                "image_data": "base64_encoded_image_string",
                "created_at": "2023-01-01T00:00:00Z"
            }
        ]
    }

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Conversation mise à jour avec succès"
    }

    Retourne:
        Réponse JSON avec un message de succès ou un message d'erreur.
    """
    try:
        curentUserId = get_jwt_identity()
        conversationUpdatedSchema = UpdatedConversation()
        data = request.get_json()
        if not data:
            raise Exception("Aucune donnée fournis ou ne contiens pas la clé messages")

        messages = conversationUpdatedSchema.load(data)

        Service_USER(curentUserId).updateConversation(
            messages.get("messages"), conversation_id
        )

        return create_json_response(
            status_code=200, status="success", message="Conversation mise à jour"
        )

    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur de validation des données.",
            details=str(e.messages),
        )

    except TypeError as e:
        return create_json_response(
            status_code=400, status="fail", message="Erreur de type", details=str(e)
        )

    except ConversationNotFoundError as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message=f"Conversation avec l'ID {conversation_id} non trouvée.",
        )

    except NotAllowedToAccessThisConversationError as e:
        return create_json_response(
            status_code=403,
            status="fail",
            message="Vous n'êtes pas autorisé à accéder à cette conversation.",
        )

    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur inconnue est survenue.",
            details=str(e),
        )


@bp_user.route(
    ENUM_ENDPOINT_USER.GET_CONVERSATION.value, methods=[ENUM_METHODS.GET.value]
)
@jwt_required()
def get_conversation(conversation_id):
    """
    Endpoint pour récupérer une conversation spécifique.

    Récupère les détails de la conversation spécifiée pour l'utilisateur actuel.

    Args:
        idConversation (int): ID de la conversation à récupérer.

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Conversation récupérée avec succès",
        "data": {
            "id": 1,
            "name": "Conversation 1",
            "messages": [
                {
                    "id": 1,
                    "content": "Message 1",
                    "created_at": "2023-01-01T00:00:00Z"
                },
                ...
            ]
        }
    }

    Retourne:
        Réponse JSON avec les détails de la conversation ou un message d'erreur.
    """
    try:
        curentUserId = get_jwt_identity()

        data = Service_USER(curentUserId).get_conversation(int(conversation_id))

        return create_json_response(
            status_code=200,
            status="success",
            message="Conversation récupérée avec succès.",
            data=data,
        )

    except TypeError as e:
        return create_json_response(
            status_code=400, status="fail", message="Erreur de type", details=str(e)
        )

    except ValidationError as e:
        return create_json_response(
            status_code=400,
            status="fail",
            message="Erreur de validation des données.",
            details=str(e.messages),
        )

    except ConversationNotFoundError as e:
        return create_json_response(
            status_code=404,
            status="fail",
            message=f"Conversation avec l'ID {conversation_id} non trouvée.",
        )

    except NotAllowedToAccessThisConversationError as e:
        return create_json_response(
            status_code=403,
            status="fail",
            message="Vous n'êtes pas autorisé à accéder à cette conversation.",
        )

    except Exception as e:
        return create_json_response(
            status_code=500,
            status="fail",
            message="Une erreur inconnue est survenue.",
            details=str(e),
        )
