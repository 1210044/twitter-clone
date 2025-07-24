from fastapi import APIRouter, UploadFile, Depends

from src.config.project_config import settings
from src.dependencies.auth_dependencies import get_current_user
from src.models.user_model import User
from src.schemas.media_schema import MediaCreate, MediaResponse
from src.services.media_service import media_service


router = APIRouter(prefix="/medias")


@router.post("", response_model=MediaResponse)
async def upload_media(
    file: UploadFile,
    user: User = Depends(get_current_user),
) -> MediaResponse:
    file_url = settings.TWEETS_MEDIA_DIR / file.filename
    # await MediaService.write_file(file_url, file)
    media_instance = await media_service.create(file_url)
    return MediaResponse(result=True, media_id=media_instance.id)
