from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from bot.database.models import async_session, Job
from bot.states.job import JobCreationState
from bot.keyboards.builders import get_main_menu_kb

router = Router()

@router.message(F.text == "📢 Есть работа")
async def start_job_creation(message: Message, state: FSMContext):
    await state.set_state(JobCreationState.description)
    await message.answer("Опишите работу (кратко):")

@router.message(JobCreationState.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(JobCreationState.payment)
    await message.answer("Сколько платите?")

@router.message(JobCreationState.payment)
async def process_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)
    await state.set_state(JobCreationState.time_required)
    await message.answer("Когда нужно выполнить работу?")

@router.message(JobCreationState.time_required)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time_required=message.text)
    await state.set_state(JobCreationState.people_count)
    await message.answer("Сколько человек нужно? (введите число)")

@router.message(JobCreationState.people_count)
async def process_people_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
        
    data = await state.get_data()
    async with async_session() as session:
        new_job = Job(
            description=data['description'],
            payment=data['payment'],
            time_required=data['time_required'],
            people_count=int(message.text)
        )
        session.add(new_job)
        await session.commit()
        
    await state.clear()
    await message.answer("Вакансия успешно сохранена!", reply_markup=get_main_menu_kb())
