from eiogram import Router
from . import _commands, _fallback  # noqa
from ._middlewares import UserMiddleware
from .servers import setup_servers_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(_commands.router)
    router.include_router(setup_servers_router())
    router.middleware.register(UserMiddleware())
    return router


__all__ = ["setup_routers"]
