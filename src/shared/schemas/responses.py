from pydantic import BaseModel


class Status(BaseModel):
    result: bool