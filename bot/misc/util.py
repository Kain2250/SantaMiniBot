from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.methods.get import get_all_users, draw_ward, load_user
from bot.database.methods.update import update_ward_is_distributed, update_user
from bot.database.models.user_state import UserStateGroup
from bot.keyboards.reply import get_draw_keyboard


async def randomizer(msg: Message, state: FSMContext, bot: Bot) -> None:
    users = await get_all_users()

    if users[0][13] != 1:
        await load_user(user_id=users[-1][0], state=state)
        ward_id = await draw_ward(user_id=users[-1][0], state=state)
        if ward_id != 'none':
            await update_ward_is_distributed(ward_id=ward_id)
            await bot.send_message(chat_id=ward_id,
                                   text="Жеребьевка прошла, скорее смотри кому ты даришь",
                                   reply_markup=get_draw_keyboard())
        await update_user(user_id=users[-1][0], state=state)

        for item in users:
            await load_user(user_id=item[0], state=state)
            ward_id = await draw_ward(user_id=item[0], state=state)
            if ward_id != 'none':
                await update_ward_is_distributed(ward_id=ward_id)
                await bot.send_message(chat_id=ward_id,
                                       text="Жеребьевка прошла, скорее смотри кому ты даришь",
                                       reply_markup=get_draw_keyboard())
            await update_user(user_id=item[0], state=state)

        await load_user(user_id=msg.from_user.id, state=state)
        await state.set_state(UserStateGroup.draw_state)
    else:
        await state.set_state(UserStateGroup.draw_state)
        await msg.answer("Пользователи уже распределены", reply_markup=get_draw_keyboard())
