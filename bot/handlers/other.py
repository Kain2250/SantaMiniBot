import logging

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.create import create_user
from bot.database.methods.get import load_user, user_is_present
from bot.database.models.user_state import UserStateGroup
from bot.keyboards.reply import get_wait_keyboard


async def start_message(msg: Message, state: FSMContext):
    logging.info(f"Текущий state = {await state.get_state()} Функция - start_message if")

    if await user_is_present(user_id=msg.from_user.id):
        await load_user(user_id=msg.from_user.id, state=state)
        await msg.answer(text="Ожидай начала жеребьевки", reply_markup=get_wait_keyboard().as_markup())
        await state.set_state(UserStateGroup.wait_state)
        logging.info(f"Текущий state = {await state.get_state()} Функция - start_message if")
    else:
        await create_user(msg=msg, state=state)
        await msg.answer(text="Мы тут решили, что лучшее завершение этого года будут подарки от друзей 🥰\n"
                              "Но друзей у нас, оказывается, аж больше 2х человек, на всех денег, "
                              "короче, не напасешься. "
                              "Так что мы предлагаем поиграть в Тайного Санту.",
                         reply=False)
        await msg.answer(text="Введи свои ФИО, чтобы Санта знал кому он дарит подарок")
        await state.set_state(UserStateGroup.input_name_state)
        logging.info(f"Текущий state = {await state.get_state()} Функция - start_message else")


def register_other_handlers(dp: Dispatcher) -> None:
    dp.message.register(start_message, Command(commands="start"))
