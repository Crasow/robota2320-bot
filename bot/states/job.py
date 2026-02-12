from aiogram.fsm.state import StatesGroup, State

class JobCreationState(StatesGroup):
    description = State()
    start_time = State()
    deadline = State()
    payment = State()
    people_count = State()
    location = State()
