import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import handlers
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("MY_TOKEN")
dp = Dispatcher()
dp.include_router(handlers.router)

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())