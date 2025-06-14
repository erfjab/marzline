from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.stats import State, StatsGroup, StatsManager
from eiogram.filters import StatsFilter, Text

from src.keyboards import InlineCB, InlineKB, SectionType, ActionType, UpdateType
from src.db import Session, Server, User
from src.clients import ClinetManager
from src.language import MesText
from src.utils import ResourceNotFoundError, DuplicateError, PatternValidationError


router = Router()


class ServerUpdateForm(StatsGroup):
    INPUT = State()
    APPROVAL = State()


@router.callback_query(
    InlineCB.filter(
        section=SectionType.SERVER,
        action=ActionType.UPDATE,
        target=...,
        command=...,
        approval=None,
    )
)
async def servers_update(
    callback_query: CallbackQuery,
    callback_data: InlineCB,
    db: Session,
    stats: StatsManager,
):
    server = Server.get_by_id(db, int(callback_data.target))
    if not server:
        raise ResourceNotFoundError()

    await stats.upsert_data(command=callback_data.command)
    await stats.upsert_data(target=callback_data.target)

    kb = InlineKB.servers_cancel()
    match callback_data.command:
        case UpdateType.REMARK:
            await stats.set_state(ServerUpdateForm.INPUT)
            text = MesText.ENTER_REMARK
        case UpdateType.REMOVE | UpdateType.ENABLE | UpdateType.DISABLE:
            kb = InlineKB.approval(section=SectionType.SERVER)
            text = MesText.APPROVAL
        case UpdateType.SERVER_CONFIG:
            await stats.set_state(ServerUpdateForm.INPUT)
            text = MesText.ENTER_SERVER_CONFIG

    return await callback_query.message.edit(
        text=text,
        reply_markup=kb,
    )


@router.callback_query(
    InlineCB.filter(section=SectionType.SERVER, action=ActionType.UPDATE, approval=...)
)
async def approval_handler(
    callback_query: CallbackQuery,
    callback_data: InlineCB,
    db: Session,
    stats: StatsManager,
):
    kb = InlineKB.servers_cancel()
    if not callback_data.approval:
        return await callback_query.message.edit(
            text=MesText.FORGET,
            reply_markup=kb,
        )

    data = await stats.get_data()
    server = Server.get_by_id(db, int(data["target"]))
    if not server:
        raise ResourceNotFoundError()

    match data["command"]:
        case UpdateType.REMOVE:
            Server.remove(db, server_id=server.id)
        case UpdateType.ENABLE:
            Server.update(db, server_id=server.id, enable=True)
        case UpdateType.DISABLE:
            Server.update(db, server_id=server.id, enable=False)
    await stats.clear_all()
    return await callback_query.message.edit(
        text=MesText.SUCCESS,
        reply_markup=kb,
    )


@router.message(StatsFilter(ServerUpdateForm.INPUT), Text())
async def input_handler(
    message: Message,
    db: Session,
    stats: StatsManager,
):
    data = await stats.get_data()
    server = Server.get_by_id(db, int(data["target"]))
    if not server:
        raise ResourceNotFoundError()

    kb = InlineKB.servers_cancel()
    match data["command"]:
        case UpdateType.REMARK:
            if Server.get_by_remark(db, message.text):
                raise DuplicateError()
            Server.update(db, server_id=server.id, remark=message.text)
        case UpdateType.SERVER_CONFIG:
            messages = message.text.split(" ")
            if len(messages) != 3:
                raise PatternValidationError()
            config = {
                "username": messages[0],
                "password": messages[1],
                "host": messages[2],
            }
            token = await ClinetManager.generate_access_token(
                config=config, server_type=server.type
            )
            if not token:
                raise ResourceNotFoundError()
            Server.update(
                db,
                server_id=server.id,
                config=config,
            )

    await stats.clear_all()
    update = await message.answer(
        text=MesText.SUCCESS,
        reply_markup=kb,
    )
    return User.clear_messages(db, update)
