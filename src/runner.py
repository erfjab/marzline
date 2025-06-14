from uvicorn import Config, Server
from src.config import (
    DEBUG,
    UVICORN_PORT,
    UVICORN_SSL_CERTFILE,
    UVICORN_SSL_KEYFILE,
    BOT,
    TELEGRAM_WEBHOOK_HOST,
    TELEGRAM_WEBHOOK_SECRET_KEY,
)
from src.api import API


async def main():
    await BOT.set_webhook(
        url=TELEGRAM_WEBHOOK_HOST, secret_token=TELEGRAM_WEBHOOK_SECRET_KEY
    )
    cfg = Config(
        app=API,
        host="0.0.0.0",
        port=UVICORN_PORT,
        workers=1,
    )
    if not DEBUG:
        cfg.ssl_certfile = UVICORN_SSL_CERTFILE
        cfg.ssl_keyfile = UVICORN_SSL_KEYFILE
    server = Server(cfg)
    await server.serve()
