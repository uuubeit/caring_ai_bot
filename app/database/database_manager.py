from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app.database.models import Base
from app.utils.logger import logger
from config import DB_PATH


engine =create_async_engine("sqlite+aiosqlite:///"+DB_PATH)
async_session_factory=async_sessionmaker(engine)

async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("The database is prepared.")

@event.listens_for(Engine,"connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()