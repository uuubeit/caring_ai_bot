from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

import re
import enum
from dataclasses import field


class Gender(enum.Enum):
    male = "Мужской"
    female = "Женский"


class Reg_state(StatesGroup):
    name = State()
    age = State()
    gender = State()
    activity = State()

class Note_state(StatesGroup):
    sleep=State()
    food=State()
    mood=State()
    activity=State()
    



class Gender_CB(CallbackData, prefix="gender_"):
    gender: Gender


class Activities_CB(CallbackData, prefix="activity_"):
    study: bool = field(default=False)
    work: bool = field(default=False)
    sport: bool = field(default=False)


start_kb=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать регистрацию", callback_data="start_registration")]
])

add_note_kb=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить запись", callback_data="add_note")]
])
menu_kb=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить новую запись", callback_data="add_note")],
    [InlineKeyboardButton(text="Посмотреть прошлые записи", callback_data="view_past_note")],
    [InlineKeyboardButton(text="Получить AI-отчёт за неделю", callback_data="get_report_week")]
])

choose_gender_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Мужской", callback_data=Gender_CB(gender=Gender.male).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Женский", callback_data=Gender_CB(gender=Gender.female).pack()
            )
        ],
    ]
)


def get_activity_kb(data: Activities_CB) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=f"Учеба  {'✅' if data.study else '❌'}",
        callback_data=Activities_CB(
            study=not data.study, work=data.work, sport=data.sport
        ).pack(),
    )
    kb.button(
        text=f"Работа {'✅' if data.work else '❌'}",
        callback_data=Activities_CB(
            study=data.study, work=not data.work, sport=data.sport
        ).pack(),
    )
    kb.button(
        text=f"Спорт  {'✅' if data.sport else '❌'}",
        callback_data=Activities_CB(
            study=data.study, work=data.work, sport=not data.sport
        ).pack(),
    )
    kb.button(text="Готово", callback_data="confirm_registration")
    kb.adjust(1)
    return kb


confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="done_registration")],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_registration")],
    ]
)

def escape_md(text: str) -> str:
    """
    Экранирует все спецсимволы для MarkdownV2
    """
    # список спецсимволов MarkdownV2, которые нужно экранировать
    symbols = r"_*[]()~`>#+-=|{}.!$"
    return re.sub(f"([{re.escape(symbols)}])", r"\\\1", text)