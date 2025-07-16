import os
import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
router = Router()

ADMIN_API_URL = os.getenv("PANEL_API_URL")
ADMIN_API_KEY = os.getenv("PANEL_API_KEY")
SUPPORT_GROUP_ID = int(os.getenv("SUPPORT_GROUP_ID"))  # Telegram group ID for manual refill forwarding

@router.message(Command("refill"))
async def handle_refill_request(message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("❗ Usage: /refill <order_id>")
        return

    order_id = args[1]
    payload = {
        "key": ADMIN_API_KEY,
        "action": "getRefill"
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(ADMIN_API_URL, data=payload)
            data = res.json()
            if data.get("status") == "success":
                task_id = data.get("id")
                await message.reply(f"✅ Refill request sent for Order ID: {order_id} (Task ID: {task_id})")

                # Send to support group
                forward_text = (
                    f"📦 *Refill Request*\n"
                    f"• Order ID: `{order_id}`\n"
                    f"• Task ID: `{task_id}`\n"
                    f"• Link: {data.get('link')}\n"
                    f"• Quantity: {data.get('quantity')}\n"
                    f"• Service ID: {data.get('service_id')}"
                )
                await message.bot.send_message(chat_id=SUPPORT_GROUP_ID, text=forward_text, parse_mode="Markdown")

            else:
                await message.reply(f"❌ Refill failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        await message.reply(f"❌ API error: {e}")
