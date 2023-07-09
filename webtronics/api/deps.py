import aioredis
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from webtronics.db.session import Session
from webtronics.core.config import settings
from webtronics.core import security
from webtronics import models, schemas, crud


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/{settings.API_ROUTE_STR}/{settings.CURRENT_API_VERSION}/auth/login/"
)


async def get_db_session():
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
        db: Session = Depends(get_db_session),
        token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, pk=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_redis_cache():
    async with aioredis.from_url(settings.REDIS_URL) as cache_session:
        yield cache_session
