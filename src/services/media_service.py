from src.models.media_model import Media
from src.repositories.media_repository import media_repository
from src.schemas.media_schema import MediaCreate
from src.services.base_service import BaseService
from typing import List


class MediaService(BaseService):

    async def get_by_ids(self, media_ids: List[int]) -> List[Media]:
        """Получает список медиафайлов по ID через filter"""
        return await self.repository.filter(filters={"id": media_ids})


media_service = MediaService(repository=media_repository)