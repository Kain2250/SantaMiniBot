from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_edit_inline_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Имя', callback_data='edit_name_button'),
        InlineKeyboardButton(text='Адрес', callback_data='edit_address_button'),
        InlineKeyboardButton(text='Предпочтения', callback_data='edit_wish_button')
    )

    return builder
