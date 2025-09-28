from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from app.bot.ui import (
    start_kb,
    Reg_state,
    choose_gender_kb,
    Gender_CB,
    Activities_CB,
    get_activity_kb,
    confirm_kb,
    add_note_kb,
)
from app.database.queries import insert_user

reg_router = Router()


@reg_router.callback_query(F.data == "start_registration")
async def reg_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await state.set_state(Reg_state.name)
    await state.update_data(id_tg=callback.from_user.id)
    await callback.message.answer(text="Как я могу тебя называть?")


@reg_router.message(StateFilter(Reg_state.name))
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg_state.age)
    await message.answer(
        text=f"Приятно познакомиться, {message.text}.\nСколько тебе лет?"
    )


@reg_router.message(StateFilter(Reg_state.age))
async def reg_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Reg_state.gender)
    await message.answer(
        text=f"Отлично!\nУкажи, пожалуйста, свой пол нажатием на одну из кнопок.",
        reply_markup=choose_gender_kb,
    )


@reg_router.callback_query(StateFilter(Reg_state.gender) and Gender_CB.filter())
async def reg_start(
    callback: CallbackQuery, callback_data: Gender_CB, state: FSMContext
):
    await callback.answer()
    await state.update_data(gender=callback_data.gender)
    await state.set_state(Reg_state.activity)
    choose_activ_kb = get_activity_kb(Activities_CB())
    await callback.message.edit_text(
        text="Чем занимаешься?\nВыбери все, что подходит, нажав на кнопки ниже:",
        reply_markup=choose_activ_kb.as_markup(),
    )


@reg_router.callback_query(StateFilter(Reg_state.activity) and Activities_CB.filter())
async def reg_start(
    callback: CallbackQuery, callback_data: Activities_CB, state: FSMContext
):
    await callback.answer()
    await state.update_data(
        study=callback_data.study, work=callback_data.work, sport=callback_data.sport
    )
    choose_activ_kb = get_activity_kb(callback_data)
    await callback.message.edit_text(
        text="Чем занимаешься?\nВыбери все, что подходит, нажав на кнопки ниже:",
        reply_markup=choose_activ_kb.as_markup(),
    )


@reg_router.callback_query(F.data == "confirm_registration")
async def reg_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text(
        text=f"""
Подтвердите введенные данные: \n
<b>Имя</b>:    {data['name']}
<b>Возраст</b>:    {data['age']}
<b>Пол</b>:    {data['gender'].value}\n
Вид активности:\n
<b>Учеба</b>:    {'✅' if data['study'] else '❌'}\n
<b>Работа</b>:    {'✅' if data['work'] else '❌'}\n
<b>Спорт</b>:    {'✅' if data['sport'] else '❌'}\n""",
        reply_markup=confirm_kb,
        parse_mode="HTML",
    )


@reg_router.callback_query(F.data == "done_registration")
async def reg_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await insert_user(data)
    await callback.message.edit_text(
        text="Отлично, регистрация завершена!\nТеперь ты можешь вести дневник здоровья каждый день.\nДля этого нажми ниже на кнопку либо отправь в чат сообщение “Добавить запись”",
        reply_markup=add_note_kb,
    )


@reg_router.callback_query(F.data == "cancel_registration")
async def reg_start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text="Хорошо.\nДавай начнем с начала.", reply_markup=start_kb
    )
