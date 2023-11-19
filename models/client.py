import datetime

from pydantic import BaseModel, Field, constr, field_validator


class Client(BaseModel):
    id: int
    document: str = Field(..., title="Document", max_length=300)
    surname: str = Field(..., title="Surname", max_length=80)
    first_name: str = Field(..., title="First Name", max_length=80)
    patronymic: str = Field(..., title="Patronymic", max_length=80)
    birthday: datetime.date = Field(..., title="Birthday")


class ClientIn(BaseModel):
    document: constr(min_length=10, max_length=300) = Field(..., title="Document", max_length=300)
    surname: str = Field(..., title="Surname", max_length=80)
    first_name: str = Field(..., title="First Name", max_length=80)
    patronymic: str = Field(..., title="Patronymic", max_length=80)
    birthday: datetime.date = Field(..., title="Birthday")

    @field_validator("birthday")
    def validate_age(cls, value):
        today = datetime.date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if not 18 <= age <= 100:
            raise ValueError("Age must be between 18 and 100.")
        return value
