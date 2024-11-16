from flask import Blueprint
from core import ENUM_BLUEPRINT_ID

bp_admin = Blueprint(ENUM_BLUEPRINT_ID.ADMIN.value, __name__)

class Controller_ADMIN:
    pass


#TODO Add routes #