import logging

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.create import create_user
from bot.database.methods.get import load_user, user_is_present, is_draft
from bot.database.models.user_state import UserStateGroup
from bot.keyboards.reply import get_wait_keyboard, get_draw_keyboard


async def start_message(msg: Message, state: FSMContext):
    logging.info(f"Текущий state = {await state.get_state()} Функция - start_message")

    if await user_is_present(user_id=msg.from_user.id):
        if await is_draft():
            await state.set_state(UserStateGroup.draw_state)
            await load_user(user_id=msg.from_user.id, state=state)
            await msg.answer(text="Поздравляю! Санта уже ищет твой подарок и в скором времени тебе сообщит",
                             reply_markup=get_draw_keyboard())
            logging.info(f"Текущий state = {await state.get_state()} Функция - start_message_draw")
        else:
            await load_user(user_id=msg.from_user.id, state=state)
            await msg.answer(text="Ожидай начала жеребьевки",
                             reply_markup=get_wait_keyboard())
            await state.set_state(UserStateGroup.wait_state)
            logging.info(f"Текущий state = {await state.get_state()} Функция - start_message if")
    elif is_draft():
        await msg.answer("К сожалению время на регистрацию закончилось... Увы в этом году без тайного Санты")
    else:
        await create_user(msg=msg, state=state)
        await msg.answer(text="Мы тут решили, что лучшее завершение этого года будут подарки от друзей 🥰\n"
                              "Но друзей у нас, оказывается, аж больше 2х человек, на всех денег, "
                              "короче, не напасешься. "
                              "Так что мы предлагаем поиграть в Тайного Санту.")
        await msg.answer(
            text="Каждая посылка имеет своего адресата. Тебе необходимо написать свое <b>ФИО</b>, "
                 "чтобы твой Санта знал кому отправлять.")
        await state.set_state(UserStateGroup.input_name_state)
        logging.info(f"Текущий state = {await state.get_state()} Функция - start_message else")


def register_other_handlers(dp: Dispatcher) -> None:
    dp.message.register(start_message, Command(commands="start"))
