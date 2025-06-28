import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from aiogram import Bot
from config.config import ADMIN_ID

# Настройка логгера
Path("logs").mkdir(exist_ok=True)
error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.ERROR)

handler = RotatingFileHandler(
    "logs/error.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))
error_logger.addHandler(handler)


async def error_handler(update, exception, bot: Bot):
    error_type = type(exception).__name__
    error_msg = str(exception)

    error_logger.error(f"{error_type}: {error_msg}", exc_info=True)

    if ADMIN_ID:
        try:
            await bot.send_message(
                ADMIN_ID,
                f"🚨 Ошибка в боте:\nТип: {error_type}\nСообщение: {error_msg}"
            )
        except Exception as e:
            error_logger.error(f"Не удалось уведомить админа: {e}")
