from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from utils.logger import error_logger
from config.config import ADMIN_ID, CHAT_ID

router = Router()


async def error_handler(exception, bot: Bot):
    error_type = type(exception).__name__
    error_msg = str(exception)

    error_logger.error(f"{error_type}: {error_msg}", exc_info=True)

    if ADMIN_ID:
        try:
            await bot.send_message(
                ADMIN_ID,
                "🚨 Ошибка в боте:\n"
                f"Тип: {error_type}\n"
                f"Сообщение: {error_msg}",
            )
        except Exception as e:
            error_logger.error(f"Не удалось уведомить админа: {e}")


@router.message(CommandStart())
async def start_command(message: Message, bot: Bot):
    try:
        if (message.chat.type != "private"
                and str(message.chat.id) != CHAT_ID):
            error_logger.warning(
                f"Попытка использования бота в чате {message.chat.id}"
            )
            return

        await bot.get_me()
        args = message.text.split()[1:] if len(
            message.text.split()) > 1 else []

        if args and args[0] == "guide":
            guide_text = (
                "Привет! 💜\n"
                "Рады видеть тебя в нашем чате. Чтобы проще было освоиться,"
                " мы собрали самые важные посты для прочтения:\n\n"
                "⏩ <a href='https://t.me/c/1813228738/65079/94421'>"
                "О ФОНДЕ - ПРОГРАММЫ ПОДДЕРЖКИ</a>\n"
                "⏩ <a href='https://t.me/c/1813228738/65079/94422'>"
                "СОЦСЕТИ ФОНДА</a>\n"
                "⏩ <a href='https://t.me/c/1813228738/65079/89691'>"
                "ЭКСКУРСИЯ ПО ЧАТУ</a>\n"
                "⏩ <a href='https://t.me/c/1813228738/65079/94423'>"
                "ПРАВИЛА ЧАТА</a>\n"
                "⏩ <a href='https://vk.com/app5898182_-153631713#s=2608034'>"
                "СКАЧАТЬ БУКЛЕТ ПЕРВОЙ ПОМОЩИ</a>\n\n"
                "Если есть вопросы — спрашивай! Здесь всегда поддержат\n"
                "А теперь заходи в общий чат и знакомься с участниками.\n"
                "Добро пожаловать! 🌟"
            )
            await message.answer(
                guide_text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        else:
            await message.answer("Привет! Я бот-помощник.")

    except Exception as e:
        error_logger.error(f"Ошибка: {e}", exc_info=True)
        await message.answer("⚠️ Произошла ошибка. Администратор уведомлен.")
        await error_handler(e, bot)
