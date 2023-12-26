import logging

from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.update import update_user
from bot.database.models.user_state import UserStateGroup
from bot.keyboards.reply import get_wait_keyboard


async def input_name_message(msg: Message, state: FSMContext):
    await state.update_data(dict([('user_name', msg.text), ('is_input_name', 1)]))

    await msg.answer(text="Теперь твоему отправителю нужно знать где ты живешь "
                          "(чтобы приехать и \"насрать\" под дверь, ха-ха, шутка!).\n"
                          "У любого получателя есть адрес и индекс ближайшей почты, так что пиши и не бойся😉\n"
                          "<u>Например:</u>\n"
                          "Печальная область, тоскливый район, город грусть, проспект разочарование, дом 13")
    await state.set_state(UserStateGroup.input_address_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - input_name_message")


async def input_address_message(msg: Message, state: FSMContext):
    await state.update_data(dict([('address', msg.text), ('is_input_address', 1)]))
    await msg.answer(text="Так, с личностью и проживанием закончили, далее у нас будут твои предпочтения "
                          "(ну не наглей, пожалуйста, айфон тебе все равно не подарят, выбирай бюджет до 3000р)\n"
                          "Ну или ты можешь скинуть артикулы с ВБ, жизнь упростишь и получишь, что хочешь👍\n"
                          "<u>Например:</u>\n"
                          "\t-Хочу получить носок, чтобы быть свободным\n"
                          "\t-Не хочу получать авадакедавру")

    await state.set_state(UserStateGroup.input_wish_state)
    logging.info(f"Текущий state = {await state.get_state()} Функция - input_address_message")


async def input_wish_message(msg: Message, state: FSMContext):
    await state.update_data(dict([('wish', msg.text), ('is_input_wish', 1)]))
    await state.set_state(UserStateGroup.wait_state)
    await update_user(user_id=msg.from_user.id, state=state)
    await msg.answer(text="Все, давай, короче жди подарочек от твоего Тайного Санты. "
                          "А мы в свою очередь хотим тебе пожелать увеличения твоего бюджета в этом году, "
                          "уменьшения нервов и большого счастья!\n"
                          "P.S.Мы всегда ждём тебя в гости, всегда будем рады. С любовью, твои Пажитновы❤",
                     reply_markup=get_wait_keyboard())
    logging.info(f"Текущий state = {await state.get_state()} Функция - input_wish_message")


def register_input_user_data_handlers(dp: Dispatcher):
    dp.message.register(input_name_message, UserStateGroup.input_name_state)
    dp.message.register(input_address_message, UserStateGroup.input_address_state)
    dp.message.register(input_wish_message, UserStateGroup.input_wish_state)
