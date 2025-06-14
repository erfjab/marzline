from fastapi import APIRouter, Request, HTTPException
from eiogram.types import Update
from src.config import TELEGRAM_WEBHOOK_SECRET_KEY, DP, BOT


router = APIRouter(prefix="/webhook", tags=["Webhook"], include_in_schema=False)


@router.post("")
async def telegram_webhook(request: Request):
    """Handle incoming webhook updates from Telegram."""
    if TELEGRAM_WEBHOOK_SECRET_KEY:
        secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret_token != TELEGRAM_WEBHOOK_SECRET_KEY:
            raise HTTPException(status_code=403, detail="Invalid secret key")
    try:
        data = await request.json()
        data["bot"] = BOT
        update = Update(**data)
        await DP.process(update)
    except Exception as e:
        print(f"Update process failed: {str(e)}")
    return {"result": "success"}
