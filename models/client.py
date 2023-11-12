import datetime

from pydantic import BaseModel, Field


class Client(BaseModel):
    id: int
    document: str = Field(..., title="Document", max_length=300)
    surname: str = Field(..., title="Surname", max_length=80)
    first_name: str = Field(..., title="First Name", max_length=80)
    patronymic: str = Field(..., title="Patronymic", max_length=80)
    birthday: datetime.date = Field(..., title="Birthday")


class ClientIn(BaseModel):
    document: str = Field(..., title="Document", max_length=300)
    surname: str = Field(..., title="Surname", max_length=80)
    first_name: str = Field(..., title="First Name", max_length=80)
    patronymic: str = Field(..., title="Patronymic", max_length=80)
    birthday: datetime.date = Field(..., title="Birthday")
