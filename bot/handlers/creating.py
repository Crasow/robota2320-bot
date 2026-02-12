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
    await state.set_state(JobCreationState.start_time)
    await message.answer("Когда приступить к работе?")

@router.message(JobCreationState.start_time)
async def process_start_time(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    await state.set_state(JobCreationState.deadline)
    await message.answer("Сроки выполнения?")

@router.message(JobCreationState.deadline)
async def process_deadline(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await state.set_state(JobCreationState.payment)
    await message.answer("Какой бюджет на работу?")

@router.message(JobCreationState.payment)
async def process_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)
    await state.set_state(JobCreationState.people_count)
    await message.answer("Сколько человек нужно? (введите число)")

@router.message(JobCreationState.people_count)
async def process_people_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
        
    await state.update_data(people_count=int(message.text))
    await state.set_state(JobCreationState.location)
    await message.answer("Адресс работы?")

@router.message(JobCreationState.location)
async def process_location(message: Message, state: FSMContext):
    data = await state.get_data()
    async with async_session() as session:
        new_job = Job(
            description=data['description'],
            start_time=data['start_time'],
            deadline=data['deadline'],
            payment=data['payment'],
            people_count=data['people_count'],
            location=message.text
        )
        session.add(new_job)
        await session.commit()
        
    await state.clear()
    await message.answer("Вакансия успешно сохранена!", reply_markup=get_main_menu_kb())
