from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from webtronics.core.config import settings


engine = create_async_engine(settings.DB_URI, pool_pre_ping=True)

Session = async_scoped_session(
    session_factory=sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    ),
    scopefunc=current_task
)


async def get_db_session() -> AsyncGenerator:
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()
