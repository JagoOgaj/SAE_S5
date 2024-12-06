from flask import Blueprint
from backend.app.core import ENUM_BLUEPRINT_ID

bp_model = Blueprint(ENUM_BLUEPRINT_ID.MODEL.value, __name__)


class Controller_MODEL:
    pass


# TODO Add routes #
@bp_model.route("/test", methods=["GET"])
def test_model():
    return jsonify({"message": "Route model OK"})
