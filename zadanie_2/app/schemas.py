from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    name: str


class UserAddress(BaseModel):
    id: int | None
    type: str | None
    city: str | None
    street: str | None
    building: str | None


class UserAddAddress(BaseModel):
    type: str
    city: str
    street: str
    building: str


class ViewUser(BaseModel):
    name: str
    id: int


class ShowUserByID(ViewUser):
    address: list[UserAddress]


class AddressUpdate(BaseModel):
    type: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    street: Optional[str] = Field(None)
    building: Optional[str] = Field(None)
