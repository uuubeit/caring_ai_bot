from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import SMALLINT
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import ForeignKey,text,Index

import enum
import datetime

class Gender(enum.Enum):
    male="male"
    female="female"

class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__='users'

    id_tg:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]
    age:Mapped[int]=mapped_column(SMALLINT)
    gender:Mapped[Gender]
    study:Mapped[bool]
    work:Mapped[bool]
    sport:Mapped[bool]


class Note(Base):
    __tablename__='notes'

    id:Mapped[int]=mapped_column(primary_key=True)
    user_id_tg:Mapped[int]=mapped_column(ForeignKey('users.id_tg',ondelete='CASCADE'))
    message_sleep:Mapped[str]
    message_food:Mapped[str]
    message_mood:Mapped[str]
    message_activity:Mapped[str]
    ai_recommendation:Mapped[str]=mapped_column(nullable=True)
    created_at:Mapped[datetime.datetime]=mapped_column(server_default=text("DATETIME('now', '+3 hours')"))

    __table_args__=(
        Index("user_id_index","user_id_tg"),
    )
