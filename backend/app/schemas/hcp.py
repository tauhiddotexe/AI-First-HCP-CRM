from datetime import datetime
from pydantic import BaseModel


class HCPCreate(BaseModel):
    first_name: str
    last_name: str
    title: str | None = None
    specialization: str | None = None
    hospital: str | None = None
    city: str | None = None
    phone: str | None = None
    email: str | None = None


class HCPUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    title: str | None = None
    specialization: str | None = None
    hospital: str | None = None
    city: str | None = None
    phone: str | None = None
    email: str | None = None


class HCPResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    title: str | None = None
    specialization: str | None = None
    hospital: str | None = None
    city: str | None = None
    phone: str | None = None
    email: str | None = None
    created_at: datetime

    model_config = {'from_attributes': True}
