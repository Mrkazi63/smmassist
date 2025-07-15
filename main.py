import asyncio, logging, os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from perfectpanel_api import get_order_status

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def on_startup(bot: Bot):
    me = await bot.get_me()
    logging.info(f"🤖 Bot @{me.username} started!")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.startup.register(on_startup)

    # /start handler
    @dp.message(CommandStart())
    async def start(m: types.Message):
        await m.answer(
            "👋 Welcome to <b>ElectroSMM Assistant</b>!\n"
            "Send me any order-related question and I’ll help you out."
        )

    # /status handler
    @dp.message(lambda msg: msg.text.startswith("/status"))
    async def order_status_handler(m: types.Message):
        try:
            parts = m.text.strip().split()
            if len(parts) != 2:
                return await m.reply("❌ Usage: /status <order_id>")

            order_id = parts[1]
            result = await get_order_status(order_id)

            if "error" in result:
                await m.reply(f"❌ Error: {result['error']}")
            else:
                quantity = int(result.get("quantity", 0))
                remains = int(result.get("remains", 0))
                delivered = quantity - remains
                await m.reply(
                    f"📦 <b>Order #{order_id}</b>\n"
                    f"Status: <b>{result['status']}</b>\n"
                    f"Quantity: {quantity}\n"
                    f"Start Count: {result.get('start_count', '-')}\n"
                    f"Delivered: {delivered}\n"
                    f"Remains: {remains}\n"
                    f"Charge: ₹{result.get('charge', '0.00')}"
                )
        except Exception as e:
            await m.reply("⚠️ Something went wrong. Please try again later.")
            print(e)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
