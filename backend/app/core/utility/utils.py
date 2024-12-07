import pytz
from datetime import datetime
from backend.app.core import ENUM_TIMEZONE


def get_paris_time():
    paris_tz = pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    return datetime.now(paris_tz)


def convert_to_datetime(time_to_convert):
    return datetime.fromtimestamp(time_to_convert, tz=pytz.UTC)


def dynamic_limit(route: str):
    # TODO Completer les conditions
    match route:
        case _:
            pass
