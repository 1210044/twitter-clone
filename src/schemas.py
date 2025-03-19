from typing import List
from pydantic import BaseModel


class StatusResponse(BaseModel):
    result: bool


class ErrorBase(BaseModel):
    error_type: str
    error_message: str


class ErrorResponse(ErrorBase, StatusResponse):
    pass


class ValidationErrors(StatusResponse):
    errors: List[ErrorBase]
