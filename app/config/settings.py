from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()

class ProjectSettings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    PAYMENT_SECRET: str
    SECRET_KEY: str
    ALGORITHM: str


class DataBaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DB_ECHO_LOG: bool = False

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


database_settings = DataBaseSettings()

project_settings = ProjectSettings()