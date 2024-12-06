from flask import Blueprint
from backend.app.core import ENUM_BLUEPRINT_ID

bp_user = Blueprint(ENUM_BLUEPRINT_ID.USER.value, __name__)


class Controller_USER:
    pass


# TODO Add routes #
