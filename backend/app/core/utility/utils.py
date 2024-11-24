import pytz
from datetime import datetime
from core import ENUM_TIMEZONE

def get_paris_time():
    paris_tz = pytz.timezone(ENUM_TIMEZONE.TIMEZONE_PARIS.value)
    return datetime.now(paris_tz)