from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    langsmith_api_key: str
    langsmith_project: str = "pixelo-agency-bot"
    
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str | None = None

    postgres_url: str
    api_secret_key: str
    
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "openai/gpt-oss-120b"
    
    chroma_persists_dir: str = "./chroma_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()