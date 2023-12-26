from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_wait_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Редактировать данные'),
        KeyboardButton(text='Отказаться от участия')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_draw_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Кому я дарю'),
        KeyboardButton(text='Подарок отправлен')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_edit_reply_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Имя'),
        KeyboardButton(text='Адрес'),
        KeyboardButton(text='Желание'),
        KeyboardButton(text='Применить')
    )
    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True)
