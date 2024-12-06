import pytz
from datetime import datetime
from backend.app.core import ENUM_TIMEZONE


def get_paris_time():
    paris_tz = pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    return datetime.now(paris_tz)

def dynamic_limit(route: str):
    #TODO Completer les conditions
    match route:
        case _:
            pass        
            