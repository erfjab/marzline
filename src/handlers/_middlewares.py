from typing import Any, Callable, Dict, Awaitable
from eiogram.middleware import BaseMiddleware
from eiogram.types import Update
from src.db import User, GetDB, Session
from src.utils import PatternValidationError, DuplicateError, ResourceNotFoundError
from src.language import MesText


class UserMiddleware(BaseMiddleware):
    def __init__(self, priority: int = 0):
        super().__init__(priority)

    async def _answer(self, db: Session, update: Update, text: str):
        if update.message:
            _update = await update.message.answer(text=text)
            return User.add_message(db, _update)
        elif update.callback_query:
            return await update.callback_query.answer(text=text, show_alert=True)

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
            try:
                return await handler(update, data)
            except PatternValidationError:
                await self._answer(db, update, MesText.ERROR_PATTERN)
            except DuplicateError:
                await self._answer(db, update, MesText.ERROR_DUPLICATE)
            except ValueError:
                await self._answer(db, update, MesText.ERROR_INTEGER)
            except ResourceNotFoundError:
                await self._answer(db, update, MesText.ERROR_NOT_FOUND)
            return None
