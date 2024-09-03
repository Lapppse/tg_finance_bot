import asyncio

import aiogram
import handlers
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from db import create_db
from loguru import logger
from utils import config

bot = aiogram.Bot(
    token=config.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = aiogram.Dispatcher()
dp.include_routers(handlers.input_router)


async def start_bot():
    logger.info("starting bot")
    create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
