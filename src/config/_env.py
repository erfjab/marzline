from decouple import config, Csv
from dotenv import load_dotenv

load_dotenv(override=True)

TELEGRAM_API_TOKEN = config("TELEGRAM_API_TOKEN", default="")
TELEGRAM_ADMIN_IDS = config("TELEGRAM_ADMIN_IDS", cast=Csv(int), default="") or []
TELEGRAM_LOGGER_CHANNEL_ID = config("TELEGRAM_LOGGER_CHANNEL_ID", cast=int, default=0)
SQLALCHEMY_DATABASE_URL = (
    "mariadb+pymysql://marzlineuser:marzlinepass@localhost:3306/marzlinedb"
)
