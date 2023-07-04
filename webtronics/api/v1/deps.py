from typing import Generator

from webtronics.db.session import Session


async def get_db_session() -> Generator:
    async with Session() as session:
        yield session
