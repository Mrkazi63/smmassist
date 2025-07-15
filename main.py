import asyncio, logging, os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv

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

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
