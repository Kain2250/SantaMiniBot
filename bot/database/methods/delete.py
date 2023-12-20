import sqlite3

from bot.misc import TgKeys
from aiogram.types import Message


async def delete_user(user_id: str, msg: Message) -> None:
    connection = sqlite3.connect(TgKeys.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
    await msg.answer(text="Пользователь удален", reply=False)
    connection.commit()
    connection.close()
