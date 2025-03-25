from src.repositories.user_repository import user_repository
from src.services.base_service import BaseService


class UserService(BaseService):
    pass


user_service = UserService(repository=user_repository)