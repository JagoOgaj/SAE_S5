from flask import (
    Blueprint,
    request
)
from backend.app.core.utility import create_json_response
from backend.app.exeptions import ModelTypeNotFoundError
from backend.app import quotas
from backend.app.core.const.enum import (
    ENUM_ENDPOINT_MODEL,
    ENUM_METHODS,
    ENUM_BLUEPRINT_ID
)
from backend.app.services.models_service import (
    Model_CNN,
    get_quota_for_model
)
from backend.app.schemas import (
    PredictRequestSchema,
)
from marshmallow import ValidationError

bp_model = Blueprint(ENUM_BLUEPRINT_ID.MODEL.value, __name__)

@bp_model.route(ENUM_ENDPOINT_MODEL.TRIALS.value, methods=[ENUM_METHODS.POST.value])
@quotas.limiter.limit("5 per day")
def trials(modelType: str):
    try :
        data = PredictRequestSchema().load(request.get_json())
        image_base64 = data.get("image")
        model = Model_CNN(modelType)
        return create_json_response(
            status="success",
            message=model.get_prediction(image_base64)
        )
    except ValidationError as e:
        create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}"
        )
    except TypeError as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Erreur de type de donnée",
            details=f"{str(e)}"
        )
            
    except ModelTypeNotFoundError as e:
        create_json_response(
            status=404,
            status="fail",
            message="Aucun model trouvée",
            details=f"{str(e)}"
        )
    except Exception as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )
        

@bp_model.route(ENUM_ENDPOINT_MODEL.PREDICT.value, methods=[ENUM_METHODS.POST.value])
@quotas.limiter.limit(get_quota_for_model)
def trials(modelType: str):
    try :
        data = PredictRequestSchema().load(request.get_json())
        image_base64 = data.get("image")
        model = Model_CNN(modelType)
        return create_json_response(
            status="success",
            message=model.get_prediction(image_base64)
        )
    except ValidationError as e:
        create_json_response(
            status_code=400,
            status="fail",
            message="Erreur dans la validation des données fournis",
            details=f"{str(e)}"
        )
    except TypeError as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Erreur de type de donnée",
            details=f"{str(e)}"
        )
    except ModelTypeNotFoundError as e:
        create_json_response(
            status=404,
            status="fail",
            message="Aucun model trouvée",
            details=f"{str(e)}"
        )
    except Exception as e:
        create_json_response(
            status_code=404,
            status="fail",
            message="Une erreur est survenue",
            details=f"{str(e)}"
        )