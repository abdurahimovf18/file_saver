from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

DB_URL = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(
    DB_URL, poolclass=NullPool,
)

new_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

metadata = MetaData()
