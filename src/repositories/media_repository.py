from typing import List, Optional
from sqlalchemy import select
from src.models.media_model import Media
from src.schemas.media_schema import MediaCreate, MediaUpdate  # Предположим, они уже определены
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from src.config.database.db_helper import db_helper

class MediaRepository(SqlAlchemyRepository[Media, MediaCreate, MediaUpdate]):
    async def get_medias_by_ids(self, media_ids: List[int]) -> List[Media]:
        async with self._session_factory() as session:
            stmt = select(self.model).where(self.model.id.in_(media_ids))
            result = await session.execute(stmt)
            return result.scalars().all()

# Создаем экземпляр репозитория для модели Media.
media_repository = MediaRepository(model=Media, db_session=db_helper.get_db_session)

# from typing import List
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from src.medias.models import Media


# async def get_medias_by_ids(
#     tweet_media_ids: List[int], session: AsyncSession
# ) -> List[Media]:
#     stmt = select(Media).where(Media.id.in_(tweet_media_ids))
#     result = await session.execute(stmt)
#     return result.scalars().all()


# async def create_media(file_url: str, session: AsyncSession) -> Media:
#     media_instance = Media(url=file_url, tweet_id=None)
#     session.add(media_instance)
#     await session.commit()
#     await session.refresh(media_instance)
#     return media_instance
