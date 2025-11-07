
from loader import dp
import asyncio
import sqlite3
import os
import handlers
from aiogram import executor
import logging
from config import DATA_PATH
import admin
from database import init_db, init_security_tables, BLOCK_SECONDS  
from database import cleanup_access_logs

async def scheduler():
    while True:
        await cleanup_access_logs()
        await asyncio.sleep(3600)  # 1 soat kutadi

async def on_startup(dp):
    asyncio.create_task(scheduler())
    print("✅ Background cleaner ishga tushdi")


logging.basicConfig(level=logging.INFO, filename="bot.log", encoding="utf-8")

if __name__ == '__main__':
    init_db()  # Ma'lumotlar bazasini ishga tushirish
    init_security_tables()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)