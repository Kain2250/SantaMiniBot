import logging

from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.update import update_user
from bot.database.models.user_state import UserStateGroup
from bot.keyboards.reply import get_edit_reply_keyboard, get_wait_keyboard


async def edit_user_message(msg: Message, state: FSMContext):
    await msg.answer(text="Выбери что хочешь отредактировать",
                     reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_user_message")


async def edit_name(msg: Message, state: FSMContext):
    await state.update_data(dict([('user_name', msg.text)]))
    await msg.answer(text="Имя отредактировано", reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_name")


async def edit_address(msg: Message, state: FSMContext):
    await state.update_data(dict([('address', msg.text)]))
    await msg.answer(text="Адрес отредактирован",
                     reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_address")


async def edit_wish(msg: Message, state: FSMContext):
    await state.update_data(dict([('wish', msg.text), ('is_input_name', 1)]))
    await msg.answer(text="Желание отредактировано",
                     reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_wish")


async def edit_name_message(msg: Message, state: FSMContext):
    await msg.answer(text="Введи имя", reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_name_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_name")


async def edit_address_message(msg: Message, state: FSMContext):
    await msg.answer(text="Введи адрес", reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_address_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_address")


async def edit_wish_message(msg: Message, state: FSMContext):
    await msg.answer(text="Введи желание",
                     reply_markup=get_edit_reply_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.edit_wish_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - edit_wish")


async def cancel_edit(msg: Message, state: FSMContext):
    await update_user(msg=msg, state=state)
    await msg.answer(text="Ожидай начала жеребьевки", reply_markup=get_wait_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(UserStateGroup.wait_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - cancel_edit")


def register_edit_handlers(dp: Dispatcher):
    dp.message.register(edit_user_message, F.text == 'Редактировать данные', UserStateGroup.wait_state)

    dp.message.register(edit_name_message, F.text == 'Имя', UserStateGroup.edit_state)
    dp.message.register(edit_name, UserStateGroup.edit_name_state)

    dp.message.register(edit_address_message, F.text == 'Адрес', UserStateGroup.edit_state)
    dp.message.register(edit_address, UserStateGroup.edit_address_state)

    dp.message.register(edit_wish_message, F.text == 'Желание', UserStateGroup.edit_state)
    dp.message.register(edit_wish, UserStateGroup.edit_wish_state)

    dp.message.register(cancel_edit, F.text == 'Применить', UserStateGroup.edit_state)
