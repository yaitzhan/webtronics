from webtronics import crud, schemas
from webtronics.db.session import Session
from webtronics.core.config import settings
from webtronics.db import base  # noqa: F401


async def init_db() -> None:
    async with Session() as db:
        user = await crud.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            await crud.user.create(db, obj_in=user_in)


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
