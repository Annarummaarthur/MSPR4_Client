from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ClientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    username: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    postal_code: Optional[str] = None
    city: Optional[str] = None

    profile_first_name: Optional[str] = None
    profile_last_name: Optional[str] = None

    company_name: Optional[str] = None


class ClientUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    profile_first_name: Optional[str] = None
    profile_last_name: Optional[str] = None
    company_name: Optional[str] = None


class Client(ClientBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
