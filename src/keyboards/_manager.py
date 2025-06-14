from typing import Optional
from eiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from eiogram.utils.inline_builder import InlineKeyboardBuilder
from src.language import KeyText
from ._callback import InlineCB, ActionType, SectionType


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
    def home(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=KeyText.SETTING,
            callback_data=InlineCB(
                section=SectionType.SETTING, action=ActionType.MENU
            ).pack(),
        )
        kb.adjust(2)
        return kb.as_markup()
