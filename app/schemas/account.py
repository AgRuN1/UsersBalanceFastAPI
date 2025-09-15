from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    email: str
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class PaymentResponse(BaseModel):
    amount: float

    model_config = ConfigDict(from_attributes=True)


class AccountResponse(BaseModel):
    id: int
    user: UserResponse
    balance: Decimal = Field(max_digits=10, decimal_places=2)
    payments: list[PaymentResponse]

    model_config = ConfigDict(from_attributes=True)