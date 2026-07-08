from langchain_groq import ChatGroq
from app.core.config import settings

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
