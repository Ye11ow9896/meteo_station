from dotenv import load_dotenv
import os

from pydantic import BaseModel, Field

load_dotenv()

# Database variables
PG_HOST = os.environ.get('PG_HOST')
PG_USER = os.environ.get('PG_USER')
PG_DB_NAME = os.environ.get('PG_DB_NAME')
PG_PORT = os.environ.get('PG_PORT')
PG_PASS = os.environ.get('PG_PASS')
APP_ASYNC_DRIVER = os.environ.get('APP_ASYNC_DRIVER')
ALEMBIC_SYNC_DRIVER = os.environ.get('ALEMBIC_SYNC_DRIVER')

# Auth variable
SALT = os.environ.get('SALT')
TOKEN_SECRET_KEY = os.environ.get('TOKEN_SECRET_KEY')
AUTH_TOKEN_EXPIRE_TIME = os.environ.get('AUTH_TOKEN_EXPIRE_TIME')

# API tokens variable
YANDEX_WEATHER_API_TOKEN = os.environ.get('YANDEX_WEATHER_API_TOKEN')
