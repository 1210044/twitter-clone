from pathlib import Path

STATIC_DIR = Path("static")
MEDIA_DIR = Path("media")
TWEETS_MEDIA_DIR = MEDIA_DIR / "tweets"


# # config.py
# from pydantic import BaseSettings
# from pathlib import Path

# class Settings(BaseSettings):
#     upload_directory: Path = Path(‘app/media’)

#     class Config:
#         env_file = “.env”  # Опционально, для работы с переменными окружения

# settings = Settings()
