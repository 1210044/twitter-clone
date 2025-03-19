from fastapi import APIRouter, File, UploadFile, Depends

from src.config import TWEETS_MEDIA_DIR
from src.db import get_session
from src.auth.dependencies import get_user
from src.auth.models import User
from src.medias.schemas import MediaOut
from src.medias import service as MediaService
from src.medias import crud as MediaCrud

router = APIRouter(prefix="/medias")


@router.post("", response_model=MediaOut)
async def upload_media(
    user: User = Depends(get_user),
    session=Depends(get_session),
    file: UploadFile = File(...),
) -> MediaOut:
    file_url = TWEETS_MEDIA_DIR / file.filename
    await MediaService.write_file(file_url, file)
    media_instance = await MediaCrud.create_media(file_url.as_posix(), session)
    return MediaOut(result=True, media_id=media_instance.id)
