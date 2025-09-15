import re

from pydantic import BaseModel, field_validator


class Auth(BaseModel):
    email: str
    password: str

    @field_validator('email')
    @classmethod
    def not_empty(cls, value):
        if not re.match('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', value):
            raise ValueError('Login is invalid')
        return value

    @field_validator('password')
    @classmethod
    def not_empty(cls, value):
        if not re.match('[a-zA-Z0-9]{4,20}', value):
            raise ValueError('Password is invalid')
        return value