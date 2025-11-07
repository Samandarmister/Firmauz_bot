import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [1234567891, 1234567891]  # Admin Telegram IDlarini kiriting
DATA_PATH = "data"
