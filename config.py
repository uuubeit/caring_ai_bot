from dotenv import load_dotenv
from typing import Final
from pathlib import Path
import os

from app.utils.logger import logger


def require_env(key: str) -> str:
    v = os.getenv(key)
    if not v:
        logger.error(f"Required environment variable {key} is not set")
        raise RuntimeError(f"Required environment variable {key} is not set")
    return v


def get_prompt(path: str) -> str:
    prompt = Path(path).read_text(encoding="utf-8").strip()
    if not len(prompt):
        logger.error(f"The file {path} is empty")
        raise ValueError(f"The file {path} is empty")
    return prompt


load_dotenv()

TOKEN: Final[str] = require_env("BOT_TOKEN")
DB_PATH: Final[str] = require_env("DB_PATH")
GEMINI_TOKEN: Final[str] = require_env("GEMINI_TOKEN")
MODEL_GEMINI: Final[str] = require_env("MODEL_GEMINI")
THINKING_BUDGET: Final[int] = require_env("THINKING_BUDGET")
BASE_PROMPT = get_prompt("prompts/base_prompt.txt")
WEEK_PROMPT = get_prompt("prompts/week_prompt.txt")
