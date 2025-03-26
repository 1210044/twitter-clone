from typing import Optional
from src.services.base_service import BaseService
from src.repositories.user_repository import user_repository
from src.models.user_model import User


class UserService(BaseService):
    async def get_user_by_api_key(self, api_key: str) -> Optional[User]:
        return await self.repository.get_single(
            api_key=api_key, 
            related=["followers", "followings"]
        )


user_service = UserService(repository=user_repository)