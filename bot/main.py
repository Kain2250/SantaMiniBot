import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage


from bot.filters import register_all_filters
from bot.misc import TgKeys
from bot.handlers import register_all_handlers
from bot.database.models import register_models
from bot.misc.env import env_load

PROXY = False


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)
    register_models()


async def start_bot():
    env_load()

    if PROXY:
        session = AiohttpSession('http://proxy.server:3128')
        bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML', session=session)
    else:
        bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')

    dp = Dispatcher(storage=MemoryStorage())
    await bot.delete_webhook(drop_pending_updates=True)
    logging.basicConfig(level=logging.NOTSET, filename='bot.log',
                        format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')

    await __on_start_up(dp)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
