from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()


class Notification(StatesGroup):
    description = State()
    date = State()
    is_periodic = State()
