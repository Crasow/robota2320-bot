from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def get_main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🔎 Ищу работу"))
    builder.add(KeyboardButton(text="📢 Есть работа"))
    builder.add(KeyboardButton(text="🗑 Очистить историю"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_jobs_pagination_kb(page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if page > 1:
        builder.button(text="⬅️ Пред.", callback_data=f"jobs_page_{page-1}")
    
    builder.button(text=f"{page}/{total_pages}", callback_data="noop")
    
    if page < total_pages:
        builder.button(text="След. ➡️", callback_data=f"jobs_page_{page+1}")
        
    return builder.as_markup()
