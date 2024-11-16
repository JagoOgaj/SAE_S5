from flask import Blueprint
from core import ENUM_BLUEPRINT_ID

bp_user = Blueprint(ENUM_BLUEPRINT_ID.USER, __name__)

class Controller_USER:
    pass

#TODO Add routes #