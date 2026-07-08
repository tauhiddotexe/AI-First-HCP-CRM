import logging
from langchain_groq import ChatGroq
from groq import RateLimitError
from app.core.config import settings

logger = logging.getLogger('uvicorn.error')

GROQ_MODEL = 'llama-3.3-70b-versatile'
FALLBACK_MODEL = 'llama-3.1-8b-instant'


def get_llm() -> ChatGroq:
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.1,
        max_tokens=1024,
    )


def get_fallback_llm() -> ChatGroq:
    return ChatGroq(
        model=FALLBACK_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.1,
        max_tokens=1024,
    )


async def ainvoke_with_fallback(messages: list):
    try:
        return await get_llm().ainvoke(messages)
    except RateLimitError:
        logger.warning('Primary model rate limited, falling back to %s', FALLBACK_MODEL)
        return await get_fallback_llm().ainvoke(messages)
