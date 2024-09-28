from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from misc.config import POSTGRES_URL


engine = create_async_engine(POSTGRES_URL)
async_session = async_sessionmaker(engine)

Base = declarative_base()


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_database():
    await engine.dispose()
