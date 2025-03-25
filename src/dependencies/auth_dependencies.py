from typing import Optional
from fastapi import Depends, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

from src.config.database.db_helper import db_helper
from src.models.user_model import User
from src.schemas.api_key_schema import ApiKey
from src.services.user_service import user_service
from src.exceptions import user_exceptions


API_KEY_NAME = "api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_current_user(
    api_key: Optional[str] = Security(api_key_header), session=Depends(db_helper.get_db_session())
) -> User:
    try:
        api_key_schema = ApiKey(api_key=api_key)
    except ValidationError as e:
        raise RequestValidationError(errors=e.errors())
    user = 'admin' # await user_service.get_user_by_api_key(api_key_schema.api_key, session)
    if not user:
        raise user_exceptions.InvalidCredentialsException()
    return user
