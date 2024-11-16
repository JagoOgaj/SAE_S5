from flask import Blueprint
from core import ENUM_BLUEPRINT_ID

bp_auth = Blueprint(ENUM_BLUEPRINT_ID.AUTH.value, __name__)

class Controller_AUTH:
    pass


#TODO Add routes #