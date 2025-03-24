from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str
    STATIC_DIR: str
    MEDIA_DIR: str
    TWEETS_MEDIA_DIR: str


settings = Settings()
