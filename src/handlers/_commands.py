from eiogram import Router
from eiogram.types import Message
from eiogram.filters import Command
from src.db import User, Session

router = Router(name="commands")


@router.message(Command("start"))
async def start(message: Message, db: Session):
    update = await message.answer("Hi user")
    return User.clear_messages(db, update)
