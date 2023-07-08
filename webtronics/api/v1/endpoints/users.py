from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics import schemas, models, crud
from webtronics.api.deps import get_db_session
from webtronics.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
