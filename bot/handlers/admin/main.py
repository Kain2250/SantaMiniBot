import logging

from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Update, Message

from bot.database.methods.get import print_user, print_all_user, get_ward_data
from bot.database.models.user_state import UserStateGroup
from bot.misc.util import randomizer


async def errors_handler(update: Update, exception: Exception):
    logging.error(f'Ошибка при обработке запроса {update}: {exception}')


async def print_user_message(msg: Message, state: FSMContext):
    await print_user(user_id=msg.from_user.id, state=state, msg=msg)
    logging.info(f"Текущий state = {await state.get_state()}\nФункция - print_user_message")


async def print_all_user_message(msg: Message, state: FSMContext):
    await print_all_user(state=state, msg=msg)
    logging.info(f"Текущий state = {await state.get_state()}\nФункция - print_all_user_message")


async def get_user_db(msg: Message, state: FSMContext):
    await get_ward_data(str(msg.from_user.id), state)


async def draw_users(msg: Message, state: FSMContext):
    await randomizer(msg=msg, state=state)


def register_admin_handlers(dp: Dispatcher):
    # dp.register_errors_handler(errors_handler)
    dp.message.register(print_user_message, UserStateGroup.wait_state, F.text == 'print')
    dp.message.register(print_all_user_message, UserStateGroup.wait_state, F.text == 'printall')
    dp.message.register(draw_users, UserStateGroup.wait_state, F.text == 'draw')
    dp.message.register(get_user_db, UserStateGroup.wait_state, F.text == 'get')
