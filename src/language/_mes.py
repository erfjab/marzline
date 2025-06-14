from enum import StrEnum


class MesText(StrEnum):
    START = "<b>👋🏻 Hi Dear <code>{full_name}</code></b>"
    SERVERS_MENU = "<b>📡 Server management menu</b>"
    SERVERS_INFO = (
        "<b>Remark:</b> <code>{remark}</code>\n"
        "<b>Enable:</b> <code>{enable}</code>\n"
        "<b>Type:</b> <code>{type}</code>\n"
        "<b>Config:</b>\n<pre>{config}</pre>\n"
    )
    ENTER_REMARK = "📝 Enter a remark [name]:\n💡 Master, test..."
    SELECT_TYPE = "🪖 Select a type:"
    ENTER_SERVER_CONFIG = (
        "🗃 Enter server config [panel]:\n"
        "- Username\n"
        "- Password\n"
        "- Host (https://sub.domain.com:port)\n"
        "💡 Erfan Sfw74sd https://panel.erfjab.top:80"
    )
    SUCCESS = "✅ Successfully"
    FAILED = "❌ Unsuccessful"
    FORGET = "Ok..."
    APPROVAL = "❔ Are you sure?"
    ERROR_PATTERN: str = "⚠️ لطفا متن را طبق الگوی تعریف شده وارد کنید."
    ERROR_DUPLICATE: str = "⚠️ ورودی تکراری، لطفا مورد غیرتکراری وارد کنید."
    ERROR_UNAVAILABLE: str = "⚠️ سرویس در حال حاضر در دسترس نمی‌باشد."
    ERROR_INTEGER: str = "⚠️ ورودی شما باید عدد باشد."
    ERROR_NOT_FOUND: str = "⚠️ آیتم موردنظر یافت نشد."
