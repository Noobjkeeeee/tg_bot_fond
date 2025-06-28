import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from config.config import TOKEN
from handlers import welcome, commands


async def on_startup(bot: Bot):
    logging.info("Бот запущен")
    me = await bot.get_me()
    logging.info(f"Bot @{me.username} ready")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()


    dp.startup.register(on_startup)
    dp.errors.register(commands.error_handler)

    # Регистрация обработчиков
    dp.message.register(welcome.handle_new_member, F.new_chat_members)
    dp.message.register(commands.start_command, CommandStart())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())