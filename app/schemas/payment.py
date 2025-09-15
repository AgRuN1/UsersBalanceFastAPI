from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    signature: str