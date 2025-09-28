from google import genai
from google.genai import types

from config import GEMINI_TOKEN,BASE_PROMPT,WEEK_PROMPT


base_client=genai.client.BaseApiClient(api_key=GEMINI_TOKEN)
client = genai.client.AsyncClient(base_client)

async def get_content_steam(data: str,days:int):
    text = BASE_PROMPT+(WEEK_PROMPT if days >3 else '') + data
    stream=await client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=text,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=-1)
        )
    )
    async for chunk in stream:
        yield chunk