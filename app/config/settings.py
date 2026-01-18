from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    CHUNK_SIZE: int = Field(default=1000)
    CHUNK_OVERLAP: int = Field(default=200)

    # Embedding Settings
    GEMINI_API_KEY: SecretStr = SecretStr("gemini_api_key")
    EMBEDDING_MODEL_NAME: str = Field(default="gemini-embedding-001")

    # LLM Settings
    GROQ_API_KEY: SecretStr = SecretStr("groq_api_key")
    GROQ_LLM_MODEL_NAME: str = Field(default="meta-llama/llama-4-scout-17b-16e-instruct")
    GEMINI_LLM_MODEL_NAME: str = Field(default="gemini-3-flash-preview")

    # Milvus Settings
    MILVUS_URI: str = Field(default="http://localhost:19530")
    MILVUS_TOKEN: str = Field(default="")
    MILVUS_COLLECTION_NAME: str = Field(default="slide_source_mapping")
    MILVUS_EMBEDDING_DIM: int = Field(default=3072)
    MILVUS_BATCH_SIZE: int = Field(default=50)


settings = Settings()
