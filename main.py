import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import handlers
from dotenv import load_dotenv
#from data.db import create_db

load_dotenv()

TOKEN = getenv("TOKEN_INFO")
dp = Dispatcher()
dp.include_router(handlers.router)

async def main() -> None:
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())