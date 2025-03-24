from src.models.media_model import Media
from src.medias.repositories.media_repository import media_repository
from src.schemas.media_schema import MediaCreate
from src.services.base_service import BaseService
from typing import List

class MediaService(BaseService):
    async def get_medias_by_ids(self, media_ids: List[int]) -> List[Media]:
        return await self.repository.get_medias_by_ids(media_ids)

    # Переиспользуем метод create, определенный в BaseService.
    # При вызове create мы передаем объект MediaCreate,
    # а BaseService преобразует его в словарь и вызывает метод create репозитория.

# Создаем экземпляр сервиса для Media, используя наш media_repository.
media_service = MediaService(repository=media_repository)
