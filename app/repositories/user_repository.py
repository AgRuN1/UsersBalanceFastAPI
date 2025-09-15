from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select

from app.models import User
from app.config.database_helper import get_database_session
from app.schemas.user import UserRequest
from app.services.password_service import PasswordService


class UserRepository:

    def __init__(
            self,
            session=Depends(get_database_session),
            pwd_service: PasswordService = Depends()
    ):
        self.session = session
        self.pwd_service = pwd_service

    async def get(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="answer not found")
        return user

    async def list(self) -> List[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_email(self, email: str) -> None|User:
        query = select(User).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user: UserRequest) -> None:
        new_user = User(
            email=user.email,
            password=self.pwd_service.get_password_hash(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
            is_admin=user.is_admin,
        )
        self.session.add(new_user)
        await self.session.commit()

    async def update(self, user_id: int, user: UserRequest) -> None:
        updating_user = await self.session.get(User, user_id)
        if not updating_user:
            raise HTTPException(status_code=404, detail="user not found")
        updating_user.email = user.email
        updating_user.password = self.pwd_service.get_password_hash(user.password)
        updating_user.first_name = user.first_name
        updating_user.last_name = user.last_name
        updating_user.is_admin = user.is_admin
        await self.session.commit()

    async def delete(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        await self.session.delete(user)
        await self.session.commit()