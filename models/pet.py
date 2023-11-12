import datetime

from pydantic import BaseModel, Field


class Pet(BaseModel):
    id: int
    client_id: int = Field(..., title="Client ID")
    name: str = Field(..., title="Name", max_length=80)
    birthday: datetime.date = Field(..., title="Birthday")


class PetIn(BaseModel):
    client_id: int = Field(..., title="Client ID")
    name: str = Field(..., title="Name", max_length=80)
    birthday: datetime.date = Field(..., title="Birthday")
