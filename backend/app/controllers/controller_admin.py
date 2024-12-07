from flask import Blueprint
from backend.app.core import ENUM_BLUEPRINT_ID

bp_admin = Blueprint(ENUM_BLUEPRINT_ID.ADMIN.value, __name__)
