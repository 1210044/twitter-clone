from typing import List
from pydantic import BaseModel


class StatusResponseTrue(BaseModel):
    result: bool = True


class StatusResponseFalse(BaseModel):
    result: bool = False


class ValidationError(BaseModel):
    error_type: str
    error_message: str


class ErrorResponse(ValidationError, StatusResponseFalse):
    pass


class ValidationErrors(StatusResponseFalse, BaseModel):
    errors: List[ValidationError]