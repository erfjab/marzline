from typing import Optional
from eiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from eiogram.utils.inline_builder import InlineKeyboardBuilder
from src.language import KeyText
from src.db import Server, ServerType
from ._callback import InlineCB, ActionType, SectionType, UpdateType


class InlineKB:
    @classmethod
    def _add_back_cancel(
        cls,
        kb: InlineKeyboardBuilder,
        *,
        section: Optional[SectionType] = None,
    ):
        buttons = []

        if section:
            buttons.append(
                InlineKeyboardButton(
                    text=KeyText.BACK,
                    callback_data=InlineCB(section=section).pack(),
                )
            )

        buttons.append(
            InlineKeyboardButton(
                text=KeyText.HOME,
                callback_data=InlineCB().pack(),
            )
        )

        kb.row(*buttons, size=2)

    @classmethod
    def _add_create(
        cls,
        kb: InlineKeyboardBuilder,
        *,
        section: Optional[SectionType],
    ):
        buttons = []

        buttons.append(
            InlineKeyboardButton(
                text=KeyText.CREATE,
                callback_data=InlineCB(
                    section=section, action=ActionType.CREATE
                ).pack(),
            )
        )

        kb.row(*buttons, size=1)

    @classmethod
    def home(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=KeyText.SERVERS,
            callback_data=InlineCB(
                section=SectionType.SERVER, action=ActionType.MENU
            ).pack(),
        )
        kb.adjust(2)
        return kb.as_markup()

    @classmethod
    def servers_menu(cls, servers: list[Server]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for server in servers:
            kb.add(
                text=server.kb_remark,
                callback_data=InlineCB(
                    section=SectionType.SERVER, action=ActionType.INFO, target=server.id
                ).pack(),
            )
        kb.adjust(2)
        cls._add_create(kb, section=SectionType.SERVER)
        cls._add_back_cancel(kb)
        return kb.as_markup()

    @classmethod
    def servers_update(cls, server: Server) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        updates = [
            UpdateType.DISABLE if server.enable else UpdateType.ENABLE,
            UpdateType.REMARK,
            UpdateType.REMOVE,
            UpdateType.SERVER_CONFIG,
        ]
        for update in updates:
            kb.add(
                text=KeyText.update_key(update),
                callback_data=InlineCB(
                    section=SectionType.SERVER,
                    action=ActionType.UPDATE,
                    target=server.id,
                    command=update,
                ).pack(),
            )
        kb.adjust(2, 2, 2)
        cls._add_back_cancel(kb, section=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def servers_cancel(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        cls._add_back_cancel(kb, section=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def servers_types(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for server in [ServerType.MARZBAN, ServerType.MARZNESHIN]:
            kb.add(
                text=server,
                callback_data=InlineCB(
                    section=SectionType.SERVER,
                    action=ActionType.CREATE,
                    target=server,
                ).pack(),
            )
        kb.adjust(1)
        cls._add_back_cancel(kb, section=SectionType.SERVER)
        return kb.as_markup()

    @classmethod
    def approval(cls, section: SectionType) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=KeyText.YES,
            callback_data=InlineCB(
                section=section, action=ActionType.UPDATE, approval=True
            ).pack(),
        )
        kb.add(
            text=KeyText.NO,
            callback_data=InlineCB(
                section=section, action=ActionType.UPDATE, approval=False
            ).pack(),
        )
        kb.adjust(2)
        cls._add_back_cancel(kb, section=SectionType.SERVER)
        return kb.as_markup()
