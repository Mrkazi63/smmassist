# refill_handler.py
import os
import httpx
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

router = Router()

ADMIN_API_URL = os.getenv("PANEL_API_URL")
ADMIN_API_KEY = os.getenv("PANEL_API_KEY")
SUPPORT_GROUP_ID = int(os.getenv("SUPPORT_GROUP_ID", "-1001234567890"))  # replace this with real group ID

@router.message(Command("refill"))
async def handle_refill_request(message: Message):
    print("🔥 /refill command triggered")

    args = message.text.strip().split()
    if len(args) != 2:
        await message.reply("❗ Usage: /refill <order_id>")
        return

    order_id = args[1]
    payload = {
        "key": ADMIN_API_KEY,
        "action": "refill",
        "order": order_id
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(ADMIN_API_URL, data=payload)
            data = res.json()
            print("✅ API Response:", data)

            if data.get("status") == "success":
                await message.reply(f"✅ Refill request sent for Order ID: {order_id}")

                forward_text = (
                    f"📦 *Refill Request Sent*\n"
                    f"• Order ID: `{order_id}`\n"
                    f"• Status: `success`\n"
                    f"• Sent: Just now"
                )
                await message.bot.send_message(chat_id=SUPPORT_GROUP_ID, text=forward_text, parse_mode="Markdown")
            else:
                await message.reply(f"❌ Refill failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print("❌ Exception occurred:", e)
        await message.reply(f"❌ API error: {e}")
