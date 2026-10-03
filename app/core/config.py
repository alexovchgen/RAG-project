from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки сервиса. Читаются из переменных окружения и из .env файла"""

    model_config = SettingsConfigDict(
        env_file=".env",
         env_file_encoding="utf-8",
         extra="ignore")
    
    llm_api_key: str | None = None

    llm_base_url: str = "https://api.vsellm.ru/v1"
    llm_model: str = "qwen/qwen3.7-flash"
    llm_temperature: float = 0.0

    # Vector store
    qdrant_url: str = "http://qdrant:6333"
    collection_name: str = "sklearn_docs"
    top_k: int = 4

    # Embeddings (e5 — мультиязычный, нужно для русского)
    embedding_model: str = "intfloat/multilingual-e5-small"
    embedding_dim: int = 384
    normalize_embeddings: bool = True

    # Настройки сервиса
    app_name: str = "Rag servise"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    debug: bool = False


settings = Settings()