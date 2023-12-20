import sqlite3

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.misc import TgKeys


async def update_user(msg: Message, state: FSMContext) -> None:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    data = await state.get_data()
    cursor.execute('''UPDATE Users SET
        user_name = ?,
        address = ?,
        wish = ?,
        ward_id = ?,
        ward_name = ?,
        ward_address = ?,
        ward_wish = ?,
        is_input_name = ?,
        is_input_address = ?,
        is_input_wish = ?,
        is_register = ?
        WHERE user_id = ?
        ''', (
        data.get('user_name'),
        data.get('address'),
        data.get('wish'),
        data.get('ward_id'),
        data.get('ward_name') if (data.get('ward_name') is not None) else '',
        data.get('ward_address') if (data.get('ward_address') is not None) else '',
        data.get('ward_wish') if (data.get('ward_wish') is not None) else '',
        data.get('is_input_name'),
        data.get('is_input_address'),
        data.get('is_input_wish'),
        data.get('is_register'),
        msg.from_user.id))

    connection.commit()
    connection.close()


async def update_ward(ward_id: str, user_id: str) -> None:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''UPDATE Users SET
            is_distributed = 1,
            ward_id = ?
            WHERE user_id = ?
            ''', (ward_id, user_id))

    connection.commit()
    connection.close()
