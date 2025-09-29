from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from html import escape
from app.bot.ui import Note_state
from app.database.queries import (
    insert_note,
    get_activities_user,
    get_user_info,
    get_last_notes,
    insert_recom,
)
from app.ai.ai_manager import get_content_stream


note_router = Router()


@note_router.callback_query(F.data == "add_note")
async def add_note(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await state.set_state(Note_state.sleep)
    text = (
        f"Давай сделаем запись в дневник\!\n"
        "Сколько часов ты сегодня спал\nи как бы оценил качество сна по шкале от 1 до 10?\n"
        "Используй этот шаблон:\n\n"
        "```Шаблон\nКоличество часов:\nКачество:\n```"
    )

    await callback.message.answer(
        text=text,
        parse_mode="MarkdownV2",
    )


@note_router.message(Note_state.sleep)
async def add_sleep(message: Message, state: FSMContext):
    await state.update_data(sleep=message.text)
    await state.set_state(Note_state.food)
    text = (
        f"Что ты ел сегодня?\n\nИспользуй этот шаблон:\n"
        "```Шаблон\nЗавтрак: \nОбед: \nУжин: \nПерекусы: ```"
    )
    await message.answer(
        text=text,
        parse_mode="MarkdownV2",
    )


@note_router.message(Note_state.food)
async def add_food(message: Message, state: FSMContext):
    await state.update_data(food=message.text)
    await state.set_state(Note_state.mood)
    text = (
        f"Как ты себя чувствуешь?\nОцени самочувствие от 1 до 10\nи добавь комментарий\.\n\n"
        "Используй этот шаблон:"
        "```Шаблон\nНастроение:\nКомментарий:```"
    )
    await message.answer(
        text=text,
        parse_mode="MarkdownV2",
    )


@note_router.message(Note_state.mood)
async def add_mood(message: Message, state: FSMContext):
    await state.update_data(mood=message.text)
    await state.set_state(Note_state.activity)
    activities = await get_activities_user(message.from_user.id)
    template_lines = ""
    if activities[0]:
        template_lines += "Учёба: \n"
    if activities[1]:
        template_lines += "Работа: \n"
    if activities[2]:
        template_lines += "Спорт: \n"
    text = (
        f"Чем занимался сегодня?\n\nИспользуй этот шаблон:"
        f"```Шаблон\n{template_lines}Отдых: ```"
    )
    await message.answer(
        text=text,
        parse_mode="MarkdownV2",
    )


@note_router.message(Note_state.activity)
async def add_activity(message: Message, state: FSMContext):
    note = await state.get_data()
    note_id = await insert_note(
        message.from_user.id, note["sleep"], note["food"], note["mood"], message.text
    )
    await state.clear()
    text = "Запись сохранена! ✅\n" "Держи AI-рекомендацию для тебя на сегодня:\n"
    send_message = await message.answer(text=escape(text), parse_mode="HTML")
    await get_recommendation(send_message, 3, note_id)


@note_router.callback_query(F.data == "get_report_week")
async def get_report(callback: CallbackQuery):
    text = "Вот твой недельный отчёт по дневнику здоровья:\n"
    send_message = await callback.message.answer(text=escape(text), parse_mode="HTML")
    await get_recommendation(send_message, 7, None)


async def get_recommendation(message: Message, days: int, note_id: int):
    user = await get_user_info(message.chat.id)
    data = f"Информация о пользователе:\n - Имя: {user.name} - Возраст: {user.age}\n Записи пользователя:\n"
    last_notes = await get_last_notes(message.chat.id, days)
    for note in last_notes:
        data += (
            note[4].strftime("%d.%m.%y")
            + "\nСон:\n"
            + note[0]
            + "\nПитание:\n"
            + note[1]
            + "\nСамочувствие:\n"
            + note[2]
            + "\nАктивность:\n"
            + note[3]
            + "\n"
        )
    response = (message.text) + "\n\n"
    async for chunk in get_content_stream(data, days):
        response += escape(chunk.text)
        await message.edit_text(text=response, parse_mode="HTML")
    if not note_id is None:
        await insert_recom(note_id, response)
