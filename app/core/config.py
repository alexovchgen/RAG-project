from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


def resolve_qdrant_url(url: str) -> str:
    """Имя сервиса qdrant есть только в Docker-сети. Jupyter/Windows — localhost."""
    in_docker = Path("/.dockerenv").exists()
    if not in_docker and "://qdrant:" in (url or ""):
        return "http://localhost:6333"
    return url


class Settings(BaseSettings):
    """Настройки сервиса. Читаются из переменных окружения и из .env файла"""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE if _ENV_FILE.is_file() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_api_key: str | None = None

    llm_base_url: str = "https://api.vsellm.ru/v1"
    llm_model: str = "qwen/qwen3.7-flash"
    llm_temperature: float = 0.0

    # С хоста (Jupyter) — localhost; compose/deploy задают http://qdrant:6333
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "sklearn_docs"
    top_k: int = 4

    embedding_model: str = "intfloat/multilingual-e5-small"
    embedding_dim: int = 384
    normalize_embeddings: bool = True

    app_name: str = "Rag servise"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    debug: bool = False

    @model_validator(mode="after")
    def qdrant_url_outside_docker(self):
        fixed = resolve_qdrant_url(self.qdrant_url)
        if fixed != self.qdrant_url:
            return self.model_copy(update={"qdrant_url": fixed})
        return self


settings = Settings()
