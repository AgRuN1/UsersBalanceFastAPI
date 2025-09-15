import uvicorn
from fastapi import FastAPI
from fastapi_auth_middlewares import JwtAuthMiddleware

from app.routes import get_apps_router
from app.config.settings import project_settings


def get_application() -> FastAPI:
    application = FastAPI(
        title=project_settings.PROJECT_NAME,
        debug=project_settings.DEBUG,
        version=project_settings.VERSION
    )
    application.add_middleware(
        JwtAuthMiddleware,
        secret_key=project_settings.SECRET_KEY,
        algorithms=[project_settings.ALGORITHM],
        public_paths=["/users/login"],
    )
    application.include_router(get_apps_router())

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
