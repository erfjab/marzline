from uvicorn import Config, Server
from eiogram.types import BotCommand
from src.config import (
    DEBUG,
    UVICORN_PORT,
    UVICORN_SSL_CERTFILE,
    UVICORN_SSL_KEYFILE,
    BOT,
    DP,
    TELEGRAM_WEBHOOK_HOST,
    TELEGRAM_WEBHOOK_SECRET_KEY,
)
from src.api import API
from src.handlers import setup_routers


async def main():
    await BOT.set_webhook(
        url=TELEGRAM_WEBHOOK_HOST,
        secret_token=TELEGRAM_WEBHOOK_SECRET_KEY,
        allowed_updates=[
            "message",
            "callback_query",
            "inline_query",
        ],
    )
    await BOT.set_my_commands(
        commands=[BotCommand(command="/start", description="start/restart bot")]
    )
    DP.include_router(setup_routers())
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
