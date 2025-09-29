from sqlalchemy import select

from app.database.database_manager import async_session_factory
from app.database.models import User, Note

from typing import Sequence

async def insert_recom(note_id: int, response: str):
    async with async_session_factory() as session:
        note = await session.get(Note, note_id)
        note.ai_recommendation = response
        await session.commit()


async def get_last_notes(user_id: int, limit_notes: int) -> Sequence:
    query = (
        select(
            Note.message_sleep,
            Note.message_food,
            Note.message_mood,
            Note.message_activity,
            Note.created_at,
        )
        .filter(Note.user_id_tg == user_id)
        .order_by(Note.created_at)
        .limit(limit_notes)
    )
    async with async_session_factory() as session:
        result = await session.execute(query)
        res = result.all()
        return res


async def check_user_id(user_id: int) -> bool:
    async with async_session_factory() as session:
        result = await session.get(User, user_id)
        return result is not None


async def get_user_info(user_id: int) -> User:
    async with async_session_factory() as session:
        return await session.get(User, user_id)


async def insert_user(user_data: dict):
    user = User(
        id_tg=user_data["id_tg"],
        name=user_data["name"],
        age=user_data["age"],
        gender=user_data["gender"].name,
        study=user_data["study"],
        work=user_data["work"],
        sport=user_data["sport"],
    )
    async with async_session_factory() as session:
        session.add(user)
        await session.commit()


async def get_activities_user(user_id: int) -> dict:
    query = select(User.study, User.work, User.sport).filter(User.id_tg == user_id)
    async with async_session_factory() as session:
        result = await session.execute(query)
        return result.all()[0]


async def insert_note(user_id: int, sleep: str, food: str, mood: str, activity: str) -> int:
    note = Note(
        user_id_tg=user_id,
        message_sleep=sleep,
        message_food=food,
        message_mood=mood,
        message_activity=activity,
    )
    async with async_session_factory() as session:
        session.add(note)
        await session.flush()
        note_id = note.id
        await session.commit()
        return note_id
