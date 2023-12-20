from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.get import get_ward_data, get_ward_id
from bot.database.methods.update import update_user, update_ward


async def randomizer(msg: Message, state: FSMContext) -> None:
    user_wish = await state.get_data()
    ward_id = await get_ward_id(msg.from_user.id, user_wish=user_wish.get('wish'))
    await get_ward_data(user_id=ward_id, state=state)
    await update_ward(ward_id)
    await update_user(msg=msg, state=state)
    await msg.answer("Теперь напиши print")
