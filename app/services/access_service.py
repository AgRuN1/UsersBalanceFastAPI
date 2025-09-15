from datetime import datetime, timezone, timedelta
from http.client import HTTPException

from fastapi import Request, Depends

from jose import jwt

from app.config.settings import project_settings
from app.models import User
from app.repositories.user_repository import UserRepository


async def get_current_user(request: Request, userRepository: UserRepository=Depends()) -> User:
    user_id = request.state.user['user_id']
    user = await userRepository.get(user_id)
    return user

async def is_admin(user: User=Depends(get_current_user)) -> bool:
    if user.is_admin:
        return True
    raise HTTPException(403, "Forbidden")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, project_settings.SECRET_KEY, algorithm=project_settings.ALGORITHM)
    return encode_jwt