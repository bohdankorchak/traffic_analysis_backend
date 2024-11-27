from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from ..config import Config

Base = declarative_base()


async def init_db():
    """
    Ініціалізація бази даних: створення таблиць.
    """
    async_engine = create_async_engine(Config.DATABASE_URL, echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
