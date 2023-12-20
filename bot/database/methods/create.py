import sqlite3

from aiogram.fsm.context import FSMContext

from bot.misc import TgKeys
from aiogram.types import Message


def create_table_users() -> None:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    default_user_first_name TEXT,
    default_user_last_name TEXT,
    user_name TEXT,
    address TEXT,
    wish TEXT,
    ward_id INTEGER,
    ward_name TEXT,
    ward_address TEXT,
    ward_wish TEXT,
    is_input_name INTEGER,
    is_input_address INTEGER,
    is_input_wish INTEGER,
    is_distributed INTEGER,
    is_register INTEGER
    )
    ''')

    connection.commit()
    connection.close()


async def create_user(msg: Message, state: FSMContext) -> None:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users WHERE user_id = ?', (msg.from_user.id,)).fetchone()

    if not results:
        await state.update_data(dict([
            ('user_id', msg.from_user.id),
            ('default_user_first_name', msg.from_user.first_name if (msg.from_user.first_name is not None) else ''),
            ('default_user_last_name', msg.from_user.last_name if (msg.from_user.last_name is not None) else ''),
            ('user_name', ''),
            ('address', ''),
            ('wish', ''),
            ('ward_id', 0),
            ('ward_name', ''),
            ('ward_address', ''),
            ('ward_wish', ''),
            ('is_input_name', 0),
            ('is_input_address', 0),
            ('is_input_wish', 0),
            ('is_distributed', 0),
            ('is_register', 1)])
        )

        cursor.execute('''INSERT INTO Users (
        user_id,
        default_user_first_name,
        default_user_last_name,
        user_name,
        address,
        wish,
        ward_id,
        ward_name,
        ward_address,
        ward_wish,
        is_input_name,
        is_input_address,
        is_input_wish,
        is_distributed,
        is_register
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
            msg.from_user.id,
            msg.from_user.first_name,
            msg.from_user.last_name,
            '',
            '',
            '',
            0,
            '',
            '',
            '',
            0,
            0,
            0,
            0,
            1))

        connection.commit()
        connection.close()
