import aiofiles
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from src.medias.models import Media


async def write_file(file_url: Path, file: UploadFile) -> None:
    async with aiofiles.open(file_url, 'wb') as f:
        file_content = await file.read()
        await f.write(file_content)


# async def 


async def create_media(file_url, session: AsyncSession) -> Media:
    media_instance = Media(url=file_url, tweet_id=None)
    session.add(media_instance)
    await session.commit()
    await session.refresh(media_instance)
    return media_instance