from fastapi import Depends

from app.models import Account
from app.config.database_helper import get_database_session


class AccountRepository:

    def __init__(self, session=Depends(get_database_session)):
        self.session = session

    async def get(self, account_id: int) -> Account|None:
        account = await self.session.get(Account, account_id)
        return account

    async def create(self, account_id: int, user_id: int, balance: float) -> None:
        account = Account(id=account_id, user_id=user_id, balance=balance)
        self.session.add(account)
        await self.session.commit()