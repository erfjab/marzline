from eiogram.types import Update
from src.config import DP
from src.db import User, GetDB


@DP.fallback
async def fallback_handler(update: Update):
    if not update.message:
        return
    with GetDB() as db:
        User.add_message(db, update.origin)
        return
