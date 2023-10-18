from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config.config import config

async_engine = create_async_engine(
    f'postgresql+asyncpg://{config.POSTGRES_USER}:'
    f'{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:'
    f'{config.POSTGRES_PORT}/{config.POSTGRES_DB}',
    pool_recycle=3600
)

async_sesison_factory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sesison_factory() as session:
        yield session


@asynccontextmanager
async def provide_session():
    async with async_sesison_factory() as session:
        try:
            yield session
            await session.commit()
            await session.close()
        except:
            await session.rollback()
            raise


Base = declarative_base()
