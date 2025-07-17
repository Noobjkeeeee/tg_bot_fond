import logging
import asyncio
import threading

from fastapi import FastAPI
from uvicorn import Config, Server

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from config.config import TOKEN
from handlers import welcome, commands

app = FastAPI()


async def start_polling_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.errors.register(commands.error_handler)
    dp.message.register(welcome.handle_new_member, F.new_chat_members)
    dp.message.register(commands.start_command, CommandStart())

    await dp.start_polling(bot)

async def on_startup(bot: Bot):
    logging.info("Бот запущен")
    me = await bot.get_me()
    logging.info(f"Bot @{me.username} ready")

def run_bot_in_thread():
    asyncio.run(start_polling_bot())

@app.get("/")
async def root():
    return {"status": "bot is running"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    bot_thread = threading.Thread(target=run_bot_in_thread, daemon=True)
    bot_thread.start()

    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    asyncio.run(server.serve())
