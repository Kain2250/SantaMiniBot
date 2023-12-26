import logging

from aiogram import Dispatcher, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Update, Message

from bot.database.methods.get import adm_print_user, adm_print_all_user
from bot.database.models.user_state import UserStateGroup
from bot.misc.util import randomizer


async def errors_handler(update: Update, exception: Exception):
    logging.error(f'Ошибка при обработке запроса {update}: {exception}')


async def adm_print_user_message(msg: Message, state: FSMContext):
    await adm_print_user(user_id=msg.from_user.id, state=state, msg=msg)
    logging.info(f"Текущий state = {await state.get_state()}\nФункция - print_user_message")


async def adm_print_all_user_message(msg: Message, state: FSMContext):
    await adm_print_all_user(msg=msg)
    logging.info(f"Текущий state = {await state.get_state()}\nФункция - print_all_user_message")


async def adm_draw_users(msg: Message, state: FSMContext, bot: Bot):
    await randomizer(msg=msg, state=state, bot=bot)
    logging.info(f"Текущий state = {await state.get_state()}\nФункция - print_all_user_message")


def register_admin_handlers(dp: Dispatcher):
    # dp.register_errors_handler(errors_handler)
    dp.message.register(adm_print_user_message, UserStateGroup.wait_state, F.text == 'print')
    dp.message.register(adm_print_all_user_message, UserStateGroup.wait_state, F.text == 'printall')
    dp.message.register(adm_draw_users, UserStateGroup.wait_state, F.text == 'draw')
