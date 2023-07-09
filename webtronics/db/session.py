from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from webtronics.core.config import settings


async_engine = create_async_engine(settings.DB_URI, pool_pre_ping=True)

Session = async_scoped_session(
    session_factory=sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    ),
    scopefunc=current_task
)


engine = create_engine(settings.DB_URI.replace("+asyncpg", ""), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
