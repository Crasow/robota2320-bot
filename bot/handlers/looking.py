from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func
from bot.database.models import async_session, Job

router = Router()

ITEMS_PER_PAGE = 10

async def get_jobs_page(page: int):
    offset = (page - 1) * ITEMS_PER_PAGE
    async with async_session() as session:
        # Get total count
        result = await session.execute(select(func.count()).select_from(Job))
        total_items = result.scalar()
        
        # Get jobs for current page
        stmt = select(Job).offset(offset).limit(ITEMS_PER_PAGE)
        result = await session.execute(stmt)
        jobs = result.scalars().all()
        
    return jobs, total_items

def format_jobs(jobs, start_index=1):
    if not jobs:
        return "Нет доступных вакансий."
        
    text = "📋 *Список вакансий:*\n\n"
    for i, job in enumerate(jobs, start_index):
        text += (
            f"🔹 *Вакансия #{i} (ID: {job.id})*\n"
            f"📝 {job.description}\n"
            f"📅 Старт: {job.start_time}\n"
            f"⌛ Срок: {job.deadline}\n"
            f"💰 Оплата: {job.payment}\n"
            f"👥 Требуется: {job.people_count} чел.\n"
            f"📍 Локация: {job.location}\n"
            f"{'-'*20}\n"
        )
    return text

def get_pagination_kb(page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"jobs_page_{page-1}")
    
    builder.button(text=f"{page}/{total_pages}", callback_data="noop")
    
    if page < total_pages:
        builder.button(text="Вперед ➡️", callback_data=f"jobs_page_{page+1}")
    return builder.as_markup()

@router.message(F.text == "🔎 Ищу работу")
async def show_jobs(message: Message, state: FSMContext):
    await state.clear()
    jobs, total_items = await get_jobs_page(1)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    text = format_jobs(jobs, start_index=1)
    kb = get_pagination_kb(1, total_pages) if total_pages > 1 else None
    
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data.startswith("jobs_page_"))
async def paginate_jobs(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    jobs, total_items = await get_jobs_page(page)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    start_index = (page - 1) * ITEMS_PER_PAGE + 1
    text = format_jobs(jobs, start_index=start_index)
    kb = get_pagination_kb(page, total_pages) if total_pages > 1 else None
    
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception:
        await callback.answer()