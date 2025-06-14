from typing import Any
from enum import StrEnum


class KeyText(StrEnum):
    HOME = "🏛 Home"
    BACK = "⬅️ Back"
    SETTING = "⚙️ Setting"
    CREATE = "➕ Create"
    REMARK = "📝 Remark"
    ENABLE = "🟢 Enable"
    DISABLE = "🔴 Disable"
    SERVER_CONFIG = "🗃 Config"
    REMOVE = "🗑 Remove"
    YES = "✅ Yes"
    NO = "❌ No"
    SERVERS = "🗃 Servers"

    @classmethod
    def update_key(cls, update: Any) -> StrEnum:
        from src.keyboards._callback import UpdateType

        data = {
            UpdateType.ENABLE: cls.ENABLE,
            UpdateType.DISABLE: cls.DISABLE,
            UpdateType.REMARK: cls.REMARK,
            UpdateType.REMOVE: cls.REMOVE,
            UpdateType.SERVER_CONFIG: cls.SERVER_CONFIG,
        }
        return data[update]
