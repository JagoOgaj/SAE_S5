from flask import Blueprint
from backend.app.core import ENUM_BLUEPRINT_ID

bp_admin = Blueprint(ENUM_BLUEPRINT_ID.ADMIN.value, __name__)

class Controller_ADMIN:
    pass


#TODO Add routes #
@bp_admin.route('/test', methods=['GET'])
def test_admin():
    return jsonify({"message": "Route admin OK"})