# refill_handler.py

import os
from aiogram import Router
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
router = Router()

@router.message()
async def debug_all(message: Message):
    print(f"📩 Message received: {message.text} | Chat Type: {message.chat.type} | From: {message.from_user.username}")
    await message.reply("✅ Message received by bot (router works)")
