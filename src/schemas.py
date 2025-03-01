from typing import List
from pydantic import BaseModel


class StatusResponse(BaseModel):
    result: bool


class ValidationError(BaseModel):
    error_type: str
    error_message: str


class ErrorResponse(ValidationError, StatusResponse):
    pass


class ValidationErrors(StatusResponse):
    errors: List[ValidationError]