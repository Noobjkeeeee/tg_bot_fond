from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.logger import error_logger
from config.config import MESSAGE_DELETE_DELAY, CHAT_ID
import asyncio

router = Router()


async def delete_message_after_delay(bot, chat_id, message_id):
    await asyncio.sleep(MESSAGE_DELETE_DELAY)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        error_logger.error(f"Ошибка при удалении сообщения: {e}")


@router.message(F.new_chat_members)
async def handle_new_member(message: Message, bot):
    if str(message.chat.id) != CHAT_ID:
        error_logger.warning(
            f"Бот использован в чужом чате: {message.chat.id}")
        return

    try:
        me = await bot.get_me()

        for member in message.new_chat_members:
            user_mention = (
                f"@{member.username}"
                if member.username
                else f"{member.first_name or 'Участник'}"
            )

            welcome_msg = (
                f"{user_mention}, Привет! 💜\n"
                "Мы рады, что ты с нами. Этот чат создан для поддержки.\n"
                "Загляни в ветку "
                "<a href='https://t.me/c/1813228738/65079'>"
                "Важное и правила</a> — там вся основная информация.\n"
                "А теперь давай познакомимся! Расскажи немного о себе:\n"
                "Как тебя зовут? (можно просто имя)\n"
                "Что привело тебя в этот чат?\n"
                "О чём тебе важно поговорить или что узнать?\n"
                "Здесь тебя выслушают. Добро пожаловать! 🌟\n\n"
                "Нажми кнопку ниже, чтобы не потерять нужную информацию"
            )

            keyboard = InlineKeyboardBuilder()
            keyboard.add(
                InlineKeyboardButton(
                    text="📚 Получить важные ссылки",
                    url=f"https://t.me/{me.username}?start=guide",
                )
            )

            sent_message = await message.reply(
                text=welcome_msg, reply_markup=keyboard.as_markup(),
                parse_mode="HTML"
            )

            task = asyncio.create_task(
                delete_message_after_delay(
                    bot, sent_message.chat.id, sent_message.message_id
                )
            )
            task.add_done_callback(
                lambda t: t.exception() and error_logger.error(
                    t.exception()
                )
            )

            error_logger.info(
                f"Новый участник: ID={member.id}, "
                f"Name={member.first_name}, "
                f"Username={member.username or 'отсутствует'}"
            )
    except Exception as e:
        error_logger.error(f"Ошибка в welcome: {e}", exc_info=True)
        from handlers.commands import error_handler

        await error_handler(e, bot)
