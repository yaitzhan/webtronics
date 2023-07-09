from sqlalchemy.orm import Session

from webtronics import crud, schemas
from webtronics.core.config import settings
from webtronics.db import base  # noqa: F401


def init_db(db: Session) -> None:
    user = crud.user.sync_get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.sync_create(db, obj_in=user_in)  # noqa: F841
