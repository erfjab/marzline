from typing import Any, Callable, Dict, Awaitable
from eiogram.middleware import BaseMiddleware
from eiogram.types import Update
from src.db import User, GetDB


class UserMiddleware(BaseMiddleware):
    def __init__(self, priority: int = 0):
        super().__init__(priority)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any],
    ):
        with GetDB() as db:
            user = update.origin.from_user
            dbuser = User.upsert(db, user=user)
            if update.message:
                User.add_message(db, update.message)
            if not dbuser.is_owner:
                return False
            data["dbuser"] = dbuser
            data["db"] = db
            return await handler(update, data)
