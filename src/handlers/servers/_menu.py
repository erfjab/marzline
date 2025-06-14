from eiogram import Router
from eiogram.types import CallbackQuery
from src.keyboards import InlineCB, InlineKB, SectionType, ActionType
from src.db import Session, Server
from src.language import MesText

router = Router()


@router.callback_query(
    InlineCB.filter(section=SectionType.SERVER, action=ActionType.MENU)
)
async def servers_menu(callback_query: CallbackQuery, db: Session):
    servers = Server.get_all(db)
    return await callback_query.message.edit(
        text=MesText.SERVERS_MENU, reply_markup=InlineKB.servers_menu(servers=servers)
    )
