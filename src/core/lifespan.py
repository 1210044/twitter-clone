from shutil import rmtree
from contextlib import asynccontextmanager

from src.config.project_config import settings
from src.core.logger import logger
from src.models.base_model import Base
from src.config.database.db_helper import db_helper
from src.config.database.db_generate_data import create_data


# @asynccontextmanager
# async def lifespan(app):
#     async with db_helper.engine.begin() as conn:
#         logger.info("Dropping table...")
#         await conn.run_sync(Base.metadata.drop_all)
#         logger.info("Creating tables...")
#         await conn.run_sync(Base.metadata.create_all)
#         logger.info("Deleted media director...")
#         rmtree(settings.TWEETS_MEDIA_DIR, ignore_errors=True)
#         logger.info("Created media director...")
#         settings.TWEETS_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
#     logger.info("Created data...")
#     await create_data()
#     yield
#     await db_helper.engine.dispose()