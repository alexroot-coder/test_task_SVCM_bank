from pydantic import BaseModel


class User(BaseModel):
    name: str


class UserAddress(BaseModel):
    id: int
    type: str
    city: str
    street: str
    building: str


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
