from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from app.bot.ui import start_kb,menu_kb
from app.database.queries import get_user_info


main_router = Router()

@main_router.message(Command("menu"))
async def menu(message:Message):
    user = await get_user_info(message.from_user.id)
    if user:
        await message.answer(text=(f"Привет, {user.name}! 🌿\n"\
        "Это твоё главное меню. Здесь ты можешь управлять своим дневником здоровья.\n\n"\
        "Используй кнопки ниже, чтобы перейти к нужному разделу.\n"\
        "Продолжай вести дневник — это поможет улучшать самочувствие и настроение! 💛"),
        reply_markup=menu_kb)
    else:
        await message.answer(
            text="Привет!\nЯ твой AI-помощник для здоровья.\nДавай начнем с регистрации.",
            reply_markup=start_kb,
        )


@main_router.message(Command("start"))
async def start_func(message: Message):
    user = await get_user_info(message.from_user.id)
    if user:
        await message.answer(text=(f"Привет снова, {user.name}! 👋\n"\
            "Я вижу, что ты уже зарегистрирован в системе.\n\n"\
            "Ты можешь:\n"\
            "\n✅ Добавить новую запись в дневник\n"\
            "\n✅ Посмотреть предыдущие записи \n"\
            "\n✅ Получить рекомендации от AI за день или неделю \n\n"\
            "Чтобы продолжить, используй команду /menu и выбери нужное действие.\n"\
            "Продолжай вести дневник — это отличный способ следить за своим самочувствием! 💛\n")
        )
    else:
        await message.answer(
            text="Привет!\nЯ твой AI-помощник для здоровья.\nДавай начнем с регистрации.",
            reply_markup=start_kb,
        )
