from dotenv import load_dotenv
import os
load_dotenv()

TOKEN=os.getenv("BOT_TOKEN")
DB_PATH=os.getenv("DB_PATH")
GEMINI_TOKEN=os.getenv("GEMINI_TOKEN")
BASE_PROMPT=os.getenv("BASE_PROMPT")
WEEK_PROMPT=os.getenv("WEEK_PROMPT")