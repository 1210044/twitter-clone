from fastapi import APIRouter, File, UploadFile, Depends

from src.config.project_config import settings
from src.config.database.db_helper import db_helper
from src.auth.dependencies import get_user
from src.models.user_model import User
from src.schemas.media_schema import MediaCreate, MediaOut
from src.medias import service as MediaService
from src.medias import crud as MediaCrud

router = APIRouter(prefix="/medias")


@router.post("", response_model=MediaOut)
async def upload_media(
    user: User = Depends(get_user),
    session=Depends(db_helper.get_db_session),
    file: UploadFile = File(...),
) -> MediaOut:
    file_url = settings.TWEETS_MEDIA_DIR / file.filename
    await MediaService.write_file(file_url, file)
    media_instance = await MediaCrud.create_media(file_url.as_posix(), session)
    return MediaOut(result=True, media_id=media_instance.id)
