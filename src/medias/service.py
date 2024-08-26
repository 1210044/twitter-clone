from typing import List
from asyncio import gather
from aiofiles import open as aio_open
from aiofiles.os import path as aio_path, remove as aio_remove
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.medias.models import Media


async def write_file(file_url: Path, file: UploadFile) -> None:
    async with aio_open(file_url, 'wb') as f:
        file_content = await file.read()
        await f.write(file_content)


async def delete_file(file_url: str) -> None:
    path = Path(file_url)
    if await aio_path.exists(path):
        await aio_remove(file_url)


async def get_medias_by_ids(tweet_media_ids: List[int], session: AsyncSession) -> List:
    stmt = select(Media).where(Media.id.in_(tweet_media_ids))
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_media(file_url: str, session: AsyncSession) -> Media:
    media_instance = Media(url=file_url, tweet_id=None)
    session.add(media_instance)
    await session.commit()
    await session.refresh(media_instance)
    return media_instance


async def delete_medias(medias: List) -> None:
    if medias:
        tasks = [delete_file(media.url) for media in medias]
        await gather(*tasks)