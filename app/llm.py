from langchain_openai import ChatOpenAI

from app.core.config import settings

def get_llm():
    return ChatOpenAI(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
    )

    