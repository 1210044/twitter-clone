from fastapi import Depends, Security
from fastapi.security.api_key import APIKeyHeader

from src.db import get_session
from src.auth.models import User
from src.auth.schemas import ApiKey
from src.auth.crud import get_user_by_api_key
from src.auth.exceptions import InvalidCredentialsException


API_KEY_NAME = "api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_user(
        api_key: str = Security(api_key_header), 
        session = Depends(get_session)
        ) -> User:
    api_key_schema = ApiKey(api_key=api_key)
    user = await get_user_by_api_key(api_key_schema.api_key, session)
    if not user:
        raise InvalidCredentialsException()
    return user