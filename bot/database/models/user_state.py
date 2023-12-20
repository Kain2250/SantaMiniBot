from aiogram.fsm.state import StatesGroup, State


class UserStateGroup(StatesGroup):
    go_state = State()
    input_name_state = State()
    input_address_state = State()
    input_wish_state = State()
    info_state = State()
    wait_state = State()
    draw_state = State()
    delete_state = State()
    edit_state = State()
    edit_name_state = State()
    edit_address_state = State()
    edit_wish_state = State()
