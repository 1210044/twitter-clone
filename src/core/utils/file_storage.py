from typing import List
from pathlib import Path
from fastapi import UploadFile
from asyncio import gather
from aiofiles import open as aio_open
from aiofiles.os import path as aio_path, remove as aio_remove


async def write_file(file_url: Path, file: UploadFile) -> None:
    async with aio_open(file_url, "wb") as f:
        file_content = await file.read()
        await f.write(file_content)


async def delete_file(file_url: str) -> None:
    path = Path(file_url)
    if await aio_path.exists(path):
        await aio_remove(file_url)


async def delete_files(urls: List[str]) -> None:
    if urls:
        tasks = [delete_file(url) for url in urls]
        await gather(*tasks)
