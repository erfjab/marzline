from typing import Union, Optional
from enum import StrEnum
from eiogram.utils.callback_data import CallbackData


class SectionType(StrEnum):
    HOME = "hm"
    SETTING = "st"


class ActionType(StrEnum):
    MENU = "mn"
    UPDATE = "up"
    SELECT = "sl"
    INFO = "nf"
    CREATE = "cr"


class InlineCB(CallbackData, prefix="a"):
    section: SectionType = SectionType.HOME
    action: ActionType = ActionType.MENU
    target: Optional[Union[str, int]] = None
    command: Optional[Union[str, StrEnum]] = None
