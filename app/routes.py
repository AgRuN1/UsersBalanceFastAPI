from fastapi import APIRouter

from app.controllers import users_controller, account_controller


def get_apps_router():
    router = APIRouter()
    router.include_router(account_controller.router)
    router.include_router(users_controller.router)
    return router