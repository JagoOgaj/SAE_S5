from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
import os
from dotenv import load_dotenv
from backend.app.core.const.enum import ENUM_REDIS_ENV

load_dotenv()

redis_host = os.environ.get(ENUM_REDIS_ENV.REDIS_HOST.value)
redis_port = int(os.environ.get(ENUM_REDIS_ENV.REDIS_PORT.value))
redis_db = int(os.environ.get(ENUM_REDIS_ENV.REDIS_DB.value))

redis_connection = Redis(host=redis_host, port=redis_port, db=redis_db)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{redis_host}:{redis_port}/{redis_db}",
)
