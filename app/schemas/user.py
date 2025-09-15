import re
from decimal import Decimal
from http.client import HTTPException

from pydantic import BaseModel, ConfigDict, field_validator, Field


class UserAccount(BaseModel):
    id: int
    balance: Decimal = Field(max_digits=10, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_admin: bool
    accounts: list[UserAccount]

    model_config = ConfigDict(from_attributes=True)


class UserRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    is_admin: bool

    @field_validator('email')
    @classmethod
    def check_email(cls, value):
        if not re.match(r'^[A-Za-z0-9.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', value):
            raise HTTPException(422, 'email is invalid')
        return value

    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        if not re.match(r'^[A-Za-z0-9._%+-]{4,20}$', value):
            raise HTTPException(422, 'password is invalid')
        return value

    @field_validator('last_name', 'first_name')
    @classmethod
    def check_name(cls, value):
        if not re.match(r'^[A-Z][a-z]{1,20}$', value):
            raise HTTPException(422, 'name is invalid')
        return value