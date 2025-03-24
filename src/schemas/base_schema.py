from typing import NewType

from pydantic import BaseModel, ConfigDict

PyModel = NewType("PyModel", BaseModel)


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)