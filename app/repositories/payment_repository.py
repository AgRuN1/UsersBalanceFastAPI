from fastapi import Depends

from app.models import Payment
from app.config.database_helper import get_database_session


class PaymentRepository:

    def __init__(self, session=Depends(get_database_session)):
        self.session = session

    async def create(self, account_id: int, amount: float) -> None:
        payment = Payment(account_id=account_id, amount=amount)
        self.session.add(payment)
        await self.session.commit()