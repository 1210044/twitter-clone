from typing import List
from pydantic import BaseModel

from src.schemas.status_schema import Status


class ErrorBase(BaseModel):
    error_type: str
    error_message: str


class ErrorOut(ErrorBase, Status):
    pass


class ValidationErrors(Status):
    errors: List[ErrorBase]