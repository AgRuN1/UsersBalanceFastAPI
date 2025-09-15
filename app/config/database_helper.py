from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .settings import database_settings


async def get_database_session():
    engine = create_async_engine(
        url=database_settings.database_url,
        echo=database_settings.DB_ECHO_LOG
    )
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )
    db = session_factory()
    try:
        yield db
    finally:
        await db.close()