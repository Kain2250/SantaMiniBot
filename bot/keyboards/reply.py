from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_wait_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Редактировать данные'),
        KeyboardButton(text='Отказаться от участия')
    )
    builder.adjust(2)
    return builder


def get_draw_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Кому я дарю'),
        KeyboardButton(text='Подарок отправлен')
    )
    builder.adjust(2)
    return builder


def get_edit_reply_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Имя'),
        KeyboardButton(text='Адрес'),
        KeyboardButton(text='Желание'),
        KeyboardButton(text='Применить')
    )
    builder.adjust(3)

    return builder
