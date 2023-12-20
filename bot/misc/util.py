from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.get import get_ward_data, get_ward_id, get_all_users
from bot.database.methods.update import update_user, update_ward


async def randomizer(msg: Message, state: FSMContext) -> None:

    users = await get_all_users()

    select = dict()

    iter = 0
    for user in users:
        pass

    # user_id = {item[0]}
    # is_distributed = {item[12]}
    #


    user_wish = await state.get_data()
    ward_id = await get_ward_id(msg.from_user.id, ward_id=user_wish.get('ward_id'))
    await get_ward_data(user_id=ward_id, state=state)
    await update_ward(ward_id, str(msg.from_user.id))
    await update_user(msg=msg, state=state)
    await msg.answer("Теперь напиши print")
