from flask import Blueprint, request
from backend.app.core.utility import create_json_response
from backend.app.exeptions import ModelTypeNotFoundError
from backend.app.core.const.enum import (
    ENUM_ENDPOINT_MODEL,
    ENUM_METHODS,
    ENUM_BLUEPRINT_ID,
)
from backend.app.services.models_service import Service_MODEL, get_quota_for_model
from backend.app.schemas import (
    PredictRequestSchema,
)
from marshmallow import ValidationError
from backend.app.limiter import limiter

bp_model = Blueprint(ENUM_BLUEPRINT_ID.MODEL.value, __name__)


@bp_model.route(ENUM_ENDPOINT_MODEL.PREDICT.value, methods=[ENUM_METHODS.POST.value])
@limiter.limit(get_quota_for_model)
def predict(modelType: str):
    """
    Endpoint pour la prédiction de modèle.

    Valide les données d'entrée et retourne le résultat de la prédiction.

    Args:
        modelType (str): Type de modèle à utiliser pour la prédiction.

    Exemple de payload d'entrée:
    {
        "image": "base64_encoded_image_string"
    }

    Exemple de payload de sortie:
    {
        "status": "success",
        "message": "Résultat de la prédiction"
    }

    Retourne:
        Réponse JSON avec le résultat de la prédiction ou un message d'erreur.
    """
    try:
        data = PredictRequestSchema().load(request.get_json())
        image_base64 = data.get("image")
        model = Service_MODEL(modelType)
        return create_json_response(
            status="success", message=model.get_prediction(image_base64)
        )
    except ValidationError as e:
        create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}",
        )
    except TypeError as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Erreur de type de donnée",
            details=f"{str(e)}",
        )
    except ModelTypeNotFoundError as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Aucun model trouvée",
            details=f"{str(e)}",
        )
    except Exception as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}",
        )
