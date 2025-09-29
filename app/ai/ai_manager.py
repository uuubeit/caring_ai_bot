from google import genai
from google.genai import types
from tenacity import (
    AsyncRetrying,
    stop_after_attempt,
    retry_if_exception,
    wait_exponential,
)
from typing import AsyncIterator

from config import GEMINI_TOKEN, MODEL_GEMINI, THINKING_BUDGET, BASE_PROMPT, WEEK_PROMPT


base_client = genai.client.BaseApiClient(api_key=GEMINI_TOKEN)
client = genai.client.AsyncClient(base_client)


async def get_content_stream(
    data: str, days: int
) -> AsyncIterator[types.GenerateContentResponse]:
    text = BASE_PROMPT + (WEEK_PROMPT if days > 3 else "") + data

    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=15),
        retry=retry_if_exception(Exception),
        reraise=True,
    ):
        with attempt:
            stream = await client.models.generate_content_stream(
                model=MODEL_GEMINI,
                contents=text,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=THINKING_BUDGET
                    )
                ),
            )
        async for chunk in stream:
            yield chunk
