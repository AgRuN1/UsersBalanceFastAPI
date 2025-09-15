from typing import List

from fastapi import Depends, APIRouter, HTTPException

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Auth
from app.schemas.user import UserResponse, UserRequest
from app.services.access_service import create_access_token, get_current_user, is_admin
from app.services.password_service import PasswordService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login(
        authData: Auth,
        userRepository: UserRepository = Depends(),
        passwordService: PasswordService = Depends()
) -> dict:
    user = await userRepository.get_by_email(authData.email)
    if user is None or not passwordService.verify_password(authData.password, user.password):
        raise HTTPException(401, 'login failed')
    return {
        "access_token": create_access_token({'user_id': user.id})
    }

@router.get("/me")
async def get_user(
        user: User = Depends(get_current_user)
) -> UserResponse:
    return UserResponse.model_validate(user)

@router.get("/list")
async def get_user(
        userRepository: UserRepository = Depends(),
        is_admin: bool = Depends(is_admin)
) -> List[UserResponse]:
    users = await userRepository.list()
    return [UserResponse.model_validate(user) for user in users]

@router.get("/{user_id}")
async def get_user(
        user_id: int,
        userRepository: UserRepository = Depends(),
        is_admin: bool = Depends(is_admin)
) -> UserResponse:
    user = await userRepository.get(user_id)
    return UserResponse.model_validate(user)

@router.patch("/{user_id}")
async def update_user(
        user_id: int,
        user: UserRequest,
        userRepository: UserRepository = Depends(),
        is_admin: bool = Depends(is_admin)
) -> dict:
    await userRepository.update(user_id, user)
    return {
        'success': True
    }

@router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        userRepository: UserRepository = Depends(),
        is_admin: bool = Depends(is_admin)
) -> dict:
    await userRepository.delete(user_id)
    return {
        'success': True
    }

@router.post("/")
async def create_user(
        user: UserRequest,
        userRepository: UserRepository = Depends(),
        is_admin: bool = Depends(is_admin)
) -> dict:
    check_user = await userRepository.get_by_email(user.email)
    if check_user is not None:
        raise HTTPException(409, 'user already exists')
    await userRepository.create(user)
    return {
        'success': True
    }
