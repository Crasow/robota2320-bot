from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.builders import get_main_menu_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для поиска работы. Выберите действие:",
        reply_markup=get_main_menu_kb()
    )

@router.message(F.text == "🗑 Очистить историю")
async def clear_history(message: Message, state: FSMContext):
    await state.clear()
    
    # Пытаемся удалить последние сообщения (Telegram позволяет удалять сообщения не старше 48 часов)
    # Идем в обратном порядке от текущего ID сообщения
    current_msg_id = message.message_id
    
    # Формируем список ID последних 50 сообщений
    # Используем delete_messages для массового удаления (одним запросом)
    msg_ids = [msg_id for msg_id in range(current_msg_id, max(0, current_msg_id - 50), -1)]
    
    try:
        await message.bot.delete_messages(chat_id=message.chat.id, message_ids=msg_ids)
    except Exception:
        # Массовое удаление может не сработать, если сообщения слишком старые (старше 48ч)
        # В таком случае просто игнорируем ошибку
        pass
            
    await message.answer("История очищена. Выберите действие:", reply_markup=get_main_menu_kb())
