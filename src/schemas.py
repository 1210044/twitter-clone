from pydantic import BaseModel


class StatusResponse(BaseModel):
    result: bool = True


class ErrorResponse(StatusResponse):
    result: bool = False
    error_type: str
    error_message: str