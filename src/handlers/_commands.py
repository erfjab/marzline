from eiogram import Router
from eiogram.types import Message
from eiogram.filters import Command
from src.db import User, Session
from src.language import MesText
from src.keyboards import InlineKB

router = Router()


@router.message(Command("start"))
async def start(message: Message, db: Session, dbuser: User):
    update = await message.answer(
        text=MesText.START.format(**dbuser.format()), reply_markup=InlineKB.home()
    )
    return User.clear_messages(db, update)
