from flask import (
    Blueprint,
    request,
    jsonify
)
from backend.app.core import ENUM_BLUEPRINT_ID
from backend.app.core.const.enum import (
    ENUM_ENDPOINT_AUTH,
    ENUM_METHODS
)
from backend.app.schemas.auth_schemas import (
    LoginSchema
)

from marshmallow import ValidationError

bp_auth = Blueprint(ENUM_BLUEPRINT_ID.AUTH.value, __name__)

@bp_auth.route(ENUM_ENDPOINT_AUTH.LOGIN.value, methods=[ENUM_METHODS.POST.value])
def login_endpoint():
    try:
        data = LoginSchema().load(request.get_json())
        
        
    except ValidationError as e:
        pass
    except Exception as e:
        pass