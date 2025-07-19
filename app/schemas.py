from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class ClientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    profile_first_name: Optional[str] = None
    profile_last_name: Optional[str] = None
    company_name: Optional[str] = None


class ClientUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    profile_first_name: Optional[str] = None
    profile_last_name: Optional[str] = None
    company_name: Optional[str] = None


class Client(ClientBase):
    id: Optional[int] = None
