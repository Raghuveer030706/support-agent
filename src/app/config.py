from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    environment: str = "local"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
