from typing import Dict
from fastapi import APIRouter, File, Header, UploadFile, Depends

from src.logger import logger
from src.db import get_session
from src.config import TWEETS_MEDIA_DIR
from src.medias.schemas import MediaOut
from src.medias import service

router = APIRouter(prefix='/medias')


@router.post('', response_model=MediaOut)
async def upload_media(api_key: str = Header(...), file: UploadFile = File(...), session = Depends(get_session)) -> Dict:
    file_url = TWEETS_MEDIA_DIR / file.filename
    await service.write_file(file_url, file)
    media_instance = await service.create_media(file_url.as_posix(), session)
    return {'media_id': media_instance.id}