import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.fsm.storage.redis import RedisStorage

from config import settings
from data.postgresql_connect import create_db, session_factory
from handlers.commands_handler import command_router
from handlers.currency_handlers import currency_router
from handlers.gigachat_hendlers import gigachat_router
from handlers.weather_handlers import weather_router
from middlewares.db_middlewares import DataBaseMiddleware
from utils.commands import register_commands
from utils.logger_settings import setup_logging

logger = logging.getLogger(__name__)


async def bot_connect():
    storage = RedisStorage.from_url(settings.REDIS_URL)
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        command_router,
        weather_router,
        currency_router,
        gigachat_router,
    )
    dp.update.middleware(DataBaseMiddleware(session_pool=session_factory))
    await create_db()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as error:
        logger.error(error)
    finally:
        await bot.close()


def main():
    setup_logging()
    try:
        asyncio.run(bot_connect())
    except TelegramRetryAfter as error:
        logger.error(error)
    except KeyboardInterrupt as error:
        logger.error(error)


if __name__ == '__main__':
    main()
