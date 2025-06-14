from fastapi import APIRouter
from . import _telegram


def setup_webhook_routers() -> APIRouter:
    router = APIRouter(prefix="/api")
    router.include_router(_telegram.router)
    return router


__all__ = ["setup_webhook_routers"]
