from decouple import config, Csv
from dotenv import load_dotenv

load_dotenv(override=True)

TELEGRAM_API_TOKEN = config("TELEGRAM_API_TOKEN")
TELEGRAM_ADMIN_IDS = config("TELEGRAM_ADMIN_IDS", cast=Csv(int)) or []
TELEGRAM_LOGGER_CHANNEL_ID = config("TELEGRAM_LOGGER_CHANNEL_ID", cast=int, default=0)
SQLALCHEMY_DATABASE_URL = (
    "mariadb+pymysql://marzlineuser:marzlinepass@localhost:3306/marzlinedb"
)

DEBUG = config("DEBUG", default=False, cast=bool)
UVICORN_PORT = config("UVICORN_PORT", cast=int)
TELEGRAM_WEBHOOK_SECRET_KEY = config("TELEGRAM_WEBHOOK_SECRET_KEY")
TELEGRAM_WEBHOOK_HOST = config("TELEGRAM_WEBHOOK_HOST")
UVICORN_SSL_CERTFILE = config("UVICORN_SSL_CERTFILE", default="")
UVICORN_SSL_KEYFILE = config("UVICORN_SSL_KEYFILE", default="")
