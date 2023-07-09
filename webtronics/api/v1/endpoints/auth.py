from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from webtronics.api.deps import get_db_session
from webtronics.core.config import settings
from webtronics.core import security
from webtronics import schemas, crud
from webtronics.integrations.clearbit.tasks import update_user_clearbit_data, update_user_clearbit_data_2

router = APIRouter()


@router.post("/login/", response_model=schemas.Token)
async def login(
    db: AsyncSession = Depends(get_db_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/signup/", response_model=schemas.User)
async def sign_up(
    background_tasks: BackgroundTasks,
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    user = await crud.user.get_by_email(db, email=user_in.email)
    if not user:
        user = await crud.user.create(db, obj_in=user_in)
        background_tasks.add_task(update_user_clearbit_data, db, user_id=user.id, user_email=user_in.email)
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with given email already exists")
