import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config import config
from bot.database.models import init_db
from bot.handlers import common, creating, looking

async def main():
    # Initialize DB
    await init_db()
    
    # Initialize Bot and Dispatcher
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(common.router)
    dp.include_router(looking.router)
    dp.include_router(creating.router)
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")