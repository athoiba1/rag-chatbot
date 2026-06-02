from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "RAG Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    UPLOAD_DIR: Path = Path("data/uploads")
    VECTORSTORE_DIR: Path = Path("data/vectorstore")

    OPENAI_API_KEY: str = Field(default="")
    LLM_MODEL: str = Field(default="gpt-4o-mini")
    LLM_TEMPERATURE: float = Field(default=0.3, ge=0.0, le=2.0)
    LLM_MAX_TOKENS: int = Field(default=2048, ge=1, le=128000)

    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small")
    EMBEDDING_DIMENSIONS: int = Field(default=1536)

    CHUNK_SIZE: int = Field(default=1000, ge=100, le=10000)
    CHUNK_OVERLAP: int = Field(default=200, ge=0, le=5000)

    TOP_K: int = Field(default=4, ge=1, le=20)
    SIMILARITY_THRESHOLD: float = Field(default=0.3, ge=0.0, le=1.0)

    CORS_ORIGINS: list[str] = ["*"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
