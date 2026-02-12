from aiogram.fsm.state import StatesGroup, State

class JobCreationState(StatesGroup):
    description = State()
    payment = State()
    time_required = State()
    people_count = State()
