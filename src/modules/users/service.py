from typing import Optional
from sqlalchemy.orm import selectinload, joinedload
from src.services.base_service import BaseService
from src.repositories.user_repository import user_repository
from src.models.user_model import User
from src.models.follow_model import Follow


class UserService(BaseService):
    async def get_user_by_api_key(self, api_key: str) -> User | None:
        return await self.repository.get_by_api_key(api_key)


user_service = UserService(repository=user_repository)