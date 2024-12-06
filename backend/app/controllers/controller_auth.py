from flask import Blueprint
from backend.app.core import ENUM_BLUEPRINT_ID

bp_auth = Blueprint(ENUM_BLUEPRINT_ID.AUTH.value, __name__)


class Controller_AUTH:
    pass


# TODO Add routes #
@bp_auth.route("/test", methods=["GET"])
def test_auth():
    return jsonify({"message": "Route auth OK"})
