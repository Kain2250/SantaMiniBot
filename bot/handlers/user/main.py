import logging

from aiogram import Dispatcher, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.delete import delete_user
from bot.database.methods.get import get_user
from bot.database.methods.update import update_user
from bot.database.models.user_state import UserStateGroup
from bot.handlers.user.edit_handler import register_edit_handlers
from bot.handlers.user.input_user_data_handlers import register_input_user_data_handlers
from bot.keyboards.reply import get_wait_keyboard, get_draw_keyboard


async def wait_message(msg: Message, state: FSMContext):
    await update_user(user_id=msg.from_user.id, state=state)
    await msg.answer(text="Ожидай начала жеребьевки", reply_markup=get_wait_keyboard())
    logging.info(f"Текущий state = {await state.get_state()} Функция - wait_message")


async def info_user_message(msg: Message, state: FSMContext):
    user = await get_user(msg.from_user.id)
    await msg.answer(f"Твой подопечный:\n\t\t{user[7]}\n"
                     f"Его адрес:\n\t\t{user[8]}\n"
                     f"Его пожелание:\n\t\t{user[9]}",
                     reply_markup=get_draw_keyboard())
    logging.info(f"Текущий state = {await state.get_state()} Функция - info_user_message")


async def draw_message(msg: Message, state: FSMContext, bot: Bot):
    #TODO доделать описание

    data = await state.get_data()

    await bot.send_message(chat_id=data.get('ward_id'), text="Твой Санта уже отправил тебе подарок")
    await msg.answer("Твой подопечный оповещен", reply_markup=None)
    logging.info(f"Текущий state = {await state.get_state()} Функция - draw_message")


async def delete_user_message(msg: Message, state: FSMContext):
    await delete_user(str(msg.from_user.id), msg)
    await state.set_state(UserStateGroup.go_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - delete_user_message")


def register_user_handlers(dp: Dispatcher):
    register_input_user_data_handlers(dp=dp)
    register_edit_handlers(dp=dp)

    dp.message.register(draw_message, F.text == 'Подарок отправлен', UserStateGroup.draw_state)
    dp.message.register(info_user_message, F.text == 'Кому я дарю', UserStateGroup.draw_state)

    dp.message.register(delete_user_message, F.text == 'Отказаться от участия', UserStateGroup.wait_state)
