from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage  
from app.bot.handlers.main_handlers import main_router
from app.bot.handlers.registration_handlers import reg_router
from app.bot.handlers.note_handlers import note_router
from app.utils.logger import logger
from config import TOKEN


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

dp.include_router(main_router)
dp.include_router(reg_router)
dp.include_router(note_router)

async def bot_main():
    try:
        logger.info("The bot is running...")
        await dp.start_polling(bot, skip_updates=True)
    finally:
        logger.info("The bot session is closed")
        await bot.session.close()
        await storage.close()
