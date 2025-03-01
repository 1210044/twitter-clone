from fastapi import APIRouter, File, Header, UploadFile, Depends

from src.logger import logger
from src.db import get_session
from src.config import TWEETS_MEDIA_DIR
from src.medias.schemas import MediaOut
from src.medias import service as MediaService

router = APIRouter(prefix='/medias')


@router.post('', response_model=MediaOut)
async def upload_media(api_key: str = Header(...), file: UploadFile = File(...), session = Depends(get_session)) -> MediaOut:
    file_url = TWEETS_MEDIA_DIR / file.filename
    await MediaService.write_file(file_url, file)
    media_instance = await MediaService.create_media(file_url.as_posix(), session)
    return MediaOut(result=True, media_id=media_instance.id)