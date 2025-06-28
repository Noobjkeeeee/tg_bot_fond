import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
CHAT_ID = os.getenv("CHAT_ID")

MESSAGE_DELETE_DELAY = 24 * 60 * 60

