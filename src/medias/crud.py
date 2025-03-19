from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.medias.models import Media


async def get_medias_by_ids(
    tweet_media_ids: List[int], session: AsyncSession
) -> List[Media]:
    stmt = select(Media).where(Media.id.in_(tweet_media_ids))
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_media(file_url: str, session: AsyncSession) -> Media:
    media_instance = Media(url=file_url, tweet_id=None)
    session.add(media_instance)
    await session.commit()
    await session.refresh(media_instance)
    return media_instance
