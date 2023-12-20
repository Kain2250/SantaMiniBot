import logging

from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.update import update_user
from bot.database.models.user_state import UserStateGroup
from bot.keyboards.reply import get_wait_keyboard


async def input_name_message(msg: Message, state: FSMContext):
    await state.update_data(dict([('user_name', msg.text), ('is_input_name', 1)]))

    await msg.answer(text="Введи свой адрес, Санта не в курсе где ты живешь")
    await state.set_state(UserStateGroup.input_address_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - input_name_message")


async def input_address_message(msg: Message, state: FSMContext):
    await state.update_data(dict([('address', msg.text), ('is_input_address', 1)]))
    await msg.answer(text="Введи свои пожелания в формате:\n\nХочу - Яхту..\nНе хочу - Ржавые гвозди...\n\n"
                          "Чтобы Санта точно не ошибся с подарком")

    await state.set_state(UserStateGroup.input_wish_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - input_address_message")


async def input_wish_message(msg: Message, state: FSMContext):
    await state.update_data(dict([('wish', msg.text), ('is_input_wish', 1)]))
    await state.set_state(UserStateGroup.wait_state)
    await update_user(msg=msg, state=state)
    await msg.answer(text="Ожидай начала жеребьевки", reply_markup=get_wait_keyboard().as_markup())
    logging.info(f"Текущий state = {await state.get_state()} Функция - input_wish_message")


def register_input_user_data_handlers(dp: Dispatcher):
    dp.message.register(input_name_message, UserStateGroup.input_name_state)
    dp.message.register(input_address_message, UserStateGroup.input_address_state)
    dp.message.register(input_wish_message, UserStateGroup.input_wish_state)
