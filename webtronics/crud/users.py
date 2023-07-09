from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from webtronics.core.security import get_password_hash, verify_password
from webtronics.crud.base import CRUDBase
from webtronics.models.users import User, UserAdditional
from webtronics.schemas.users import UserCreate, UserUpdate, UserAdditionalCreate, UserAdditionalUpdate


class CRUDUserAdditional(CRUDBase[UserAdditional, UserAdditionalCreate, UserAdditionalUpdate]):
    async def get_by_user_id(self, db: AsyncSession, *, user_id: int) -> Optional[User]:
        query = select(self.model).filter_by(user_id=user_id)
        row = await db.execute(query)
        return row.scalar_one_or_none()


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(self.model).filter(User.email == email)
        row = await db.execute(query)
        return row.scalar_one_or_none()

    def sync_get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = self.model(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)

        await db.flush()
        additional = UserAdditional(user_id=db_obj.id)
        db.add(additional)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    def sync_create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = self.model(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        user_obj = await self.get_by_email(db, email=email)
        if not user_obj:
            return None
        if not verify_password(password, user_obj.hashed_password):
            return None
        return user_obj

    def is_active(self, user_obj: User) -> bool:
        return user_obj.is_active

    def is_superuser(self, user_obj: User) -> bool:
        return user_obj.is_superuser


user = CRUDUser(User)
user_additional = CRUDUserAdditional(UserAdditional)
