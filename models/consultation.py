import datetime

from pydantic import BaseModel, Field


class Consultation(BaseModel):
    id: int
    client_id: int = Field(..., title="Client ID")
    pet_id: int = Field(..., title="Pet ID")
    date_time: datetime.datetime = Field(..., title="Consultation Date and Time")
    description: str = Field(default='', title="Description", max_length=300)


class ConsultationIn(BaseModel):
    client_id: int = Field(..., title="Client ID")
    pet_id: int = Field(..., title="Pet ID")
    date_time: datetime.datetime = Field(..., title="Consultation Date and Time")
    description: str = Field(default='', title="Description", max_length=300)
