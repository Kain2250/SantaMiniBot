import sqlite3

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.misc import TgKeys


async def user_is_present(user_id: int) -> bool:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    cursor.close()

    return results is not None


async def is_draft() -> bool:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT is_distributed FROM Users').fetchone()

    if results:
        for item in results:
            if item == 0:
                return False
        return True

    return False


async def load_user(user_id: int, state: FSMContext) -> bool:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()

    if results:
        await state.set_data(
            dict([('user_id', results[0]),
                  ('default_user_first_name', results[1]),
                  ('default_user_last_name', results[2]),
                  ('user_name', results[3]),
                  ('address', results[4]),
                  ('wish', results[5]),
                  ('ward_id', results[6]),
                  ('ward_name', results[7]),
                  ('ward_address', results[8]),
                  ('ward_wish', results[9]),
                  ('is_input_name', results[10]),
                  ('is_input_address', results[11]),
                  ('is_input_wish', results[12]),
                  ('is_distributed', results[13]),
                  ('is_register', results[14])
                  ])
        )

        connection.close()
    return results is not None


async def print_ward_data(user_id: int, state: FSMContext):
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    results = cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()

    if results:
        await state.update_data(
            dict([('ward_id', results[6]),
                  ('ward_name', results[3]),
                  ('ward_address', results[4]),
                  ('ward_wish', results[5])
                  ])
        )

    connection.close()


async def get_ward_id(user_id: int, ward_id: str) -> str:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    results = cursor.execute('SELECT user_id FROM Users WHERE user_id != ? and is_distributed != 1 and ward_id != ?',
                             (user_id, ward_id)).fetchone()

    ret = "None"
    if results:
        ret = str(results[0])

    connection.close()

    return ret


async def draw_ward(user_id: int, state: FSMContext) -> str:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    results = cursor.execute(
        'SELECT * FROM Users WHERE user_id != ? and is_distributed != 1 and ward_id != ?',
        (user_id, user_id)).fetchone()

    if results:
        await state.update_data(
            dict([('ward_id', results[0]),
                  ('ward_name', results[3]),
                  ('ward_address', results[4]),
                  ('ward_wish', results[5])
                  ])
        )

    connection.close()

    return results[0] if results else 'none'


async def adm_print_user(user_id: int, state: FSMContext, msg: Message):
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()

    if results:
        data = await state.get_data()
        await msg.answer(text=f"user_id = {data.get('user_id')}\n"
                              f"default_user_first_name = {data.get('default_user_first_name')}\n"
                              f"default_user_last_name = {data.get('default_user_last_name')}\n"
                              f"user_name = {data.get('user_name')}\n"
                              f"address = {data.get('address')}\n"
                              f"wish = {data.get('wish')}\n"
                              f"ward_id = {data.get('ward_id')}\n"
                              f"ward_name = {data.get('ward_name')}\n"
                              f"ward_address = {data.get('ward_address')}\n"
                              f"ward_wish = {data.get('ward_wish')}\n"
                              f"is_input_name = {data.get('is_input_name')}\n"
                              f"is_input_address = {data.get('is_input_address')}\n"
                              f"is_input_wish = {data.get('is_input_wish')}\n"
                              f"is_distributed = {data.get('is_distributed')}\n"
                              f"is_register = {data.get('is_register')}\n\n"
                         )

    connection.close()


async def adm_print_all_user(msg: Message):
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users').fetchall()

    if results:
        message = ""
        for item in results:
            message += f"user_id = {item[0]}\n" \
                       f"default_user_first_name = {item[1]}\n" \
                       f"default_user_last_name = {item[2]}\n" \
                       f"user_name = {item[3]}\n" \
                       f"address = {item[4]}\n" \
                       f"wish = {item[5]}\n" \
                       f"ward_id = {item[6]}\n" \
                       f"ward_name = {item[7]}\n" \
                       f"ward_address = {item[8]}\n" \
                       f"ward_wish = {item[9]}\n" \
                       f"is_input_name = {item[10]}\n" \
                       f"is_input_address = {item[11]}\n" \
                       f"is_input_wish = {item[12]}\n" \
                       f"is_distributed = {item[13]}\n" \
                       f"is_register = {item[14]}\n\n"

        await msg.answer(text=message)

    connection.close()


async def get_all_users() -> list:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users').fetchall()
    connection.close()

    return results


async def get_user(user_id: int) -> list:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()
    results = cursor.execute('SELECT * FROM Users WHERE user_id == ?', (user_id,)).fetchone()
    connection.close()

    return results
