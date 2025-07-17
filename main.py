import asyncio
import logging
import os

from fastapi import FastAPI
import uvicorn

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from config.config import TOKEN
from handlers import welcome, commands

app = FastAPI()

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.startup.register(lambda _: logging.info("Бот запущен"))
dp.errors.register(commands.error_handler)
dp.message.register(welcome.handle_new_member, F.new_chat_members)
dp.message.register(commands.start_command, CommandStart())

@app.get("/")
async def root():
    return {"status": "Bot is running"}

async def start_web_and_bot():
    port = int(os.getenv("PORT", 8000))
    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)

    polling_task = asyncio.create_task(dp.start_polling(bot))
    server_task = asyncio.create_task(server.serve())

    await asyncio.gather(polling_task, server_task)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_web_and_bot())