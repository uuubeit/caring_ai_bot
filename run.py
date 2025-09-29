import asyncio
from app.bot.bot_runner import bot_main
from app.database.database_manager import start_db
from app.utils.logger import logger


async def main():
    await start_db()
    await bot_main()


if __name__ == "__main__":
    asyncio.run(main())
