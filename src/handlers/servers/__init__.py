from eiogram import Router
from . import _menu, _info, _update, _create


def setup_servers_router() -> Router:
    router = Router()
    router.include_router(_menu.router)
    router.include_router(_info.router)
    router.include_router(_update.router)
    router.include_router(_create.router)
    return router


__all__ = ["setup_servers_router"]
