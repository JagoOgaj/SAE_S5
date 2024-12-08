import pytz
from datetime import datetime
from backend.app.core import ENUM_TIMEZONE
from flask import jsonify

def get_paris_time():
    paris_tz = pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    return datetime.now(paris_tz)


def convert_to_datetime(time_to_convert):
    return datetime.fromtimestamp(time_to_convert, tz=pytz.UTC)

def create_json_response(status_code=200, **kwargs):
    response = jsonify(kwargs)
    response.status_code = status_code
    return response

def dynamic_limit(route: str):
    # TODO Completer les conditions
    match route:
        case _:
            pass
